import json
import os

with open("test-data/customers_data.json") as f:
    CUSTOMER_DATA = json.load(f)

print(CUSTOMER_DATA)