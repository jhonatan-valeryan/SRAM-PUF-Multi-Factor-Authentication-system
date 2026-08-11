# SRAM PUF Multi-Factor Authentication System

A hardware-based multi-factor authentication (MFA) prototype developed using **Python** and an **Arduino UNO R3**.

The system combines password-based authentication with a hardware authentication factor. During registration, a device identifier obtained from the Arduino is associated with the user's account. During login, both the user's password and the connected Arduino device must be successfully verified before access is granted.

## Project Overview

Traditional username and password authentication relies only on something the user knows. If the password is compromised, an unauthorized user may be able to access the account.

This project adds a second authentication factor using an Arduino UNO R3 as a hardware device.

The authentication process consists of:

1. **Password Authentication** — The user's password is hashed using SHA-256 and compared with the stored password hash.
2. **Hardware Authentication** — The Python application communicates with the connected Arduino through a serial connection and retrieves its device identifier.
3. **Multi-Factor Verification** — Access is granted only when both the password and hardware device match the information registered to the user.

This demonstrates the concept of combining:

- **Something the user knows** — password
- **Something the user possesses** — registered Arduino device

---

## Features

- User registration and login
- Password confirmation during registration
- SHA-256 password hashing
- CSV-based user database
- Automatic detection of available serial ports
- Interactive Arduino COM-port selection
- Python-to-Arduino serial communication
- Hardware device enrolment during registration
- Hardware-based second-factor authentication
- Detection of an unregistered Arduino device
- Multi-factor authentication success and failure handling
- Persistent hardware identifier provided by the Arduino

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main authentication application |
| Arduino C/C++ | Arduino firmware |
| Arduino UNO R3 | Hardware authentication device |
| PySerial | Communication between Python and Arduino |
| SHA-256 | Password hashing |
| CSV | User credential and device information storage |
| EEPROM | Persistent Arduino device identifier storage |
| Serial Communication | Communication between the computer and Arduino |

---

## Project Structure

```text
sram-puf-mfa-authentication/
│
├── src/
│   ├── python/
│   │   └── authentication_system.py
│   │
│   └── arduino/
│       └── sram_puf_device.ino
│
├── screenshots/
│   ├── registration-port-selection.jpeg
│   ├── registration-process.jpeg
│   ├── login-success.jpeg
│   └── login-failed.jpeg
│
├── sample/
│   └── database_sample.csv
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## How the System Works

### Registration

During registration:

1. The user selects that they have not registered before.
2. The user creates a username.
3. The user creates and confirms a password.
4. The Python application detects available serial ports.
5. The user selects the COM port associated with the Arduino UNO.
6. Python opens a serial connection with the Arduino.
7. The application sends a `GET_PUF` request to the Arduino.
8. The Arduino returns its device identifier.
9. The password is hashed using SHA-256.
10. The username, password hash, and hardware identifier are stored in the CSV database.

Conceptually:

```text
User
  │
  ├── Username
  │
  ├── Password
  │      │
  │      ▼
  │   SHA-256
  │      │
  │      ▼
  │ Password Hash
  │
  └── Arduino UNO
          │
          ▼
      Device ID
          │
          ▼
     database.csv
```

---

### Login

During login:

1. The user enters their username and password.
2. The password is hashed using SHA-256.
3. The generated hash is compared with the stored password hash.
4. If the password is correct, the first authentication factor succeeds.
5. The application asks the user to connect the registered Arduino.
6. The available serial ports are displayed.
7. The user selects the Arduino COM port.
8. Python requests the device identifier from the Arduino.
9. The returned identifier is compared with the identifier registered to the user.
10. Access is granted only when the hardware identifiers match.

The authentication process can be represented as:

```text
          LOGIN
            │
            ▼
    Username + Password
            │
            ▼
      Hash Password
            │
            ▼
     Password Correct?
        /         \
      No           Yes
      │             │
      ▼             ▼
 Access Denied   Arduino Check
                    │
                    ▼
               Read Device ID
                    │
                    ▼
             Device ID Match?
                /       \
              No         Yes
              │           │
              ▼           ▼
         Access Denied   MFA
                       Successful
```

---

## Arduino Communication

The Python application communicates with the Arduino through a serial connection at:

```text
9600 baud
```

The application sends:

```text
GET_PUF
```

to request the hardware identifier from the Arduino.

The Arduino returns its device identifier through the serial connection.

Python then compares the received identifier with the identifier stored during user registration.

The serial connection uses **PySerial** with a timeout of **5 seconds**.

---

## Demonstration

### 1. User Registration and Arduino Selection

The user creates a username and password and then connects the Arduino UNO R3.

The application automatically detects the available serial ports and allows the user to select the port associated with the Arduino.

![Registration and Arduino Port Selection](screenshots/registration-port-selection.jpeg)

---

### 2. Successful Hardware Registration

After the correct Arduino serial port is selected, the Python application requests the device identifier.

The returned identifier is associated with the user's account and registration is completed successfully.

![Successful Hardware Registration](screenshots/registration-process.jpeg)

---

### 3. Successful Multi-Factor Authentication

During login, the correct username and password successfully complete the first authentication factor.

The registered Arduino is then connected as the second authentication factor. When the detected device identifier matches the registered identifier, multi-factor authentication succeeds and access is granted.

![Successful Multi-Factor Authentication](screenshots/login-success.jpeg)

---

### 4. Authentication Failure with a Different Device

The system was also tested using a different Arduino device.

In this test, the username and password are correct, meaning password authentication succeeds. However, the identifier returned by the connected Arduino does not match the identifier registered to the account.

The hardware authentication therefore fails and access is denied.

![Failed Authentication with Different Device](screenshots/login-failed.jpeg)

This demonstrates that possession of the registered hardware device is required in addition to knowing the correct password.

---

## Installation

### Prerequisites

To run this project, you need:

- Python 3
- Arduino IDE
- Arduino UNO R3
- USB cable
- PySerial
- A computer with an available USB/serial connection

---

### 1. Clone the Repository

```bash
git clone https://github.com/jhonatan-valeryan/sram-puf-mfa-authentication.git
```

Then navigate to the repository:

```bash
cd sram-puf-mfa-authentication
```

### 2. Install Python Dependencies

Install the required Python package using:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
pyserial>=3.5
```

