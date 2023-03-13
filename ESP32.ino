////////////  edit these values for each sensor 
const char* ssid       = "SSIDnameHere";     // your network SSID (name of wifi network)
const char* password   = "123123123"; // your network password
const char* udpAddress = "192.168.1.100";  // your syslog server destination IP
/////////// no edits below this line unless you know what you are doing
#include <OneWire.h> 
#include <DallasTemperature.h>
#include <WiFiClientSecure.h>
#define tempPin0 14
#define WDT_TIMEOUT 30
OneWire oneWire0(tempPin0); 
DallasTemperature sensor0(&oneWire0);
int i=0;int last = millis();
const int udpPort = 3333;  
boolean connected = false; 
WiFiUDP udp; 

void setup() {
 //Initialize serial and wait for port to open:
 Serial.begin(115200);
 delay(100);
 sensor0.begin(); 

  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  connectToWiFi(ssid, password);
  // attempt to connect to Wifi network:
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("My IP is: "); 
  Serial.println(WiFi.localIP());
  
  Serial.println("Configuring WDT...");
  esp_task_wdt_init(WDT_TIMEOUT, true); //enable panic so ESP32 restarts
  esp_task_wdt_add(NULL); //add current thread to WDT watch
}
void(* resetFunc) (void) = 0; //declare reset function at address 0 - MUST BE ABOVE LOOP

void loop() {
Serial.print("millis() = ");Serial.println(String( millis() ) );
if(millis() > 3600000 )resetFunc();

sensor0.requestTemperatures();  // send command 
float temp0C = sensor0.getTempCByIndex(0);
float temp0F = (temp0C*9/5) + 32;
 Serial.print("Temperature #0 is: "); 
 Serial.print(temp0C);
 Serial.print(" C / "); 
 Serial.print(temp0F);
 Serial.println(" F"); 
 String mydata = String(temp0F) + " " + location;
 Serial.print("sending packet: '"); 
 Serial.print(mydata); 
 Serial.println("'"); 


// send to listening server
if(connected){
    //Send a packet
    udp.beginPacket(udpAddress,udpPort);
    udp.print(mydata);
    udp.endPacket();
  }
else{
 resetFunc();  // RESET IF DISCONNECTED
}

 delay(5000); 
 esp_task_wdt_reset();
}

void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));
  WiFi.disconnect(true);
  WiFi.onEvent(WiFiEvent);
  WiFi.begin(ssid, password);
  Serial.println("Waiting for WIFI connection...");
}
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case ARDUINO_EVENT_WIFI_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
          udp.begin(WiFi.localIP(),udpPort);
          connected = true;
          break;
      case ARDUINO_EVENT_WIFI_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;
          break;
      default: break;
    }
}
