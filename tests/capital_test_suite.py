import csv
import os
import json
import time
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1:free"  # Or "openai/gpt-4", etc.

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

API_URL = "https://openrouter.ai/api/v1/chat/completions"

def load_test_data(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def query_model(prompt):
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)
    if response.status_code == 402:
        print(" Insufficient credits.")
        return None
    if response.status_code != 200:
        print(f" Error {response.status_code}: {response.text}")
        return None

    reply = response.json()['choices'][0]['message']['content']
    return reply.strip()

def evaluate_response(response, expected_capital):
    return expected_capital.lower() in response.lower()

def run_test_suite():
    test_data = load_test_data("prompts/capital_data.csv")
    results = []

    for item in test_data:
        country = item["country"]
        expected = item["expected_capital"]
        prompt = f"What is the capital of {country}?"

        print(f"🧪 Testing: {prompt}")
        response = query_model(prompt)
        if response is None:
            print("⚠️ Skipping due to error or no credits.")
            continue

        passed = evaluate_response(response, expected)
        print(f"Passed" if passed else f" Failed")
        print(f"→ Response: {response}\n")

        results.append({
            "timestamp": datetime.utcnow().isoformat(),
            "country": country,
            "prompt": prompt,
            "expected": expected,
            "response": response,
            "passed": passed
        })

        time.sleep(1)  # Avoid rate limits

    # Save results
    with open("capital_test_results.jsonl", "w", encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(" All results saved to capital_test_results.jsonl")

if __name__ == "__main__":
    run_test_suite()
