# DHT-mini-project-2
### Mini Project 2 Group G5

**By Sean Gupta & Elliott Eisele-Miller**

## Introduction

This project details the implementation of an environmental monitoring system using an ESP32 microcontroller and a Python Flask server. The ESP32 is used to read temperature and humidity data from a DHT11 sensor. This data is encrypted and transmitted over WiFi to the Flask server, where it is decrypted and displayed on a web dashboard. Additionally, the ESP32 is configured to act as a local web server. This provides a RESTful API that allows for remote configuration, system diagnostics, and direct data retrieval independent of the main Python server.

## Data Reading

The temperature and humidity data are read from the DHT11 sensor using the DHT library. The data readings are obtained only when they are needed for a request.

## WiFi Connectivity

WiFi connection is achieved using the WiFi library. The SSID and password are set using constant string variables. The WiFi connection is initiated using a function that makes the connection using the credentials and waits for the connection to complete. There is a WiFi reconnect logic function that will attempt to reconnect to the WiFi in the case of a lost connection.

## JSON Formatting

The JSON payload contains the keys of team number, temperature, humidity, and time stamp. The values for temperature, humidity, and time stamp are encrypted. The JSON is then turned into a string and sent via the http POST.

## Data Upload

The data is sent to the Python Flask server via http POST. Once received by the server, the JSON string is parsed by key value pairs. The values are decrypted and saved into local variables, then saved to the team data dictionary. The team data is then displayed to the web page.

## Data Encryption ESP32

The temperature, humidity, and timestamp data are encrypted using the AES ECB algorithm with a 16 bit key. The raw encrypted bytes are then encoded to a base64 string. Below is a sample of our encrypted data in the JSON payload.

**Payload:**

```json
{
  "team_number":"5",
  "temperature":"7MAMm8aVEoKeY3rqNCfUTg==",
  "humidity":"hXuW7Gu7QUAbAy+T5gjtYQ==",
  "timestamp":"k85WREW4J0FrO4kPyKjowA=="
}

```

## Data Decryption Python Flask Server

The base64 string is decoded and the raw bytes are decrypted using the AES ECB algorithm with a 16 bit key.

## RESTful API On ESP32

The ESP32 uses the built-in WebServer library to act as a local web server on port 80. This allows the board to handle RESTful API requests directly, separate from the Python Flask server. Four endpoints are implemented for this project:

* **GET /health** to check system diagnostics
* **GET /sensor** to retrieve the latest data directly
* **POST /config** to update device settings using a JSON payload
* **POST /push-now** to trigger an immediate data upload.

## Challenges Faced

Encryption and decryption presented a unique challenge. The main issues faced were deciding on which algorithm to use as well as the padding required to ensure the data length is 16 bits.

Additionally, implementing a C++ RESTful API on the ESP32 presented a significant challenge. Adapting standard web architecture concepts, such as HTTP routing and JSON deserialization, required integrating the WebServer and ArduinoJson libraries.

Merging the new API capabilities with the hardware logic from Mini Project 1 also introduced architectural complexity. The system required a fully non-blocking design using `millis()` timers so the board could continuously process incoming API requests without interrupting the DHT11 sensor's polling intervals.
