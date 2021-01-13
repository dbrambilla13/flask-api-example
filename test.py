import requests

# location of the Api 
BASE = "http://localhost:5000/"

response = requests.get(url=BASE+"api/v0/RandGen/")

print(response.json())