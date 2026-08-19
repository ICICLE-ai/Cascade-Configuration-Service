# Cascade Configuration Service

A Streamlit demo for **Cascade Configuration Service**.

The service takes a maximum cost budget and maximum error budget and selects the lowest-latency feasible cascade configuration.

## Outputs

- Execution policy
- Edge model(s)
- Cloud model
- Confidence threshold
- Estimated latency
- Expected error
- Dynamic execution-policy workflow

## Repository Structure

```text
cascade-service/
├── app.py
├── data/
│   └── policy_table.csv
├── dysci/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── selector.py
│   ├── model_utils.py
│   └── visualization.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Policy Table

The CSV must contain these columns:

```text
policy
edge_model
cloud_model
threshold
cost
error
estimated_latency_ms
```

The included CSV is only a small example. 

## Selection Rule

A configuration is feasible when:

```text
cost <= user cost budget
error <= user error budget
```

Among feasible configurations, System selects the configuration with the lowest estimated latency.

