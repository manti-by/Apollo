#include <WiFi.h>

#include "WiFiConnect.h"

void ConnectWiFi(char* ssid, const char* pass)
{
    Serial.println("Connecting to AP ...");
    int status = WiFi.status();

    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to WPA SSID: ");
        Serial.println(ssid);

        status = WiFi.begin(ssid, pass);
        delay(500);
    }

    Serial.println("Connected to AP");
}

void InitWiFi(char* ssid, const char* pass)
{
    // Check for the presence of the shield
    if (WiFi.status() == WL_NO_SHIELD) {
        Serial.println("WiFi shield not present");
        while(true);
    }

    ConnectWiFi(ssid, pass);
}