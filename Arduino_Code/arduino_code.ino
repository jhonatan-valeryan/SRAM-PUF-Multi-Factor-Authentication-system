#include <EEPROM.h>

const int ID_LENGTH = 16;
const int EEPROM_MARKER_ADDRESS = 0;
const int EEPROM_ID_ADDRESS = 1;
const byte VALID_MARKER = 0xA5;

byte deviceID[ID_LENGTH];

void setup() {
  Serial.begin(9600);

  loadOrCreateDeviceID();
}

void loop() {
  if (Serial.available() > 0) {
    String request = Serial.readStringUntil('\n');
    request.trim();

    if (request == "GET_PUF") {
      printDeviceID();
    }
  }
}

void loadOrCreateDeviceID() {
  // Check whether this board already has an ID.
  if (EEPROM.read(EEPROM_MARKER_ADDRESS) == VALID_MARKER) {
    loadDeviceID();
  } else {
    createDeviceID();
    saveDeviceID();
  }
}

void createDeviceID() {
  unsigned long seed = micros();

  /*
    Gather changing values from an unconnected analogue pin.
    Leave A0 unconnected while generating the ID.
  */
  for (int i = 0; i < 64; i++) {
    seed ^= ((unsigned long)analogRead(A0) << (i % 16));
    seed ^= micros();

    delayMicroseconds(137);
  }

  randomSeed(seed);

  for (int i = 0; i < ID_LENGTH; i++) {
    byte value = (byte)random(0, 256);

    /*
      Mix in more analogue and timing variation.
    */
    value ^= (byte)analogRead(A0);
    value ^= (byte)micros();

    deviceID[i] = value;

    delayMicroseconds(211);
  }
}

void saveDeviceID() {
  for (int i = 0; i < ID_LENGTH; i++) {
    EEPROM.update(EEPROM_ID_ADDRESS + i, deviceID[i]);
  }

  // Write the marker last so an incomplete write is not treated as valid.
  EEPROM.update(EEPROM_MARKER_ADDRESS, VALID_MARKER);
}

void loadDeviceID() {
  for (int i = 0; i < ID_LENGTH; i++) {
    deviceID[i] = EEPROM.read(EEPROM_ID_ADDRESS + i);
  }
}

void printDeviceID() {
  for (int i = 0; i < ID_LENGTH; i++) {
    if (deviceID[i] < 0x10) {
      Serial.print("0");
    }

    Serial.print(deviceID[i], HEX);
  }

  Serial.println();
}