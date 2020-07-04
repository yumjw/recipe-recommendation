import json
import requests

# with statement
with open('test.json', mode='r', encoding='utf-8-sig') as json_file:
    if len(json_file.readlines()) !=0:
        json_file.seek(0)
    json_data = json.load(json_file)

res = requests.get('http://3.133.76.141:10001/plus?user_musts=["양배추"]&user_options=["햄"]')    # AWS
# res = requests.post("http://3.133.76.141:5000/recipes/", json=json_data) # AWS Original