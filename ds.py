import requests

url = "https://api.deepseek.com/models"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer sk-c586b9b5ed944a61a4e676416952ee93'
}


response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)