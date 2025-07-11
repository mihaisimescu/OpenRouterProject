import requests
import os
import time

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1:free"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Define your regression test cases
regression_tests = [
    {
        "prompt": "What is the capital of France?",
        "expected_substring": "Paris"
    },
    {
        "prompt": "2 + 2 = ?",
        "expected_substring": "4"
    },
    {
        "prompt": "Translate 'hello' to Spanish.",
        "expected_substring": "hola"
    },
    {
        "prompt": "In what year was Arsenal Football Club founded?",
        "expected_substring": "1886"
    },
    {
        "prompt": "What animal is the called the king of the jungle ?",
        "expected_substring": "Lion"
    },
    {
        "prompt": "What is the largest planet in our solar system?",''
        "expected_substring": "Jupiter"
    }
]

def run_regression_test(test_case):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": test_case["prompt"]}]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text}")
        return False

    output = response.json()["choices"][0]["message"]["content"].lower()
    expected = test_case["expected_substring"].lower()

    passed = expected in output
    print(f"{'✅' if passed else '❌'} Prompt: {test_case['prompt'][:40]} | Expected: '{expected}' | Got: {output[:100]}...")
    return passed

def run_all_regression_tests():
    failures = 0
    for test in regression_tests:
        if not run_regression_test(test):
            failures += 1
    print(f"\n📋 Regression summary: {len(regression_tests) - failures} passed / {len(regression_tests)} total.")

if __name__ == "__main__":
    run_all_regression_tests()
