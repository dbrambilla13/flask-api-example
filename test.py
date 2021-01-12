import requests

# location of the Api 
BASE = "http://localhost:5000/"

daniele = {
    'name' : 'daniele',
    'country' : 'it',
    'birth' : '13/02/1994'
}

response = requests.put(BASE + f"Contacts/1", daniele)

response = requests.get(BASE + "Contacts/1")



print(response.json())