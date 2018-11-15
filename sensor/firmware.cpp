// Including libraries
#include <DHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Set DHT pin and type (AM2302)
#define DHTPin 5
#define DHTTYPE DHT22

// Init DHT sensor
DHT dht(DHTPin, DHTTYPE);


// Send HTTP request
void send(data) {
    HTTPClient http;
    char* server_url = "http://192.168.0.112/data=%s";

    Serial.print("Sending data: ");
    Serial.println(r);

    sprintf(server_url, data);

    WiFi.begin("Walhall", "0005925362");
    http.begin(completeURI);

    http.GET();
    http.end();
}


// Get DHT Sensor data
char* get_data() {
    char* r[16], h_str[8], t_str[8];

    Serial.println("Getting data");

    dht.begin();

    h = dht.readHumidity();
    dtostrf(t, 8, 2, t_str);

    t = dht.readTemperature();
    dtostrf(h, 8, 2, h_str);

    sprintf(r, "%f%f", t_str, h_str);

    return r;
}

// Get data and send to the server
void setup() {
    char* data[16];

    Serial.begin(115200);
    Serial.setTimeout(2000);

    // Wait for serial to initialize.
    while (!Serial) { }

    data = get_data();
    send_data(data);

    Serial.println("Entering to deep sleep");
    ESP.deepSleep(18e8);
}

// Run loop
void loop() {}
