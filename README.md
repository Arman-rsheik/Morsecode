# Optical Morse Code Communication System 📡💡

## 📖 Overview
This project implements a complete **wireless optical communication system** that transmits text messages using Morse code through LED blinks and decodes them back to text using Computer Vision (OpenCV).

Unlike traditional RF communication, this system uses visible light (VLC). The transmitter is powered by an **Arduino Uno** (programmed via Android), and the receiver is a **Python-based Computer Vision engine** that detects light pulses via a standard webcam, filters noise, and decodes the message in real-time.

![Result Demo](https://via.placeholder.com/800x400?text=Project+Demo+Image+Here)
*(Replace above link with an actual screenshot of your "HELLO WORLD" result if available)*

## ✨ Key Features
*   **Computer Vision Decoder:** Uses OpenCV to detect LED brightness within a dynamic Region of Interest (ROI).
*   **Adaptive Calibration:** Two-stage calibration system (Dark/Bright) to handle different lighting environments.
*   **Robust Timing:** Implements a "Slow Morse" standard (600ms unit) to ensure stability against webcam frame rate jitter.
*   **Mobile-First Firmware:** Arduino firmware developed and flashed using **Android (Termux + PlatformIO)**.
*   **Noise Filtering:** Gaussian blur and temporal filtering to reject flashes shorter than 200ms.
*   **Real-Time Feedback:** Live GUI showing the detected ROI, current signal state (ON/OFF), and decoded text.

## 🛠️ Tech Stack

### Hardware
*   **Transmitter:** Arduino Uno, LED (Pin 13).
*   **Receiver:** Laptop with built-in or USB Webcam.
*   **Dev Station:** Android Smartphone (for compiling firmware).

### Software
*   **Receiver Logic:** Python 3.8+, OpenCV 4.5+, NumPy, Tkinter/PyQt5.
*   **Transmitter Logic:** C++ (Arduino Framework).
*   **Tools:** PlatformIO CLI (running on Termux via Debian proot).

## ⚙️ Algorithms & Protocol
The system follows the **ITU-R M.1677-1** Morse Code standard but scaled for optical reliability:

| Signal Element | Ratio | Duration (ms) |
| :--- | :--- | :--- |
| **Dot** | 1 unit | 600 ms |
| **Dash** | 3 units | 1800 ms |
| **Intra-char Gap** | 1 unit | 600 ms |
| **Letter Gap** | 3 units | 1800 ms |
| **Word Gap** | 7 units | 4200 ms |

**Detection Logic:**
The Python receiver analyzes a 150x150 pixel center crop of the video feed. It calculates a dynamic threshold based on calibration:
`Threshold = (Calibrated_Dark_Level + Calibrated_Bright_Level) / 2`
https://github.com/user-attachments/assets/ec9fa47d-7c04-474a-9bc7-c579e547bb04
## 🚀 Installation & Setup

### Prerequisites
Ensure you have Python installed. Then install the required libraries:
```bash
pip install opencv-python numpy
1. The Transmitter (Arduino)
Connect your LED to Pin 13 and GND.
Upload the firmware code (located in the transmitter folder) to your Arduino.
Note: As per our methodology, this was compiled using PlatformIO on Android, but standard Arduino IDE works fine too.
2. The Receiver (Python)
Clone this repository:
code
Bash
git clone https://github.com/Arman-rsheik/Morsecode.git
cd Morsecode
Run the receiver script:
code
Bash
python receiver.py
🎮 How to Use (Calibration Guide)
The system uses a Space Bar state machine for setup. Follow these steps strictly for best results:
Step 1: Dark Calibration
Run the Python script. The terminal will say STEP 1: DARK.
Cover the LED or ensure it is turned OFF.
Press the SPACE BAR. The system records ambient light levels.
Step 2: Bright Calibration
The terminal will say STEP 2: FLASH.
Turn the LED ON (continuously).
Press the SPACE BAR. The system records the max brightness.
Step 3: Running Mode
The system enters RUNNING mode.
Start your Morse Code transmission on the Arduino.
Watch the terminal/GUI as the message decodes in real-time!
📊 Performance
Accuracy: 95% in normal indoor lighting.
Latency: Letter decoding occurs 1.5s after the sequence finishes.
Reliability: Successfully tested with the string "HELLO WORLD" and complex punctuation.
📂 Project Structure
code
Code
Morsecode/
├── receiver.py         # Main computer vision & decoding logic
├── transfer.py         # (Optional) Helper utilities or alternative logic
├── transmitter/        # Arduino firmware code
│   └── src/main.cpp
├── README.md           # This file
└── .gitignore

