import requests
import json
from datetime import datetime
import os

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def test_openrouter_completion():
    headers = {
        'Authorization': f"Bearer {API_KEY}",  # Replace with your real API key
        'Content-Type': 'application/json'
    }

    data = {
        "model": "deepseek/deepseek-r1:free",  # You can change this to other models like mistralai/mixtral
        "messages": [{"role": "user", "content": "What is the capital of France?"}]
    }

    response = requests.post('https://openrouter.ai/api/v1/chat/completions', json=data, headers=headers)
    
    # Basic assertions
    assert response.status_code == 200, f"Status code: {response.status_code}, Response: {response.text}"
    response_data = response.json()
    assert 'choices' in response_data, "Missing 'choices' in response"

    # Log result to a file
    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": data["messages"][0]["content"],
        "model": data["model"],
        "response": response_data['choices'][0]['message']['content'],
        "status_code": response.status_code
    }

    with open("openrouter_test_results.jsonl", "a") as f:
        f.write(json.dumps(result) + "\n")

    print("✅ Test passed. Response saved to openrouter_test_results.jsonl")

if __name__ == "__main__":
    test_openrouter_completion()