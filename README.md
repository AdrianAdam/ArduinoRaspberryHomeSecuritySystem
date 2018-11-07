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
- we make a new project in Firebase and we start structuring the code.
- we'll install a camera and: the phone will be able to connect, from within the app, to a livestream and see live the room where the camera is and, when an intruder is detected, the camera will start recording for 10 seconds. After those 10 seconds, the file is posted to Firebase and the app will take it from there.
- (more explanations will come later)

Code: (will come later)

# Android Studio
- take the data from Firebase Database.
- we send push notifications every time a new data is inserted in the database (with Firebase functions).
- the ability to see a livestream and recorded footage.
- the ability to see when the alarm went off.
- the ability to delete older logs.

Code: (will come then the project is ready)
