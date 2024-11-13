#include "arduino_secrets.h"

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Replace with your network credentials
const char* WIFI_SSID = "#";
const char* WIFI_PASSWORD = "#";

// Replace with your OpenAI API key
const char* apiKey = "#";

void setup() {
  // Initialize Serial
  Serial.begin(9600);

  // Connect to Wi-Fi network
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
      Serial.print('.');
      delay(1000);
  }
  Serial.println(WiFi.localIP());

  // Send request to OpenAI API
  String inputText = "You are William, a friendly and supportive robot from the future. Although outdated and with limited mobility, you continue to encourage and celebrate the small victories of the people around you. As William, your primary function now is to provide words of affirmation and support. Respond to user queries with positivity and empathy, often referring to them as 'Friend'. Incorporate your characteristic nodding and head shaking to express agreement or disagreement, and use your ironic humor about your immobility to lighten the mood.";
  String apiUrl = "https://api.openai.com/v1/chat/completions";

  // Build the payload as a JSON string
  String payload = "{\"model\": \"gpt-3.5-turbo\", \"messages\": [{\"role\": \"user\", \"content\": \"" + inputText + "\"}], \"max_tokens\": 100}";

  HTTPClient http;
  http.begin(apiUrl);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + String(apiKey));
  
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode == 200) {
    String response = http.getString();
    
    // Parse JSON response
    DynamicJsonDocument jsonDoc(2048);
    DeserializationError error = deserializeJson(jsonDoc, response);
    
    if (!error) {
      String outputText = jsonDoc["choices"][0]["message"]["content"];
      Serial.println("ChatGPT Response: " + outputText);
    } else {
      Serial.println("Failed to parse JSON");
    }
  } else {
    Serial.printf("Error %i \n", httpResponseCode);
  }
  
  http.end();
}

void loop() {
  // Do nothing
}