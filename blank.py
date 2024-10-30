import requests
import json  # Import json to pretty print

data = {
    "model": "llama3.2:1b",
    "prompt": "merhaba dünya",
    "stream": False
}

# Print the JSON to be sent

response = requests.post("http://localhost:11434/api/generate", json=data)

print(response.status_code)
print(response.text)
