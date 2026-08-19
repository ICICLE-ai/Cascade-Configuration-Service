from pathlib import Path

import streamlit as st

from dysci.data_loader import load_policy_table
from dysci.model_utils import format_model_name, split_edge_models
from dysci.selector import select_best_policy
from dysci.visualization import show_policy_workflow


POLICY_FILE = Path("data/policy_table.csv")

st.set_page_config(
    page_title="DYSCI Cascade Configuration",
    page_icon="⚙️",
    layout="wide",
)

st.title("DYSCI: Dynamic Speculative Cascading for Serverless Model Inference")
st.subheader("Cascade Configuration Service")

st.write(
    "Provide the maximum cost and error constraints. "
    "DYSCI automatically selects the optimal execution policy, "
    "edge model, cloud model, and confidence threshold."
)

try:
    policies = load_policy_table(POLICY_FILE)
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

st.subheader("User Requirements")

input_col1, input_col2 = st.columns(2)

with input_col1:
    cost_budget = st.number_input(
        "Maximum Cost Budget (C)",
        min_value=0.0,
        max_value=200.0,
        value=50.0,
        step=5.0,
        help="Maximum allowed expected execution cost.",
    )

with input_col2:
    error_budget = st.number_input(
        "Maximum Error Budget (E)",
        min_value=0.0,
        max_value=1.0,
        value=0.10,
        step=0.01,
        format="%.2f",
        help="Maximum allowed classification error.",
    )

if st.button(
    "Select Optimal Cascade",
    type="primary",
    use_container_width=True,
):
    selected, feasible_policies = select_best_policy(
        policy_table=policies,
        cost_budget=cost_budget,
        error_budget=error_budget,
    )

    st.divider()

    if selected is None:
        st.warning(
            "No cascade satisfies both constraints. "
            "Increase the cost budget or allow a larger error."
        )
    else:
        st.success("An optimal feasible cascade was found.")
        st.subheader("Selected Cascade")

        display_edge_model = " + ".join(
            split_edge_models(str(selected["edge_model"]))
        )
        display_cloud_model = format_model_name(
            str(selected["cloud_model"])
        )

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric("Execution Policy", str(selected["policy"]))
            st.metric("Confidence Threshold", f'{selected["threshold"]:.2f}')

        with result_col2:
            st.metric("Edge Model", display_edge_model)
            st.metric("Cloud Model", display_cloud_model)

        with result_col3:
            st.metric(
                "Estimated Latency",
                f'{selected["estimated_latency_ms"]:.0f} ms',
            )
            st.metric("Expected Error", f'{selected["error"]:.3f}')

        st.divider()

        show_policy_workflow(
            policy=str(selected["policy"]),
            edge_model=str(selected["edge_model"]),
            cloud_model=str(selected["cloud_model"]),
            threshold=float(selected["threshold"]),
        )

        st.divider()
        st.subheader("Decision Summary")

        st.code(
            f'''{{
  "cost_budget": {cost_budget:.2f},
  "error_budget": {error_budget:.2f},
  "selected_policy": "{selected['policy']}",
  "edge_model": "{selected['edge_model']}",
  "cloud_model": "{selected['cloud_model']}",
  "threshold": {selected['threshold']:.2f},
  "estimated_latency_ms": {selected['estimated_latency_ms']:.2f},
  "expected_cost": {selected['cost']:.2f},
  "expected_error": {selected['error']:.3f}
}}''',
            language="json",
        )

        with st.expander("Show all feasible configurations"):
            columns_to_show = [
                "policy",
                "edge_model",
                "cloud_model",
                "threshold",
                "cost",
                "error",
                "estimated_latency_ms",
            ]
            st.dataframe(
                feasible_policies[columns_to_show],
                use_container_width=True,
                hide_index=True,
            )

with st.expander("Show complete offline policy table"):
    st.dataframe(
        policies,
        use_container_width=True,
        hide_index=True,
    )
