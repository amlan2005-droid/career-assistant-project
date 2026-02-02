
import os
import time
import threading
from dotenv import load_dotenv
from app.services.gemini_client import ask_gemini

load_dotenv()

def fire_request(i):
    print(f"[{i}] Sending request...")
    start = time.time()
    response = ask_gemini(f"Write a 1-sentence joke about number {i}")
    duration = time.time() - start
    print(f"[{i}] Received in {duration:.2f}ks: {response[:50]}...")

def test_burst():
    print("--- Testing Burst Resilience (429 Mitigation) ---")
    print("This will send many requests quickly to trigger retries.")
    
    threads = []
    # Gemini free tier has ~15 RPM. 10 requests at once should trigger it if some are fast.
    for i in range(12):
        t = threading.Thread(target=fire_request, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.5) # Small stagger to not instantly die, but still bursty

    for t in threads:
        t.join()

    print("\n--- Burst Test Completed ---")

if __name__ == "__main__":
    test_burst()
