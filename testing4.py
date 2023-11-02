import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
headers = {"Authorization": f"Bearer {'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'}"}

'''
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "What is meant by quantum computing",
})
print(output[0]['generated_text'])
'''

# write program to print numbers from 1 to 100?


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "What's your name?",
})
print(output)
print(output[0]['generated_text'])
