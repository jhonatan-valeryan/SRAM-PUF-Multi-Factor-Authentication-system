# ==========================================
# SRAM PUF MULTI-FACTOR AUTHENTICATION SYSTEM
# Python + Arduino
# ==========================================
#
# FEATURES:
# 1. Ask if user already registered
# 2. Registration page
# 3. Login page
# 4. Second authentication using SRAM PUF ID
# 5. Reads PUF ID from Arduino through Serial Port
#
# REQUIREMENTS:
# pip install pyserial
#
# Arduino should send the PUF ID through serial:
# Example:
# Serial.println("PUF123456");
#
# ==========================================

import hashlib
import serial
import time
from serial.tools import list_ports
import csv

# ==========================================
# USER DATABASE
# ==========================================

# Stores:
# username : {
#     password : hashed_password,
#     puf_id  : registered_puf
# }

#Move the user data and SRAM PUF data to a separate file, e.g CSV
user_file = "database.csv"
users = {}

# ==========================================
# SERIAL PORT SETTINGS
# ==========================================

# Change COM port based on your Arduino
# Windows example: COM3
# Linux example: /dev/ttyUSB0

#bid rate of transfer = 9600 is standard for arduino
BAUD_RATE = 9600

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def save_users():
    #save all registered users into database.csv

    with open(user_file, "w", newline="") as file:

        writer = csv.writer(file)

        #Header row
        writer.writerow(["username", "password", "puf_id"])

        #Save each user
        for username, data in users.items():

            writer.writerow([
                username,
                data["password"],
                data["puf_id"]
            ])

def load_users():
    #load all registered users from users.csv

    try:

        with open(user_file, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:
                users[row["username"]]={
                    "password" : row["password"],
                    "puf_id" : row["puf_id"]
                }

    except FileNotFoundError:
        #database.csv doesn't exist
        pass


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def list_available_ports():
    #List all available serial / COM ports
    #Let the user choose one

    ports = list(list_ports.comports())

    if not ports:
        print("No serial ports detected")
        return None

    ports.sort(key=lambda port: int(port.device.replace("COM", "")))

    print("\nAvailable Serial Ports:")
    print("-------------------------")

    for i, port in enumerate(ports, start=1):
        print(f"{i}. {port.device} - {port.description}")

    while True:
        try:
            choice = int(input("\nSelect port number: "))

            if 1 <= choice <= len(ports):
                selected_port = ports[choice - 1].device
                print(f"Selected Port: {selected_port}")
                return selected_port

            else:
                print("Invalid selection!")

        except ValueError:
            print("PLease enter a number.")

def read_puf_from_arduino():
    """
    Read SRAM PUF ID from Arduino serial port
    """
    serial_port = list_available_ports()

    if serial_port is None:
        return None


    try:
        arduino = serial.Serial(serial_port, BAUD_RATE, timeout=5)

        # Wait for Arduino reset
        time.sleep(2)

        # Request the PUF from Arduino
        arduino.write(b"GET_PUF\n")

        print("\nWaiting for SRAM PUF ID from Arduino...")

        puf_id = arduino.readline().decode().strip()

        arduino.close()

        if puf_id == "":
            print("No PUF ID received!")
            return None

        print(f"Detected Device PUF ID: {puf_id}")

        return puf_id

    except Exception as e:
        print("Error connecting to Arduino!")
        print(e)
        return None


# ==========================================
# REGISTRATION
# ==========================================

def register_user():

    print("\n========== USER REGISTRATION ==========")

    username = input("Create username: ").strip()

    if username == "":
        print("Username cannot be empty!")
        return

    if username in users:
        print("Username already exists!")
        return

    password = input("Create password: ")

    while True:
        confirm_password = input("Confirm password: ")

        if confirm_password == password:
            break

        print("Passwords do not match! Please try again.")


    print("\nConnect your SRAM PUF device...")
    device_puf = read_puf_from_arduino()

    if device_puf is None:
        print("Registration failed!")
        return

    users[username] = {
        "password": hash_password(password),
        "puf_id": device_puf
    }

    save_users()

    print("\nRegistration Successful!")
    print("PUF Device Registered Successfully!")

    # Redirect to login page
    login_user()


# ==========================================
# LOGIN
# ==========================================

def login_user():

    print("\n========== LOGIN PAGE ==========")

    username = input("Enter username: ")
    password = input("Enter password: ")

    # Check user existence
    if username not in users:
        print("User not found!")
        register_user()

    # Verify password
    hashed_password = hash_password(password)

    if hashed_password != users[username]["password"]:
        print("Incorrect password!")
        login_user()

    print("\nPassword Authentication Successful!")

    # ======================================
    # SECOND FACTOR AUTHENTICATION
    # ======================================

    print("\n========== SECOND AUTHENTICATION ==========")
    print("Please connect registered SRAM PUF device...")

    device_puf = read_puf_from_arduino()

    if device_puf is None:
        print("Second Authentication Failed!")
        return

    # Compare PUF IDs
    if device_puf == users[username]["puf_id"]:

        print("\n===================================")
        print("MULTI-FACTOR AUTHENTICATION SUCCESS")
        print(f"Welcome {username}!")
        print("===================================")

    else:

        print("\n===================================")
        print("SRAM PUF AUTHENTICATION FAILED")
        print("Unknown Device Detected!")
        print("Access Denied.")
        print("===================================")


# ==========================================
# START SYSTEM
# ==========================================

def start_system():

    print("===================================")
    print(" SRAM PUF MFA LOGIN SYSTEM ")
    print("===================================")

    answer = input("\nHave you registered before? (yes/no): ").lower()

    if answer == "yes":
        login_user()

    elif answer == "no":
        register_user()

    else:
        print("Invalid input!")
        start_system()


# ==========================================
# RUN PROGRAM
# ==========================================

load_users()
start_system()


