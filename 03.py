import requests
import pandas as pd
import json

url = "http://ip-api.com/json/?fields=61439"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)
text = response.text.encode('utf8')
a_json = json.loads(text)
print(a_json)
