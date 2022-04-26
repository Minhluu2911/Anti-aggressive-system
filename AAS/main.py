import random
import time
import sys
import os
import json

import serial.tools.list_ports
from Adafruit_IO import MQTTClient

AIO_FEED_IDS = ['button']
AIO_USERNAME = os.environ['AIO_USERNAME']
AIO_KEY = os.environ['AIO_KEY']

def connected(client):
    print("Connection established successfully.")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed.")

def disconnected(client):
    print("Disconnected.")
    sys.exit (1)

def message(client, feed_id, payload):
    print("Data received: " + payload)
    if isMicrobitConnected:
        ser.write((str(payload) + "#").encode())

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isMicrobitConnected = True
print("microbit = " + str(isMicrobitConnected))


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    try:
        if splitData[0] == "BUTTON":
            client.publish("project212.button", splitData[1])
        elif splitData[0] == "TEMP":
            client.publish("project212.temp", splitData[1])
        elif splitData[0] == "HUMI":
            client.publish("project212.humid", splitData[1])
        # if splitData[1] == "TEMP":
        #     client.publish("bbc-temp", splitData[2])
        # elif splitData[2] == "HUMI":
        #     client.publish("bbc-temp", splitData[3])
    except:
        pass

mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    print('bytesToRead = ' + str(bytesToRead))
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        print('mess = ' + mess)
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            mess = mess[end+1:]

while True:
    if isMicrobitConnected:
        readSerial()
    client.publish(
        'button',
        json.dumps({'value': random.randint(0, 999999)}),
        )
    time.sleep(5)