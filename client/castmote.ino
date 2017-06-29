#include <ESP8266WiFi.h>

WiFiClient client;

const uint8_t castbutton = D0;
const uint8_t successLED = D2;
const uint8_t errorLED = D1;

//variables for polling the button
uint8_t castState = HIGH;
uint32_t timeDelta = 0;

char response[4];

void setup() {
  //configre serial and gpio
  Serial.begin(115200);
  
  pinMode(successLED, OUTPUT);
  pinMode(errorLED, OUTPUT);

  digitalWrite(successLED, HIGH);
  digitalWrite(errorLED, HIGH);
  
  //setup and connect to wifi
  WiFi.begin("SSID", "PASSWORD");
  Serial.println("\nconnecting...");
  uint8_t timeout = 12;
  while(WiFi.status() != WL_CONNECTED){
    delay(1000);
    timeout --;
    Serial.print(".");
    if(timeout < 1){
      Serial.print("connection timed out");
      digitalWrite(D1, HIGH);
      while(true)
        ;
    }
  }
  Serial.println();
  Serial.println("connected!");
  Serial.println(WiFi.localIP());
  delay(1000);
  digitalWrite(successLED, LOW);
  digitalWrite(errorLED, LOW);
  Serial.println("ready");

  pinMode(castbutton, INPUT_PULLUP);
}

void loop() {
  //poll for button presses
  if(digitalRead(castbutton) == LOW && castState == HIGH){
    xwlbcast();
    castState = LOW;
  }
  else if(digitalRead(castbutton) == HIGH && millis() - timeDelta > 500){
    castState = HIGH;
    timeDelta = millis();
  }
}

void xwlbcast(){
  Serial.println("contacting server...");
  
  const char* host = "SERVER IP ADDRESS";
  //connect to server
  if(client.connect(host, SERVER PORT)){
    //send cast command
    Serial.println("sending cast command");
    client.println("xwlb");
    uint8_t charcount = 0;

    //expecting a 3 character response
    while(charcount < 3){
      if(client.available()){
        response[charcount] = client.read();
        charcount ++;
      }
    }
    response[3] = '\0';
    client.stop();

    Serial.print("response: ");
    Serial.println(response);
    //sucessful. blink green led
    if(strcmp(response, "200") == 0){
      Serial.println("success");
      for(uint8_t i = 0; i < 2; i ++){
        digitalWrite(successLED, HIGH);
        delay(500);
        digitalWrite(successLED, LOW);
        delay(500);
      }
    }
    //error. blink red led
    else{
      Serial.println("error");
      for(uint8_t i = 0; i < 10; i ++){
        digitalWrite(errorLED, HIGH);
        delay(100);
        digitalWrite(errorLED, LOW);
        delay(100);
      }
    }
  }
  //something went wrong. turn on red led
  else{
    Serial.println("failed to connect");
    digitalWrite(errorLED, HIGH);
    delay(5000);
    digitalWrite(errorLED, LOW);
  }
  Serial.println("finished communication");
}

