#include <Arduino.h>

// --- SUPER ACCURATE SLOW TIMINGS ---
// Dot = 0.6 seconds
// Dash = 1.8 seconds
const int DOT = 600;
const int DASH = 1800;
const int GAP = 600;           // Gap between symbols
const int LETTER_GAP = 1800;   // Gap between letters
const int WORD_GAP = 4200;     // Gap between words
const int LED = 13;

// --- MORSE TABLE ---
const char* letters[] = {
  ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", 
  "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", 
  "..-", "...-", ".--", "-..-", "-.--", "--.."
};
const char* numbers[] = {
  "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----."
};

void dot() { digitalWrite(LED, HIGH); delay(DOT); digitalWrite(LED, LOW); delay(GAP); }
void dash() { digitalWrite(LED, HIGH); delay(DASH); digitalWrite(LED, LOW); delay(GAP); }

void sendChar(char c) {
  const char* pattern = "";
  if (c >= 'a' && c <= 'z') c -= 32; 
  if (c >= 'A' && c <= 'Z') pattern = letters[c - 'A'];
  else if (c >= '0' && c <= '9') pattern = numbers[c - '0'];
  else if (c == ' ') { delay(WORD_GAP - LETTER_GAP); return; }
  else return; 

  for (int i=0; pattern[i] != '\0'; i++) {
    if (pattern[i] == '.') dot();
    else if (pattern[i] == '-') dash();
  }
  delay(LETTER_GAP - GAP);
}

void setup() { pinMode(LED, OUTPUT); }

void loop() {
  // MESSAGE TO SEND
  String message = "HELLO WORLD"; 
  
  for (int i = 0; i < message.length(); i++) {
    sendChar(message[i]);
  }
  delay(5000); // Long wait before repeating
}