Alternatively, PySerial can be installed directly:

```bash
pip install pyserial
```

---

## Arduino Setup

1. Connect the Arduino UNO R3 to the computer using USB.
2. Open:

```text
src/arduino/sram_puf_device.ino
```

in the Arduino IDE.

3. Select:

```text
Tools → Board → Arduino Uno
```

4. Select the correct COM port.
5. Upload the Arduino program.
6. Close the Arduino Serial Monitor before starting the Python application.

> The Arduino Serial Monitor should be closed because the Python application needs access to the same serial port.

---

## Running the Python Application

Navigate to:

```bash
cd src/python
```

Run:

```bash
python authentication_system.py
```

The program will ask:

```text
Have you registered before? (yes/no):
```

Enter:

```text
no
```

to create a new account.

Enter:

```text
yes
```

to log in using an existing account.

---

## User Database

The application stores registered users in:

```text
database.csv
```

The database contains:

```text
username,password,puf_id
```

For example:

```text
username,password,puf_id
sampleuser,<hashed-password>,<device-identifier>
```

The real `database.csv` file is excluded from this repository through `.gitignore` because it may contain authentication information.

A demonstration file is provided instead:

```text
sample/database_sample.csv
```

---

## Security Design

### Password Hashing

Passwords are not stored directly as plaintext in the database.

The Python application hashes passwords using:

```python
hashlib.sha256(password.encode()).hexdigest()
```

During login, the entered password is hashed again and compared with the stored hash.

---

### Hardware Authentication

After successful password authentication, the system requires the registered Arduino hardware device.

The application:

```text
Python
   │
   │ GET_PUF
   ▼
Arduino UNO
   │
   │ Device Identifier
   ▼
Python
   │
   ▼
Compare with Registered Identifier
```

If the identifiers match:

```text
MULTI-FACTOR AUTHENTICATION SUCCESS
```

If they do not match:

```text
SRAM PUF AUTHENTICATION FAILED
Unknown Device Detected!
Access Denied.
```

---

## Authentication Scenarios

| Password | Hardware Device | Result |
|---|---|---|
| Correct | Registered device | Authentication successful |
| Correct | Different device | Access denied |
| Incorrect | Registered device | Access denied |
| Incorrect | Different device | Access denied |

Both authentication factors must therefore be successfully verified before access is granted.

---

## Security Limitations

This project was developed as an educational prototype and is **not intended for production use**.

Several security limitations should be considered:

### 1. SHA-256 Password Hashing

The current implementation uses SHA-256 directly for password hashing.

Although this prevents plaintext passwords from being stored, general-purpose SHA-256 is not ideal for production password storage because it is designed to be computationally fast.

Production systems should use dedicated password hashing algorithms such as:

- Argon2
- bcrypt
- scrypt

with appropriate salts and security parameters.

### 2. CSV Database

User authentication information is stored in a CSV file.

A production authentication system should use a properly secured database with appropriate access controls and encryption where necessary.

### 3. Hardware Identifier Security

The current prototype uses a persistent hardware identifier for device verification.

If an attacker can extract and reproduce the identifier, the hardware factor could potentially be cloned.

A stronger implementation could use challenge-response authentication instead of transmitting and directly comparing a static identifier.

### 4. Serial Communication

Communication between the Python application and Arduino is not encrypted.

A production implementation would require stronger protection against interception, replay, and device impersonation.

### 5. SRAM PUF Implementation

The project demonstrates an SRAM PUF-inspired hardware authentication concept. The current prototype should not be considered a complete production-grade Physical Unclonable Function implementation.

A more advanced implementation could directly characterize SRAM startup behaviour and use error correction or fuzzy extraction techniques to reconstruct stable cryptographic information from noisy PUF responses.

---

## Future Improvements

Possible improvements include:

- Replace SHA-256 password hashing with Argon2 or bcrypt
- Add unique password salts
- Replace CSV storage with a secure database
- Implement account lockout after repeated failed login attempts
- Add authentication attempt logging
- Implement challenge-response hardware authentication
- Protect against replay attacks
- Encrypt sensitive communication
- Add error-tolerant PUF reconstruction
- Improve automatic Arduino detection
- Add a graphical user interface
- Implement user account management
- Add password reset functionality

---

## Learning Outcomes

Through this project, I gained practical experience with:

- Multi-factor authentication concepts
- Hardware-based authentication
- Python application development
- Arduino programming
- Serial communication between software and hardware
- Password hashing
- Authentication system design
- CSV data management
- Basic hardware security concepts
- Testing successful and unsuccessful authentication scenarios

---

## Disclaimer

This project was developed for **educational and academic purposes**.

It is a prototype intended to demonstrate multi-factor and hardware-based authentication concepts and should not be used as a production authentication system without significant additional security improvements.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more information.
