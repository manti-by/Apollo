// Including HTTP server library
#include <SPI.h>
#include <Ethernet.h>

// Including WiFi library
#include <WiFi.h>
#include <WiFiServer.h>
#include <WiFiClient.h>

// Including the DHT and WiFi library
#include "lib/DHT/DHT.h"
#include "lib/WiFiConnect/WiFiConnect.h"

// Set DHT pin and type (AM2302)
#define DHTPin 5
#define DHTTYPE DHT22

// Set Wi-Fi network credentials
char* ssid = "Rom";
const char* pass = "6766863000";

// Init server, DHT sensor and serial port
EthernetServer server(80);
DHT dht(DHTPin, DHTTYPE);

// Setup Arduino
void setup() {
    Serial.begin(9600);
    InitWiFi(ssid, pass);
    dht.begin();
    server.begin();
}

// Run loop
void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        ConnectWiFi(ssid, pass);
    }

    EthernetClient client = server.available();
    if (client) {
        Serial.println("Client connected");

        boolean currentLineIsBlank = true;
        char result[128] = "{\"result\": 500, \"message\": \"Failed to read from DHT sensor\"}",
             h_str[32], t_str[32];
        float h, t;

        // An http request ends with a blank line
        while (client.connected()) {
            if (client.available()) {
                char c = client.read();
                Serial.write(c);

                // If you've gotten to the end of the line (received a newline
                // character) and the line is blank, the http request has ended,
                // so you can send a reply
                if (c == '\n' && currentLineIsBlank) {
                    h = dht.readHumidity();
                    t = dht.readTemperature();

                    if (!isnan(h) && !isnan(t)) {
                        dtostrf(h, 8, 2, h_str);
                        dtostrf(t, 8, 2, t_str);
                        sprintf(result, "{\"result\": 200, \"data\": {\"temperature\": %f, \"humidity\": %f}}",
                                h_str, t_str);
                    }

                    client.println("HTTP/1.1 200 OK");
                    client.println("Content-Type: application/json");
                    client.println("Connection: close");
                    client.println(result);
                    break;
                }

                if (c == '\n') {
                    // You're starting a new line
                    currentLineIsBlank = true;
                } else if (c != '\r') {
                    // You've gotten a character on the current line
                    currentLineIsBlank = false;
                }
            }
        }

        // Give the web browser time to receive the data
        delay(1000);
        client.stop();
        Serial.println("Client disconnected");
    }
}
