import requests
import os

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def test_openrouter_math():
    headers = {
        'Authorization': f"Bearer {API_KEY}",  # Replace with your real API key
        'Content-Type': 'application/json'
    }

    data = {
        "model": "deepseek/deepseek-r1:free",  # You can change this to other models like mistralai/mixtral
        "messages": [{"role": "user", "content": "What is the result of 2 + 2?"}]
    }

    response = requests.post('https://openrouter.ai/api/v1/chat/completions', json=data, headers=headers)

    print("Response status code:", response.status_code)

    assert response.status_code == 200, f"Status code: {response.status_code}, Response: {response.text}"
    response_data = response.json()

     # Extract the model's answer from the response
    answer = response_data['choices'][0]['message']['content'].strip()

    #print("Model answer:", answer)

    assert "4" in answer, f"Expected 4, got {answer}"

    print("\n Assertion passed: Model gave a correct or acceptable answer.")
    
if __name__ == "__main__":
    test_openrouter_math()