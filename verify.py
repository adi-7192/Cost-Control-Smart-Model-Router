import subprocess
import time
import requests
import sys
import os

def run_verification():
    print("Starting server...")
    # Start the server
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for server to start
        time.sleep(5)
        
        base_url = "http://localhost:8001"
        
        # Test 1: Simple Prompt (Expect Phi-3)
        print("\nTest 1: Simple Prompt")
        response = requests.post(f"{base_url}/route", json={"prompt": "What is 2+2?"})
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data}")
            print(f"Reasoning: {data.get('reasoning')}")
            if "Phi-3" in data["model"]:
                print("PASS: Routed to Phi-3")
            else:
                print(f"FAIL: Expected Phi-3, got {data['model']}")
        else:
            print(f"FAIL: Status {response.status_code}, {response.text}")

        # Test 2: Moderate Prompt (Expect Gemini)
        print("\nTest 2: Moderate Prompt")
        response = requests.post(f"{base_url}/route", json={"prompt": "Write a python function to reverse a string."})
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data}")
            if "Gemini" in data["model"]:
                print("PASS: Routed to Gemini")
            else:
                print(f"FAIL: Expected Gemini, got {data['model']}")
        else:
            print(f"FAIL: Status {response.status_code}, {response.text}")

        # Test 3: Complex Prompt (Expect GPT-4o)
        print("\nTest 3: Complex Prompt")
        long_prompt = "Explain quantum physics " * 50 # Make it long
        response = requests.post(f"{base_url}/route", json={"prompt": long_prompt})
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data}")
            if "GPT-4o" in data["model"]:
                print("PASS: Routed to GPT-4o")
            else:
                print(f"FAIL: Expected GPT-4o, got {data['model']}")
        else:
            print(f"FAIL: Status {response.status_code}, {response.text}")

        # Test 4: Stats
        print("\nTest 4: Stats")
        response = requests.get(f"{base_url}/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data}")
            if data["total_requests"] >= 3:
                print("PASS: Stats updated")
            else:
                print("FAIL: Stats not updated")
        else:
            print(f"FAIL: Status {response.status_code}, {response.text}")

    finally:
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    # Install dependencies first if needed, but assuming they are installed or we can install them
    # For this script, we assume requests is installed. If not, we can install it.
    try:
        import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests

    run_verification()
