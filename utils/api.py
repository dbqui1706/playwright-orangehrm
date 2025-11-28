import requests

# get prameter from environment variable
import os
from dotenv import load_dotenv
load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_URL = os.getenv("API_URL")


print(BEARER_TOKEN)
print(API_URL)

headers = {"Authorization": f"Bearer {BEARER_TOKEN}", "Content-Type": "application/json"}

class APIClient:
    def __init__(self, api_url=API_URL, headers=headers):
        self.api_url = api_url
        self.headers = headers

    def get(self, endpoint, params=None):
        response = requests.get(f"{self.api_url}/{endpoint}", headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        response = requests.post(f"{self.api_url}/{endpoint}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None):
        response = requests.put(f"{self.api_url}/{endpoint}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        response = requests.delete(f"{self.api_url}/{endpoint}", headers=self.headers)
        response.raise_for_status()
        return response.status_code

client = APIClient()
def list_all_employees_for_project():
    """
    List Available Employees for Project Admin
    """
    return client.get("project-admins")
