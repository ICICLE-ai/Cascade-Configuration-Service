<!-- # Cascade Configuration Service

A Streamlit-based demo for the **Cascade Configuration Service**.

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

Among all feasible configurations, the service selects the configuration with the **lowest estimated latency**. -->



# Cascade Configuration Service

The Cascade Configuration Service is a Streamlit-based interface for selecting a model cascade configuration based on user-defined cost and error constraints. The service selects the lowest-latency feasible configuration from a predefined policy table and presents the selected configuration through an interactive interface.

**Tags:** Software

For guidance on the organization of Tutorials, How-To Guides, Explanation, and Reference material, see [Diátaxis](https://diataxis.fr/).

### License

License information will be added based on the license used by the ICICLE project.

## References

- [ICICLE](https://icicle.ai/)
- [Cascade Configuration Service Repository](https://github.com/ICICLE-ai/Cascade-Configuration-Service)

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Please report bugs, feature requests, or other issues through the GitHub Issues page:

https://github.com/ICICLE-ai/Cascade-Configuration-Service/issues

---

# Tutorials

## Running the Cascade Configuration Service Locally

### 1. Clone the repository

```bash
git clone https://github.com/ICICLE-ai/Cascade-Configuration-Service.git
cd Cascade-Configuration-Service
```

### 2. Install `uv`

This project uses `uv` for Python dependency management.

If `uv` is not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart the terminal or run:

```bash
source $HOME/.local/bin/env
```

Verify the installation:

```bash
uv --version
```

### 3. Install the project dependencies

```bash
uv sync
```

### 4. Start the service

Run the Streamlit application using:

```bash
uv run streamlit run src/cascade_configuration_service/app.py
```

By default, the application will be available at:

```text
http://localhost:8501
```

Open this address in a web browser to access the Cascade Configuration Service.

### 5. Run using the deployment entry point

The service can also be started using the deployment entry point:

```bash
PORT=8000 ./entrypoint.sh
```

The application will then be available at:

```text
http://localhost:8000
```

---

# How-To Guides

## Using the Service

The user provides two constraints:

- **Maximum Cost Budget (C)**
- **Maximum Error Budget (E)**

The service evaluates the available configurations and identifies those satisfying the provided constraints.

A configuration is considered feasible when:

```text
cost <= user cost budget
error <= user error budget
```

Among the feasible configurations, the service selects the configuration with the lowest estimated latency.

The service returns:

- Execution policy
- Edge model(s)
- Cloud model
- Confidence threshold
- Estimated latency
- Expected error
- Dynamic execution-policy workflow

If no configuration satisfies the specified constraints, the user can adjust the cost or error budget and run the selection again.

## Policy Table

The service uses a predefined policy table located at:

```text
data/policy_table.csv
```

The policy table contains the candidate configurations used by the service.

The CSV contains fields such as:

```text
policy
edge_model
cloud_model
threshold
cost
error
estimated_latency_ms
```

The included CSV provides the configuration data required by the current demonstration.

## Check Service Health

When the service is running on port `8000`, the Streamlit health endpoint can be checked using:

```bash
curl http://localhost:8000/_stcore/health
```

A healthy service returns:

```text
ok
```

---

# Explanation

## Overview

The Cascade Configuration Service provides a simple interface for selecting a suitable model cascade configuration based on user-defined requirements.

Users provide cost and error constraints, and the service returns a corresponding configuration from a predefined policy table. The interface also provides a visual representation of the selected configuration.

This repository contains the service implementation, configuration data, and supporting utilities required to run the application.

## Repository Structure

```text
Cascade-Configuration-Service/
├── .github/
│   └── workflows/
│       └── deploy.yaml
├── data/
│   └── policy_table.csv
├── src/
│   └── cascade_configuration_service/
│       ├── __init__.py
│       ├── app.py
│       └── dysci/
│           ├── __init__.py
│           ├── data_loader.py
│           ├── model_utils.py
│           ├── selector.py
│           └── visualization.py
├── .dockerignore
├── component-info.yaml
├── entrypoint.sh
├── icicle-service.yaml
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## Main Components

- `app.py` — provides the Streamlit user interface.
- `data_loader.py` — loads the policy configuration data.
- `selector.py` — handles configuration selection.
- `model_utils.py` — provides model-related utility functions.
- `visualization.py` — provides visualization utilities.
- `policy_table.csv` — contains the configurations used by the service.

## ICICLE CI/CD Deployment

The repository uses the ICICLE CI/CD workflow for building and deploying the service.

The main deployment-related files are:

- `.github/workflows/deploy.yaml` — defines the GitHub Actions deployment workflow.
- `icicle-service.yaml` — contains the ICICLE service deployment configuration.
- `entrypoint.sh` — defines how the application is started.
- `pyproject.toml` — defines the Python project and its dependencies.
- `uv.lock` — provides reproducible dependency versions.

Changes pushed to the `main` branch trigger the configured ICICLE CI/CD workflow.
