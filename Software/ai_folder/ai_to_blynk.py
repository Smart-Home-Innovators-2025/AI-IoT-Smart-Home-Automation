# ai_to_blynk.py
# Reads V5 (gas), V6 (power), V7 (energy) for AI recommendations.

import requests
import time
import json

# Import the master AI function from our other file
from ai_engine import ai_master

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "{BLYNK_AUTH_TOKEN}" # Paste your token here
BLYNK_GET_URL = f"https://blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}"
BLYNK_UPDATE_URL = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}"

# --- HELPER FUNCTIONS ---
def blynk_get_value(pin):
    """Gets the raw value from a Blynk virtual pin and parses JSON response."""
    try:
        response = requests.get(f"{BLYNK_GET_URL}&{pin}")
        if response.status_code == 200:
            raw = response.text.strip()
            # Blynk API returns JSON array: ["value"]
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list) and len(parsed) > 0:
                    return str(parsed[0])
                return str(parsed)
            except (json.JSONDecodeError, IndexError):
                # Fallback: return raw string if parsing fails
                return raw
        else:
            print(f"Error getting {pin}: Status {response.status_code}")
            return "0"
    except requests.exceptions.RequestException as e:
        print(f"Error getting {pin}: {e}")
        return "0"

def blynk_send_report(report_string):
    """Sends the final report string to the V8 Terminal."""
    try:
        payload = {'v8': report_string}
        response = requests.get(BLYNK_UPDATE_URL, params=payload)
        print(f"✓ Report sent to Blynk V8. Response: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending to V8: {e}")
        return False


# --- MAIN SYSTEM MONITORING LOOP ---
# System generates and sends SMART HOME STATUS REPORT automatically every 30 seconds
# No trigger required - runs continuously and updates Blynk dashboard

print("\n╔════════════════════════════════════╗")
print("║   📊 SMART HOME DATA ENGINE 📊     ║")
print("║   (Auto-generating reports...)     ║")
print("╚════════════════════════════════════╝")
print("\n✅ Reports will be generated automatically every 30 seconds.\n")

report_interval = 10  # Generate report every 30 seconds
last_report_time = 0

while True:
    current_time = time.time()
    
    # Check if it's time to generate a new report
    if current_time - last_report_time >= report_interval:
        print("\n" + "="*40)
        print(f"  📡 Generating Report at {time.strftime('%H:%M:%S')}")
        print("  Fetching System Data...")
        print("="*40)
        
        # 1. Initialize data dictionary
        sensor_data = {}

        # 2. Fetch all sensor data from Blynk
        try:
            sensor_data['gas'] = int(blynk_get_value('v5'))
            sensor_data['power'] = float(blynk_get_value('v6'))
            sensor_data['energy_today'] = float(blynk_get_value('v7'))
        except ValueError as e:
            print(f"⚠️  Sensor Error: {e}")
            # Continue with defaults defined in ai_engine
        
        # 3. Generate formatted status report
        report = ai_master(sensor_data)
        
        # 4. Display report locally
        print(report)

        # 5. Send the report to Blynk V8
        if blynk_send_report(report):
            print("✓ Report successfully sent to Blynk V8")
            last_report_time = current_time
        else:
            print("⚠️  Failed to send report to Blynk V8")
    else:
        # System idle - waiting for next report generation
        remaining = int(report_interval - (current_time - last_report_time))
        print(f".", end="", flush=True)
    
    # Check every 2 seconds
    time.sleep(2)
