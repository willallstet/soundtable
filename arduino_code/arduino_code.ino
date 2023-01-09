#include <Wire.h>
#include "Adafruit_MPR121.h"

Adafruit_MPR121 cap_sense = Adafruit_MPR121();

#define MPR121_ADDR 0x5A
#define PRINT_DELAY 2000
//uint16_t oldVals[12];
void setup()
{
    Serial.begin(115200);
    cap_sense.begin(MPR121_ADDR);
    
    //attachInterrupt(digitalPinToInterrupt(2), resetFunc, FALLING);
    //Serial.println("Ready to sense");*/
}
void(* resetFunc) (void) = 0; //declare reset function at address 0 - MUST BE ABOVE LOOP

void loop()
{
    sense();
    delay(200);
}

void sense()
{
  String output = String(String(cap_sense.filteredData(0)) + "," + String(cap_sense.filteredData(1)) + "," + String(cap_sense.filteredData(2)) + "," + String(cap_sense.filteredData(3)) + "," + String(cap_sense.filteredData(4)) + "," + String(cap_sense.filteredData(5)) + "," + String(cap_sense.filteredData(6)) + "," + String(cap_sense.filteredData(7)) + "," + String(cap_sense.filteredData(8)) + "," + String(cap_sense.filteredData(9)) + "," + String(cap_sense.filteredData(10)) + "," + String(cap_sense.filteredData(11)));
  Serial.println(output);
    
}
