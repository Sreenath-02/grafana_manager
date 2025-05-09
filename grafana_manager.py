import requests
import json


class GrafanaDatasourceManager:
    def __init__(self, grafana_url, api_key):
        """
        Initialize the GrafanaDatasourceManager with the Grafana URL and API key.
        """
        self.grafana_url = grafana_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_all_datasources(self):
        """
        Fetch all available data sources from Grafana.
        """
        api_endpoint = f"{self.grafana_url}/api/datasources"
        try:
            response = requests.get(api_endpoint, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to fetch data sources. Status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"An error occurred while fetching data sources: {e}")

    def add_datasource(self, datasource):
        """
        Add a new data source to Grafana using its API.
        """
        api_endpoint = f"{self.grafana_url}/api/datasources"
        try:
            response = requests.post(api_endpoint, headers=self.headers, data=json.dumps(datasource))
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise Exception(f"Failed to add data source. Status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"An error occurred while adding the data source: {e}")

    def fetch_metrics(self, data_source_url):
        """
        Fetch all available metrics from the selected data source.
        """
        try:
            response = requests.get(f"{data_source_url}/api/v1/label/__name__/values")
            if response.status_code == 200:
                return response.json()["data"]
            else:
                raise Exception(f"Failed to fetch metrics. Status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"An error occurred while fetching metrics: {e}")

    def create_panel(self, metric, data_source_name, visualization_type="gauge"):
        """
        Create a single panel for a given metric and data source.
        """
        visualization_mapping = {
            "gauge": "gauge",
            "time series": "timeseries",
            "bar gauge": "bargauge",
            "stat": "stat"
        }

        visualization_type_mapped = visualization_mapping.get(visualization_type, "gauge")

        panel = {
            "type": visualization_type_mapped,
            "title": f"{metric} ({data_source_name})",
            "gridPos": {"x": 0, "y": 0, "w": 12, "h": 9},
            "targets": [
                {
                    "datasource": data_source_name,
                    "expr": metric,
                    "refId": "A"
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "unit": "none",
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 50},
                            {"color": "red", "value": 80}
                        ]
                    },
                    "mappings": [],
                },
                "overrides": []
            },
            "options": {
                "showThresholdLabels": True,
                "showThresholdMarkers": True,
                "reduceOptions": {
                    "calcs": ["mean"],
                    "fields": "",
                    "values": False
                }
            }
        }
        return panel

    def create_dashboard_json(self, panels, data_source_name):
        """
        Create a Grafana dashboard JSON with user-defined panels for a specific data source.
        """
        dashboard = {
            "dashboard": {
                "id": None,
                "title": f"Dashboard for {data_source_name}",
                "panels": panels,
                "version": 1
            },
            "overwrite": True
        }
        return dashboard

    def create_or_update_dashboard(self, dashboard_json):
        """
        Create or update a Grafana dashboard using the Grafana API.
        """
        api_endpoint = f"{self.grafana_url}/api/dashboards/db"
        try:
            response = requests.post(api_endpoint, headers=self.headers, data=json.dumps(dashboard_json))
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise Exception(f"Failed to create/update dashboard. Status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"An error occurred while creating/updating the dashboard: {e}")