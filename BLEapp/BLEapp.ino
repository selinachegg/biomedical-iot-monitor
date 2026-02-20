#include <LBT.h>
#include <LBTClient.h>
  
void setup()
{
  Serial.begin(9600);
  bool success = LBTClient.begin();
  if( !success )
  {
      Serial.println("Cannot begin Bluetooth Client successfully");
      // Do nothing.
      while(true);
  }
  else
  {
      Serial.println("Bluetooth Client begins successfully");
      // start scan, at most scan 15 seconds
      int num = LBTClient.scan(15);
 
      if(num > 0)
      {
          LBTDeviceInfo info = {0};
          bool conn_result = LBTClient.connect("12:34:56:ab:cd:ef");//bool conn_result = LBTClient.connect("28:33:34:EE:24:95", "1234");
          if( !conn_result )
          {
              Serial.println("Cannot connect to SPP Server successfully");
              // Do nothing.
              while(true);
          }
          else
          {
             Serial.println("Connect to SPP Server successfully");
          }
      } 
  }
}
