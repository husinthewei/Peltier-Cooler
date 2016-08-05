#include <DHT.h>


void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(100);
  float h = dht.readHumidity();
  Serial.print(dht.readTemperature());
  Serial.print("  ");
  Serial.println(h);
  
}
