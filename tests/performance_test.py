import requests
import time
import os

from dotenv import load_dotenv
load_dotenv()

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1:free"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

API_URL = "https://openrouter.ai/api/v1/chat/completions"

def send_request(prompt):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    start = time.time()
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    latency = time.time() - start

    if response.status_code != 200:
        print(f" Error: {response.status_code} | {response.text}")
        return None

    data = response.json()
    usage = data.get("usage", {})
    output = data["choices"][0]["message"]["content"]
    short_output = output[:50] + "..." if len(output) > 50 else output

    print(f" Prompt: {prompt[:30]} | Latency: {latency:.2f}s | Tokens: {usage} | Output: {short_output}")
    return latency, usage

def run_tests(prompts):
    results = []
    for prompt in prompts:
        result = send_request(prompt)
        if result:
            results.append(result)
    return results

# Example prompts
test_prompts = [
    "Summarize the theory of relativity.",
    "What is the capital of Brazil?",
    "Generate a poem about AI and humanity.",
    "Explain how blockchain works in simple terms.",
    "What's the weather like on Mars?",
]

if __name__ == "__main__":
    run_tests(test_prompts)
