# ArduinoRaspberryHomeSecuritySystem

Requirements: Arduino (I used an Arduino Mega 2560 Rev3), Raspberry Pi (I used a Raspberry Pi 3 B+), Android Studio, Firebase Database.

# Arduino: 
- breadboard, jumper wires, buzzer, HC-SR04 sensor.
- every time the distance between the sensor and the object in front of it is below 20 centimeters, the buzzer will start and we will print a message in the serial monitor ("Intruder").

Diagram: Images/Diagram.png (Take the shorter leg and connect it to Ground. The longer leg goes to PWM 11).

Code: file ArduinoDistance.ino.

# Raspberry:
- take the data from arduino and send it to Firebase Database.
- we make a serial connection between Arduino and Raspberry.
- we will import a lot of libraries needed for firebase database, storage and other essentials
- we'll install a camera and: the phone will be able to connect, from within the app, to a livestream and see live the room where the camera is and, when an intruder is detected, the camera will start recording for 10 seconds. After those 10 seconds, the file is posted to Firebase and the android app will take it from there.
- there is no need to manually delete older videos, because each time we run the script, and at each 30 minutes, the videos are automatically deleted.
- initially I didn't have the function to delete older videos, and I have noticed that older videos were uploaded to firebase instead of the newer ones (when I rerun the script, the video count restarts at 0). So a file management system is mandatory.

Code: file Raspberry.py

# Android Studio
- take the data from Firebase Database.
- we send push notifications every time a new data is inserted in the database (with Firebase functions).
- we can: see a livestream and recorded footage and when the alarm went off and delete older logs.
- videos will be stored locally to save data (and make them available to watch when offline).

Code: (will come then the project is ready)
