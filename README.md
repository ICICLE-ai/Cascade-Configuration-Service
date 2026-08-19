# Cascade Configuration Service

A Streamlit-based demo for the **DYSCI Cascade Configuration Service**.

The service takes a maximum cost budget and maximum error budget as input and selects the lowest-latency feasible cascade configuration.

## Outputs

The service returns:

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

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/isurugamage37/Cascade-Configuration-Service.git
cd Cascade-Configuration-Service
```

> Note: This is a private repository. Access must be granted before cloning.

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

For macOS/Linux:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install the required dependencies

```bash
pip install -r requirements.txt
```

## Deployment

### Run the service locally

Start the Streamlit application using:

```bash
streamlit run app.py
```

By default, the application will be available at:

```text
http://localhost:8501
```

Open the provided URL in a web browser to access the Cascade Configuration Service.

## Using the Service

The user provides two constraints:

- **Maximum Cost Budget (C)**
- **Maximum Error Budget (E)**

The service then identifies the lowest-latency feasible cascade and returns the selected execution policy, edge model(s), cloud model, and confidence threshold.

The interface also visualizes how the selected execution policy operates.

## Policy Table

The service uses an offline-generated policy table located at:

```text
data/policy_table.csv
```

The CSV must contain the following columns:

```text
policy
edge_model
cloud_model
threshold
cost
error
estimated_latency_ms
```

The included CSV is a small example policy table.

## Selection Rule

A cascade configuration is considered feasible when:

```text
cost <= user cost budget
error <= user error budget
```

Among all feasible configurations, the service selects the configuration with the **lowest estimated latency**.