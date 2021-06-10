#include "Adafruit_Thermal.h"
#include "adalogo.h"
#include "adaqrcode.h"
#include "SoftwareSerial.h"
#define TX_PIN 6 // Arduino transmit  groen WIRE  labeled RX on printer
#define RX_PIN 7 // Arduino receive   geel WIRE   labeled TX on printer
SoftwareSerial mySerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);     // Pass addr to printer constructor
String inBytes;
String func = "0";
int motor1Pin = 2;
int motor2Pin = 3;
int motor3Pin = 4;
int motor4Pin = 5;
int counter1 = 0;
int counter2 = 0;
int laststate1 = HIGH;
int laststate2 = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(motor1Pin, OUTPUT);
  pinMode(motor2Pin, OUTPUT);
  pinMode(motor3Pin, OUTPUT);
  pinMode(motor4Pin, OUTPUT);
  
}

void loop() {
  inBytes = Serial.readStringUntil('\n');
  String func = inBytes;
  func.remove(1,100);
  inBytes.remove(0,1);
  if(func == "1") {
  dispense();
  }
  
  if(func == "2"){
    printen();
  }
}

void printen(){
  pinMode(7, OUTPUT); digitalWrite(7, LOW);
      String tijd = inBytes;
      String bedrag = inBytes;
      String iban = inBytes;
      tijd.remove(19,100);
      iban.remove(35,100);
      iban.remove(0,31);
      bedrag.remove(0, 35);
      mySerial.begin(9600);  
      printer.begin();        
      printer.justify('C');
      printer.setSize('L'); 
      printer.inverseOn();   
      printer.println(F("NIBA"));
      printer.inverseOff();
      printer.setSize('M');
      printer.println(F("-------------------------"));
      printer.setSize('S');
      printer.justify('L');
      printer.print(F("Datum: "));
      printer.println(tijd);
      printer.print(F("IBAN: **** **** **** "));
      printer.println(iban);
      printer.print(F("Bedrag: "));
      printer.println(bedrag);
      printer.justify('C');
      printer.setSize('M');
      printer.println(F("-------------------------"));
      printer.feed(2);
      printer.sleep();      // Tell printer to sleep
      delay(3000L);         // Sleep for 3 seconds
      printer.wake();       // MUST wake() before printing again, even if reset
      printer.setDefault(); // Restore printer to defaults
      func = "0";
}

void dispense(){
    String aantal1Str = inBytes;
    aantal1Str.remove(1,100);
    String aantal2Str = inBytes;
    aantal2Str.remove(0,1);
    int aantal1 = aantal1Str.toInt();
    int aantal2 = aantal2Str.toInt();
  while (true)
  {
    int state1 = digitalRead(8);
    int state2 = digitalRead(9);

   if (state1 != laststate1){
    laststate1 = state1;
    counter1++;
   }

   else if (state2 != laststate2){
    laststate2 = state2;
    counter2++;
   }

   if (counter1 < aantal1*2){
    digitalWrite(motor2Pin, HIGH);
   }

    else{
    digitalWrite(motor2Pin, LOW);
   }

   if (counter2 < aantal2*2){
    digitalWrite(motor4Pin, HIGH);
   }
    else{
    digitalWrite(motor4Pin, LOW);
    }

  }
  func = "0";
}
