# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

while True:
    num = input("Enter a number: ") # Taking input from user
    value = write(num)
