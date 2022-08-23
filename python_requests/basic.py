import requests

endpoint = 'http://localhost:8000/rest_api/'          #'http://127.0.0.1:8000/my_customers_list/38'

response = requests.get(endpoint)

print(response.text)