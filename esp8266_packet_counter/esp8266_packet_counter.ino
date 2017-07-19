#include <ESP8266WiFi.h>
extern "C" {
  #include "user_interface.h"
}

//===== Run-Time variables =====//
int ch = 1;
unsigned long prevTime = 0;
unsigned long pkts = 0;

void sniffer(uint8_t *buf, uint16_t len) {
  pkts++;
}

//===== SETUP =====//
void setup() {
  /* start Serial */
  Serial.begin(115200);

  /* setup wifi */
  wifi_set_opmode(STATION_MODE);
  wifi_set_promiscuous_rx_cb(sniffer);
  wifi_set_channel(ch);
  wifi_promiscuous_enable(1);
}

//===== LOOP =====//
void loop() {
  unsigned long curTime = millis();

  //every second
  if(curTime - prevTime >= 1000){
    prevTime = curTime;
    Serial.println((String)pkts);
    pkts = 0;
  }

  if(Serial.available()){
    ch = Serial.readString().toInt();
    if(ch < 1 || ch > 14) ch = 1;
     wifi_set_channel(ch);
  }
  
}
