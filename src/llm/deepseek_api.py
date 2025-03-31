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


def reasoner_test():
    from openai import OpenAI
    client = OpenAI(api_key="...", base_url="https://api.deepseek.com")

    # Round 1
    messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages
    )

    reasoning_content = response.choices[0].message.reasoning_content
    print(reasoning_content)
    content = response.choices[0].message.content
    print(content)

    # Round 2
    # messages.append({'role': 'assistant', 'content': content})
    # messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
    # response = client.chat.completions.create(
    #     model="deepseek-reasoner",
    #     messages=messages
    # )
    # print(response)
    # ...


if __name__ == "__main__":
    # model_list()
    reasoner_test()
