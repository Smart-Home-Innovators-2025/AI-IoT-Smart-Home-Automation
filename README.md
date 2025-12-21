# Enhanced Edge IoT System for Hands-Free Control & Energy Monitoring

## 🚀 Project Overview
This project is an **AI-Integrated Smart Home Automation System** designed to prioritize safety, energy efficiency, and accessibility. It moves beyond traditional switching by integrating **Computer Vision (MediaPipe)** for contactless gesture control, **Real-time Energy Auditing (ACS712)**, and an **Active Safety System (MQ135)** that automatically ventilates the room during gas leaks.

All data is visualized locally on a **16x2 LCD** and remotely via the **Blynk IoT Cloud**, offering detailed analytics graphs (Power vs. Time, Gas vs. Time).

## 👥 Team Members
* **Atiksh Singh** - Computer Science & Engineering.
* **Arjun Singh** - Computer Science & Engineering.
* **Manish Nehra** - Computer Science & Engineering.
* **Rishabh Jain** - Computer Science & Engineering.

---

## 🛠️ Key Features
1.  **👋 Contactless Gesture Control:** * Uses a Laptop Webcam + Python (MediaPipe) to detect hand gestures.
    * **Open Palm:** Turns Appliance (LED) ON.
    * **Closed Fist:** Turns Appliance OFF.
2.  **⚡ Intelligent Energy Monitoring:**
    * Measures **Current (Amps)**, **Power (Watts)**, and **Cumulative Energy (Wh)** using the ACS712 sensor.
    * Helps users track consumption and prevent wastage.
3.  **🔥 Active Safety Response:**
    * Continuously monitors air quality using the **MQ135 Gas Sensor**.
    * **Trigger Condition:** If Gas Level > 2000 ppm.
    * **Action:** Immediately sounds a **Buzzer Alarm** AND activates a **DC Exhaust Fan** to ventilate the room.
4.  **📱 IoT Dashboard & Analytics:**
    * Live telemetry on the **Blynk Mobile App**.
    * Historical graphs for Current, Power, Energy, and Gas Levels.

---

## ⚙️ Hardware Tech Stack
* **Microcontroller:** ESP32 (DOIT DEVKIT V1)
* **Sensors:** MQ135 (Gas/Smoke Detection), ACS712 (Current/Power Monitoring)
* **Actuators:** DC Motor (Exhaust Fan), Piezo Buzzer, LED (Load).
* **Display:** 16x2 LCD with I2C Module.

## 💻 Software Tech Stack
* **Firmware:** C++ (Arduino IDE)
* **AI Engine:** Python 3.x, OpenCV, MediaPipe
* **IoT Cloud:** Blynk (HTTP API & Mobile App)

---

## 📸 System Architecture
*(Upload the Block Diagram image in `diagrams/` and link it here)*

---

## 🚀 How to Run the Project

### Step 1: Hardware Setup
Connect the components as per the circuit diagram found in `docs/`:
* **MQ135 (Analog):** Pin D34
* **ACS712 (Analog):** Pin D35
* **Buzzer + Fan:** Pin D19
* **LED (Load):** Pin D23
* **LCD (I2C):** SDA (D21), SCL (D22)

### Step 2: Firmware Upload
1.  Open `firmware/main_esp32_code.ino` in Arduino IDE.
2.  Install the required libraries: `Blynk`, `LiquidCrystal_I2C`, `WiFi`.
3.  Update the `BLYNK_AUTH_TOKEN`, `WIFI_SSID`, and `WIFI_PASS` in the code.
4.  Upload to your ESP32 board.

### Step 3: AI Gesture Script
1.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the script:
    ```bash
    python software/gesture_control.py
    ```
3.  Show your hand to the webcam to toggle the LED!

---

## 📊 Results
* **Latency:** Gesture commands are executed in under 2 seconds.
* **Safety:** The exhaust fan triggers automatically when gas levels exceed the threshold.
* **Accuracy:** The ACS712 sensor provides linear current readings calibrated to a zero-point of ~2.3V.

## 🔮 Future Scope
* Integration of multiple loads for complex gesture control.
* Automatic solenoid valve control to shut off gas supply during leaks.
* Short-circuit auto-cutoff protection.
