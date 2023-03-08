import requests
import json

data = [{'likes': 20,"name":"API REST","views":5000},{'likes': 10,"name":"Azure","views":1700},{'likes': 15,"name":"Django","views":1500},{'likes': 150,"name":"SQL","views":20000}]

BASE = "http://127.0.0.1:8080/"
headers = {'Content-Type': 'application/json'}
for i in range(len(data)):
   response = requests.put(BASE + "video/" + str(i),data[i])
   print(response.json())



