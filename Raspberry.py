#!/usr/bin/env python3
import serial
import os
from time import sleep
from firebase import firebase
import json
import shlex
import subprocess
import datetime
from picamera import PiCamera
from google.cloud import storage
from Crypto.Cipher import AES
import base64
from apscheduler.schedulers.background import BackgroundScheduler

ser=serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600

Input = ""
startRecording = False
indexVideo = 0
indexVideoDeleted = 0
callFunctionAgain = 600 #repeat the function after 10 minutes
videoPath = "/home/pi/Documents/Project"

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1280, 768)

# To achieve AES 256, the key must have a length of 32 bits
#aes = AES.new("This needs to be a 32 bit key!!!", AES.MODE_CBC, "This is a 16 bit")

def deleteVideos():
    print("Started deleting older videos")
    global indexVideoDeleted
    if not indexVideo == indexVideoDeleted:
        for i in range(indexVideoDeleted, indexVideo - 1):
            os.remove("/home/pi/Documents/Project/video{:03d}.h264".format(i))
            os.remove("/home/pi/Documents/Project/video{:03d}.mp4".format(i))
           
        indexVideoDeleted = indexVideo - 1
    print("Finished deleting older videos")

    
def customEncryptData(strText):
    print("Started encrypting data")
    strResult = ""
    
    for i in range(0, len(strText)):
        if(strText[i] == " ")
            strResult += "n "
        else:
            strResult += str(ord(strText[i]) - 10) + " "
            
    return strResult

        
scheduler = BackgroundScheduler()
scheduler.start()
deleteVideos()
scheduler.add_job(deleteVideos, 'interval', seconds = callFunctionAgain)

firebase = firebase.FirebaseApplication('', None) #link to your Firebase project
client = storage.Client.from_service_account_json('') #path to your Firebase storage json file
bucket = client.get_bucket('') #link to your storage bucket

try:
    print("Started main loop")
    print("----------------------------")
    while True:
        if ser.readline() is not None:
            print("Received message")
            Input = ser.readline()
            time = datetime.datetime.now()
            time = time.strftime("%Y-%m-%d %H%M%S")
            #if len(time) < 32:
                #time += "!" * (32 - len(time))
            message = "Sensor triggered"
            #encryptedMessage = aes.encrypt(message)
            #encryptedTime = aes.encrypt(time)
            
            encryptedMessage = customEncryptData(message)
            encryptedTime = customEncryptTime(time)
            
            dataOut = {"message": encryptedMessage, "datetime": encryptedTime}
            firebase.post('/Door1/DT', dataOut)

            print("Sent message")
            print("Started camera preview")
            
            camera.start_preview()
            camera.start_recording('/home/pi/Documents/Project/video{:03d}.h264'.format(indexVideo))
            sleep(10)
            camera.stop_recording()
            camera.stop_preview()
            
            print("Finished camera preview")
            print("Started file upload")
            
            command = "MP4Box -add video{:03d}.h264 video{:03d}.mp4".format(indexVideo, indexVideo)
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

            videoBlob = bucket.blob(str(time))
            videoBlob.upload_from_filename(videoPath + "/video{:03d}.mp4".format(indexVideo))
            
            print("Finished file upload")
            print("----------------------------")
    
            indexVideo += 1
except KeyboardInterrupt:
    pass
