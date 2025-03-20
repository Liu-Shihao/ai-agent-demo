import os

import requests


os.environ["DEEPSEEK_API_KEY"] = "..."

def model_list():
    url = "https://api.deepseek.com/models"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer you-api-key'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    model_list()
