import requests
import time

# esp32 ip address
ESP32_IP = "http://192.168.12.209" 

def test_endpoints():
    print("--- Testing GET /health ---")
    response = requests.get(f"{ESP32_IP}/health")
    print(response.json())
    time.sleep(1)

    print("\n--- Testing GET /sensor ---")
    response = requests.get(f"{ESP32_IP}/sensor")
    print(response.json())
    time.sleep(1)

    print("\n--- Testing POST /config (Changing interval to 10 seconds) ---")
    new_settings = {"upload_interval": 10000, "encrypt_flag": False}
    response = requests.post(f"{ESP32_IP}/config", json=new_settings)
    print(response.json())
    time.sleep(1)

    print("\n--- Testing POST /push-now ---")
    response = requests.post(f"{ESP32_IP}/push-now")
    print(response.text)

if __name__ == "__main__":
    test_endpoints()