// Including WiFi library
#include <WiFiUdp.h>
#include <WiFi.h>
#include <WiFiServer.h>
#include <WiFiClient.h>

// Including HTTP server library
#include <EthernetServer.h>
#include <Dns.h>
#include <Ethernet.h>
#include <EthernetClient.h>
#include <EthernetUdp.h>
#include <Dhcp.h>

// Including the DHT and WiFi library
#include <DHT_U.h>
#include <DHT.h>

// Set DHT pin and type (AM2302)
#define DHTPin 5
#define DHTTYPE DHT22

// Set Wi-Fi network credentials
#define SSID "Rom"
#define PASS "6766863000"

// Init server, DHT sensor and serial port
EthernetServer server(80);
DHT dht(DHTPin, DHTTYPE);


// Setup Arduino
void setup(void) {
    Serial.begin(9600);
    InitWiFi();
    dht.begin();
    server.begin();
}


// Run loop
void loop(void) {
    if (WiFi.status() != WL_CONNECTED) {
        ConnectWiFi();
    }

    EthernetClient client = server.available();
    if (client) {
        Serial.println("Client connected");

        boolean currentLineIsBlank = true;
        String result = "";
        float humidity = 0;
        float temperature = 0;

        // An http request ends with a blank line
        while (client.connected()) {
            if (client.available()) {
                char c = client.read();
                Serial.write(c);

                // If you've gotten to the end of the line (received a newline
                // character) and the line is blank, the http request has ended,
                // so you can send a reply
                if (c == '\n' && currentLineIsBlank) {
                    humidity = dht.readHumidity();
                    temperature = dht.readTemperature();

                    if (isnan(humidity) || isnan(temperature)) {
                        result = "{\"result\": 500, \"message\": \"Failed to read from DHT sensor\"}";
                    } else {
                        result = String("{\"result\": 200, \"data\": {\"temperature\": ") + humidity + ", \"humidity\": " + temperature + "}}";
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

void InitWiFi()
{
    // Check for the presence of the shield
    if (WiFi.status() == WL_NO_SHIELD) {
        Serial.println("WiFi shield not present");
        while(true);
    }

    ConnectWiFi();
}

void ConnectWiFi()
{
    Serial.println("Connecting to AP ...");
    int status = WiFi.status();

    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to WPA SSID: ");
        Serial.println(SSID);

        status = WiFi.begin(SSID, PASS);
        delay(500);
    }

    Serial.println("Connected to AP");
}
