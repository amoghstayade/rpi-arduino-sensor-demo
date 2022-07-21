#include <dht.h>
#include <LiquidCrystal.h>

dht DHT;
#define DHT11_PIN 7

String temp_humidity_light_string = "";

// lcd screen pins
const int rs=12, en=11, d4=5, d5=4, d6=3, d7=2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

int ledPin = 6;
int pushButton = 8;

int ledState = HIGH;         // the current state of the output pin
int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin
String buttonStateString = "ON";

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers



void setup(){
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(pushButton, INPUT);
  lcd.begin(16,2);
  lcd.print("Hello, world!");
  delay(1000);
  lcd.setCursor(0, 0);
  lcd.print("Temp | Hmd | Lt");
  digitalWrite(ledPin, ledState);
}

void loop(){
  //push bubtton debounce code
  int reading = digitalRead(pushButton);

  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (buttonState == HIGH) {
        ledState = !ledState;
      }
    }
  }
  
  digitalWrite(ledPin, ledState);
  lastButtonState = reading;
  
  if (ledState == HIGH) {
    buttonStateString = "ON ";
  } else {
    buttonStateString = "OFF";
  }

  // Code for DHT sensor check
  int chk = DHT.read11(DHT11_PIN);
  lcd.setCursor(0, 1);
  // Write to the lcd screen
  lcd.print(temp_humidity_light_string);
  // TODO: add sampling logic here
  temp_humidity_light_string = String(int(DHT.temperature)) + (char)223 + "C" + " | " + String(int(DHT.humidity)) + "% | " + buttonStateString;
  Serial.println("Temperature:" + String(int(DHT.temperature)) + ",Humidity:" + String(int(DHT.humidity)) + ",Light:" + buttonStateString);
  delay(50);
}
