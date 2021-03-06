#include <OneWire.h>
#include <DallasTemperature.h>

/********************************************************************/
// Data wire is plugged into pin 2 on the Arduino 
#define ONE_WIRE_BUS 2 
/********************************************************************/
// Setup a oneWire instance to communicate with any OneWire devices  
// (not just Maxim/Dallas temperature ICs) 
OneWire oneWire(ONE_WIRE_BUS); 
/********************************************************************/
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);
/********************************************************************/
// Setup variables
int which_line = 0; 
void setup(void) 
{ 
 // start serial port 
 Serial.begin(9600); 
 Serial.println("Testing temp by request"); 
 // Start up the library 
 sensors.begin(); 
} 
void loop(void) 
{ 
  // call sensors.requestTemperatures() to issue a global temperature 
  // request to all devices on the bus  
  /********************************************************************/
  // Wait to ask for something
  if (Serial.available()>0) {
    which_line = Serial.parseInt();
    sensors.requestTemperatures(); // Send the command to get temperature readings 
    /********************************************************************/
    Serial.print(which_line, "DEC");
    Serial.print("=");
    Serial.print(sensors.getTempCByIndex(which_line)); // Why "byIndex"?  
      // You can have more than one DS18B20 on the same bus.  
      // 0 refers to the first IC on the wire 
    Serial.println("");
    delay(10);
  }
}
