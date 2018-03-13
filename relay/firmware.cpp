// Including HTTP server library
#include <SPI.h>
#include <Ethernet.h>

// Including WiFi library
#include <WiFi.h>
#include <WiFiServer.h>
#include <WiFiClient.h>

// Including WiFi library
#include "lib/WiFiConnect/WiFiConnect.h"

// Set Relay pin (GPIO1/TXD01)
#define RelayPin 1

// Set Wi-Fi network credentials
char* ssid = "Rom";
const char* pass = "6766863000";

// Set initial relay status
int status = 0;

// Init server
EthernetServer server(80);

// Setup Wi-Fi and output pin
void setup() {
    Serial.begin(9600);
    InitWiFi(ssid, pass);
    server.begin();
    pinMode(RelayPin, OUTPUT);
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
        char* result = "{\"result\": 500, \"type\": \"relay\", \"message\": \"Failed to init relay\"}";

        // An http request ends with a blank line
        while (client.connected()) {
            if (client.available()) {
                char c = client.read();
                Serial.write(c);

                // If you've gotten to the end of the line (received a newline
                // character) and the line is blank, the http request has ended,
                // so you can send a reply
                if (c == '\n' && currentLineIsBlank) {
                    // Check relay

                    if (status == 0) {
                        status = 1;
                        digitalWrite(RelayPin, HIGH);
                        result = "{\"result\": 200, \"type\": \"relay\", \"status\": 1}";
                    } else {
                        status = 0;
                        digitalWrite(RelayPin, LOW);
                        result = "{\"result\": 200, \"type\": \"relay\", \"status\": 0}";
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
