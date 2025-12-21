# gesture_to_blynk.py
# This script controls an LED connected to an ESP32 via Blynk Cloud.
# - Shows webcam feed with hand tracking.
# - Counts fingers:
#   - 5 Fingers (Open Palm) -> Sends "LED_ON" to Blynk V9
#   - 0 or 1 Finger (Fist)  -> Sends "LED_OFF" to Blynk V9
# - Includes smoothing to prevent spamming the Blynk server.

import cv2
import mediapipe as mp
import requests
import time

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "{BLYNK_AUTH_TOKEN}"  # Paste your token here
BLYNK_VIRTUAL_PIN = "v9"
BLYNK_API_URL = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}"

# --- MEDIAPIPE HAND TRACKING SETUP ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Finger tip landmark IDs
tip_ids = [4, 8, 12, 16, 20]

# --- BLYNK COMMUNICATION ---
def send_to_blynk(command):
    """Sends the given command string to Blynk V9 with error handling."""
    try:
        url = f"{BLYNK_API_URL}&{BLYNK_VIRTUAL_PIN}={command}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✓ Sent '{command}' to Blynk.")
            return True
        else:
            print(f"⚠️  Blynk response {response.status_code} for '{command}'")
            return False
    except requests.exceptions.Timeout:
        print(f"⚠️  Timeout sending '{command}' to Blynk")
        return False
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error sending to Blynk: {e}")
        return False

# --- MAIN GESTURE DETECTION LOOP ---
cap = cv2.VideoCapture(0)  # 0 is the default webcam
last_command = ""          # For smoothing
last_sent_time = 0

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Failed to grab frame from webcam.")
        break

    # Flip the image horizontally for a natural, mirror-like view
    img = cv2.flip(img, 1)
    
    # Convert from BGR (OpenCV) to RGB (MediaPipe)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image and find hands
    results = hands.process(img_rgb)

    finger_count = 0
    status_text = "No Hand"
    command = ""

    if results.multi_hand_landmarks:
        # Get landmarks for the first hand detected
        hand_lms = results.multi_hand_landmarks[0]
        
        # Draw hand landmarks on the image
        mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

        # --- FINGER COUNTING LOGIC ---
        fingers = []
        landmarks = hand_lms.landmark

        # 1. Thumb
        # Check if thumb tip is to the left of the thumb's next joint
        # (This works because the image is flipped)
        if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # 2. Other 4 Fingers
        # Check if finger tip's y-coordinate is above the joint 2 landmarks down
        for id in range(1, 5):
            if landmarks[tip_ids[id]].y < landmarks[tip_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        finger_count = fingers.count(1)

        # --- COMMAND LOGIC ---
        if finger_count == 5:
            status_text = "LED ON"
            command = "LED_ON"
        elif finger_count <= 1:
            status_text = "LED OFF"
            command = "LED_OFF"
        else:
            status_text = "..."
            command = "" # No valid command

    # --- SMOOTHING & SENDING TO BLYNK ---
    # Only send a new command if it's different from the last one
    # AND at least 1 second has passed (prevents flickering)
    current_time = time.time()
    if command and command != last_command and (current_time - last_sent_time > 1):
        if send_to_blynk(command):
            last_command = command
            last_sent_time = current_time
    elif not command:
        last_command = "" # Reset if no valid gesture

    # --- DISPLAY INFO ON SCREEN ---
    cv2.putText(img, f"Fingers: {finger_count}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.putText(img, f"Status: {status_text}", (10, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Gesture Control - (Press 'q' to quit)", img)
    
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q') or key == 27:  # 'q' or ESC to quit
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()
