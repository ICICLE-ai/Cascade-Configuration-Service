import streamlit as st

from dysci.model_utils import format_model_name, split_edge_models


def show_policy_workflow(
    policy: str,
    edge_model: str,
    cloud_model: str,
    threshold: float,
) -> None:
    """Display the workflow for the selected DYSCI policy."""

    normalized_policy = (
        str(policy)
        .strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )

    edge_models = split_edge_models(edge_model)
    first_edge_model = edge_models[0] if edge_models else format_model_name(edge_model)
    second_edge_model = edge_models[1] if len(edge_models) > 1 else "Second Edge Model"
    formatted_cloud_model = format_model_name(cloud_model)

    st.subheader("How the Selected Policy Works")

    if normalized_policy in {
        "sequential",
        "sequential cascade",
        "classic",
        "classic cascade",
    }:
        diagram = f'''
        digraph SequentialCascade {{
            rankdir=LR;
            graph [bgcolor="transparent", pad="0.4", nodesep="0.45", ranksep="0.40"];
            node [shape=box, style="rounded,filled", fontname="Arial", fontsize=12, margin="0.15,0.10"];
            edge [fontname="Arial", fontsize=11];

            input [label="Input Request", fillcolor="#F0F2F6"];
            edge_queue [label="Edge Queue", fillcolor="#E5E7EB"];
            edge_model [label="Edge Model\\n{first_edge_model}", fillcolor="#FDE2E2"];
            decision [label="Confidence ≥ {threshold:.2f}?", shape=diamond, style="filled", fillcolor="#FFF7BF"];
            edge_result [label="Return {first_edge_model} Result", fillcolor="#DCFCE7"];
            network [label="Network Transfer", fillcolor="#E0F2FE"];
            cloud_queue [label="Cloud Queue", fillcolor="#E5E7EB"];
            cloud_model [label="Cloud Model\\n{formatted_cloud_model}", fillcolor="#DBEAFE"];
            cloud_result [label="Return {formatted_cloud_model} Result", fillcolor="#DCFCE7"];

            input -> edge_queue;
            edge_queue -> edge_model;
            edge_model -> decision;
            decision -> edge_result [label="Yes"];
            decision -> network [label="No"];
            network -> cloud_queue;
            cloud_queue -> cloud_model;
            cloud_model -> cloud_result;
        }}
        '''

        st.graphviz_chart(diagram, use_container_width=True)
        st.info(
            f"DYSCI first executes **{first_edge_model}** on the edge. "
            f"If its confidence is at least **{threshold:.2f}**, the prediction "
            f"from **{first_edge_model}** is returned. Otherwise, the request is "
            f"transferred to the cloud, where **{formatted_cloud_model}** performs "
            "inference and returns the final result."
        )

    elif normalized_policy in {
        "cloud speculation",
        "cloud speculative",
        "spec b",
        "specb",
    }:
        diagram = f'''
        digraph CloudSpeculation {{
            rankdir=LR;
            graph [bgcolor="transparent", pad="0.8", nodesep="0.8", ranksep="1.8"];
            node [shape=box, style="rounded,filled", fontname="Arial", fontsize=12, margin="0.22,0.22"];
            edge [fontname="Arial", fontsize=11];

            input [label="Input Request", fillcolor="#F0F2F6"];
            edge_queue [label="Edge Queue", fillcolor="#E5E7EB"];
            edge_model [label="Edge Model\\n{first_edge_model}", fillcolor="#FDE2E2"];
            network [label="Network Transfer", fillcolor="#E0F2FE"];
            cloud_queue [label="Cloud Queue", fillcolor="#E5E7EB"];
            cloud_model [label="Cloud Model\\n{formatted_cloud_model}", fillcolor="#DBEAFE"];
            decision [label="Edge Confidence ≥ {threshold:.2f}?", shape=diamond, style="filled", fillcolor="#FFF7BF"];
            edge_result [label="Return {first_edge_model} Result\\nCancel Cloud", fillcolor="#DCFCE7"];
            cloud_result [label="Return {formatted_cloud_model} Result", fillcolor="#DCFCE7"];

            input -> edge_queue;
            input -> network;
            edge_queue -> edge_model;
            edge_model -> decision;
            network -> cloud_queue;
            cloud_queue -> cloud_model;
            decision -> edge_result [label="Yes"];
            decision -> cloud_result [label="No"];
            cloud_model -> cloud_result;
        }}
        '''

        st.graphviz_chart(diagram, use_container_width=True)
        st.info(
            f"DYSCI starts **{first_edge_model}** on the edge and "
            f"**{formatted_cloud_model}** in the cloud concurrently. If "
            f"**{first_edge_model}** finishes with confidence at least "
            f"**{threshold:.2f}**, its result is returned immediately and the cloud "
            "execution is cancelled. Otherwise, DYSCI waits for and returns the "
            f"result from **{formatted_cloud_model}**."
        )

    elif normalized_policy in {
        "edge speculation",
        "edge speculative",
        "po2",
        "power of two",
        "power2",
    }:
        diagram = f'''
        digraph EdgeSpeculation {{
            rankdir=LR;
            graph [bgcolor="transparent", pad="0.4", nodesep="0.45", ranksep="0.40"];
            node [shape=box, style="rounded,filled", fontname="Arial", fontsize=12, margin="0.15,0.10"];
            edge [fontname="Arial", fontsize=11];

            input [label="Input Request", fillcolor="#F0F2F6"];
            edge_queue_1 [label="Edge Queue", fillcolor="#E5E7EB"];
            edge_queue_2 [label="Edge Queue", fillcolor="#E5E7EB"];
            edge_model_1 [label="Edge Model 1\\n{first_edge_model}", fillcolor="#FDE2E2"];
            edge_model_2 [label="Edge Model 2\\n{second_edge_model}", fillcolor="#FDE2E2"];
            first_finish [label="First Completed\\nEdge Result", fillcolor="#E0F2FE"];
            first_decision [label="Confidence ≥ {threshold:.2f}?", shape=diamond, style="filled", fillcolor="#FFF7BF"];
            first_exit [label="Return First\\nEdge Result", fillcolor="#DCFCE7"];
            wait_second [label="Wait for Remaining\\nEdge Result", fillcolor="#E5E7EB"];
            second_decision [label="Confidence ≥ {threshold:.2f}?", shape=diamond, style="filled", fillcolor="#FFF7BF"];
            second_exit [label="Return Second\\nEdge Result", fillcolor="#DCFCE7"];
            network [label="Network Transfer", fillcolor="#E0F2FE"];
            cloud_queue [label="Cloud Queue", fillcolor="#E5E7EB"];
            cloud_model [label="Cloud Model\\n{formatted_cloud_model}", fillcolor="#DBEAFE"];
            cloud_result [label="Return {formatted_cloud_model} Result", fillcolor="#DCFCE7"];

            input -> edge_queue_1;
            input -> edge_queue_2;
            edge_queue_1 -> edge_model_1;
            edge_queue_2 -> edge_model_2;
            edge_model_1 -> first_finish;
            edge_model_2 -> first_finish;
            first_finish -> first_decision;
            first_decision -> first_exit [label="Yes"];
            first_decision -> wait_second [label="No"];
            wait_second -> second_decision;
            second_decision -> second_exit [label="Yes"];
            second_decision -> network [label="No"];
            network -> cloud_queue;
            cloud_queue -> cloud_model;
            cloud_model -> cloud_result;
        }}
        '''

        st.graphviz_chart(diagram, use_container_width=True)
        st.info(
            f"DYSCI sends the request to **{first_edge_model}** and "
            f"**{second_edge_model}** in parallel. It first checks whichever edge "
            "model finishes first. If that model produces confidence at least "
            f"**{threshold:.2f}**, DYSCI immediately returns its prediction. "
            "Otherwise, DYSCI waits for the remaining edge model. If the second "
            f"result also has confidence below **{threshold:.2f}**, the request is "
            f"transferred to **{formatted_cloud_model}** in the cloud, which returns "
            "the final prediction."
        )

    else:
        st.warning(f"No workflow diagram is currently defined for policy: {policy}")
