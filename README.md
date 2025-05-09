# Grafana Manager

A Python library for managing Grafana datasources, dashboards, and panels.

## Installation

```bash
pip install grafana-manager
```

## Usage

```python
from grafana_manager import GrafanaDatasourceManager

GRAFANA_URL = "http://localhost:3000"
API_KEY = "your_grafana_api_key"

grafana = GrafanaDatasourceManager(GRAFANA_URL, API_KEY)

# Example: Get all datasources
datasources = grafana.get_all_datasources()
print(datasources)

# Example: Add a new datasource
datasource = {
    "name": "MyDatasource",
    "type": "prometheus",
    "url": "http://prometheus.local",
    "access": "proxy",
    "basicAuth": False
}
response = grafana.add_datasource(datasource)
print(response)

# Example: Create a panel
panel = grafana.create_panel("custom_metric", "MyDatasource", "gauge")
print(panel)
```