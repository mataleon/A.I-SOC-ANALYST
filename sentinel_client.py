import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SentinelClient:
    def __init__(self):
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        self.workspace = os.getenv("SENTINEL_WORKSPACE")
        self.resource_group = os.getenv("SENTINEL_RESOURCE_GROUP")
        self.token = self._get_token()

    def _get_token(self):
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "resource": "https://management.azure.com/"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        token_data = response.json()
        if "access_token" not in token_data:
            raise ValueError(f"Auth failed: {token_data.get('error_description', token_data)}")
        return token_data["access_token"]

    def get_incidents(self, limit=10):
        url = (f"https://management.azure.com/subscriptions/{self.subscription_id}"
               f"/resourceGroups/{self.resource_group}"
               f"/providers/Microsoft.OperationalInsights/workspaces/{self.workspace}"
               f"/providers/Microsoft.SecurityInsights/incidents"
               f"?api-version=2023-02-01&$top={limit}"
               f"&$orderby=properties/createdTimeUtc desc")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("value", [])

    def get_incident_alerts(self, incident_id):
        url = (f"https://management.azure.com/subscriptions/{self.subscription_id}"
               f"/resourceGroups/{self.resource_group}"
               f"/providers/Microsoft.OperationalInsights/workspaces/{self.workspace}"
               f"/providers/Microsoft.SecurityInsights/incidents/{incident_id}/alerts"
               f"?api-version=2023-02-01")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json().get("value", [])
