import serial.tools.list_ports
import time
import sys
import threading
from Adafruit_IO import MQTTClient

currentWater = [0]
cwLock = threading.Lock()

AIO_FEED_IDS = ["emotion-a@a"]

AIO_USERNAME = "nghianguyen1"
AIO_KEY = "aio_IbfZ71bWihZqIeK0BYOdt9ZXxZnO"


def  connected(client):
    print("Connection established successfully.")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)


def  subscribe(client, userdata, mid, granted_qos):
    print("Subsciptions are done.")


def  disconnected(client):
    print("Disconnected.")
    sys.exit (1)


def  message(client, feed_id, payload):
    if isMicrobitConnected:
        if feed_id == "emotion-a@a" and payload == "0":
            ser.write(("1#").encode())
            with cwLock:
                currentWater[0] += 500


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


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    try:
        if splitData[0] == "BUTTON":
            if splitData[1] == "0":
                with cwLock:
                    currentWater[0] += 500
        elif splitData[0] == "TEMP":
            if splitData[1] >= "20":
                ser.write(("2#").encode())
    except:
        pass


mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            mess = mess[end+1:]


def sendWaterData(currentWater):
    while True:
        time.sleep(10)
        client.publish("water-a@a", currentWater[0])
        with cwLock:
            currentWater[0] = 0


threading.Thread(target=sendWaterData, args=(currentWater,)).start()
while True:
    if isMicrobitConnected:
        readSerial()

    time.sleep(1)
