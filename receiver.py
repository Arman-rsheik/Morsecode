import cv2
import numpy as np
import time

# --- CONFIGURATION ---
# This is the "Sensitivity". 
# If the camera sees brightness > 150, it thinks the LED is ON.
THRESHOLD = 150 
DOT_TIME = 0.4  # Max duration of a dot (in seconds)

# Morse Code Dictionary
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9'
}

cap = cv2.VideoCapture(0)

# State Variables
is_led_on = False
start_time = 0
current_symbol = ""
decoded_message = ""
last_signal_time = time.time()

print("Point webcam at the LED. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret: break

    # 1. SETUP REGION OF INTEREST (The Green Box)
    height, width, _ = frame.shape
    # We look at a 50x50 pixel box in the center of the screen
    y1, y2 = height//2 - 25, height//2 + 25
    x1, x2 = width//2 - 25, width//2 + 25
    roi = frame[y1:y2, x1:x2]

    # 2. CALCULATE BRIGHTNESS
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray_roi)

    # 3. DETECT ON/OFF
    led_state = avg_brightness > THRESHOLD

    # 4. DECODING LOGIC
    current_time = time.time()

    if led_state and not is_led_on:
        # LED turned ON
        is_led_on = True
        start_time = current_time
        
        # Check for gap (Space between letters)
        silence = current_time - last_signal_time
        if silence > 1.0: # If silence was long, decode the previous letter
            if current_symbol in MORSE_CODE_DICT:
                char = MORSE_CODE_DICT[current_symbol]
                decoded_message += char
            elif silence > 2.5: # Very long silence = Space
                decoded_message += " "
            current_symbol = ""

    elif not led_state and is_led_on:
        # LED turned OFF
        is_led_on = False
        duration = current_time - start_time
        last_signal_time = current_time
        
        # Decide if Dot or Dash
        if duration < DOT_TIME:
            current_symbol += "."
        else:
            current_symbol += "-"

    # 5. DRAW INTERFACE
    # Color the box Green if ON, Red if OFF
    box_color = (0, 255, 0) if led_state else (0, 0, 255)
    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
    
    # Display Info
    cv2.putText(frame, f"Bright: {int(avg_brightness)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, f"Code: {current_symbol}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Msg: {decoded_message}", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    cv2.imshow("Receiver", frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()python receiver.py
