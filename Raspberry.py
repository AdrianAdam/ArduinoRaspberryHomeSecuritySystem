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


def deleteVideos():
    global indexVideoDeleted
    if not indexVideo == indexVideoDeleted:
        for i in range(indexVideoDeleted, indexVideo - 1):
            os.remove("/home/pi/Documents/Project/video{:03d}.h264".format(i))
            os.remove("/home/pi/Documents/Project/video{:03d}.mp4".format(i))
           
        indexVideoDeleted = indexVideo - 1
        
        
scheduler = BackgroundScheduler()
scheduler.start()
deleteVideos()
scheduler.add_job(deleteVideos, 'interval', seconds = callFunctionAgain)

firebase = firebase.FirebaseApplication('', None) #link to your Firebase project
client = storage.Client.from_service_account_json('') #path to your Firebase storage json file
bucket = client.get_bucket('') #link to your storage bucket

#subprocess.call("raspivid -t 0 -o - | nc 192.168.43.216 8090", shell=True) #not working attempt of live streaming

try:
    while True:
        if ser.readline() is not None:
            Input = ser.readline()
            time = datetime.datetime.now()
            dataOut = {"message": "Intruder detected!", "datetime": time}
            firebase.post('/Door1/DT', dataOut)

            camera.start_preview()
            camera.start_recording('/home/pi/Documents/Project/video{:03d}.h264'.format(indexVideo))
            sleep(10)
            camera.stop_recording()
            camera.stop_preview()
    
            command = "MP4Box -add video{:03d}.h264 video{:03d}.mp4".format(indexVideo, indexVideo)
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

            videoBlob = bucket.blob(str(time))
            videoBlob.upload_from_filename(videoPath + "/video{:03d}.mp4".format(indexVideo))
    
            indexVideo += 1
except KeyboardInterrupt:
    pass

if not indexVideo == 0:
    for i in range(indexVideosDeleted, indexVideo + 1):
        os.remove("/home/pi/Documents/Project/video{:03d}.h264".format(i))
        os.remove("/home/pi/Documents/Project/video{:03d}.mp4".format(i))
