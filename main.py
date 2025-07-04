import requests
import os

from dotenv import load_dotenv
load_dotenv()

# Add your OpenRouter API key here (or use environment variables)
API_KEY = os.getenv("OPENROUTER_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",  # Replace with your site or leave default
    "X-Title": "Test OpenRouter Python App"
}

data = {
    "model": "deepseek/deepseek-r1:free",  
    "messages": [
        {"role": "user", "content": "Hello! What can you do?"}
    ]
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

if response.ok:
    reply = response.json()['choices'][0]['message']['content']
    print("Assistant:", reply)
else:
    print("Error:",response.text)