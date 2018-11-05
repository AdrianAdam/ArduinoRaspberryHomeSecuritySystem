// defines pins numbers
const int trigPin = 9;
const int echoPin = 10;
const int buzzerPin = 11;

// defines variables
long duration;
int distance;

void setup() {
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
pinMode(buzzerPin, OUTPUT); // Sets the buzzerPin as an Output 
Serial.begin(9600); // Starts the serial communication
delay(1000);
}

void loop() {
// Clears the trigPin
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);
// Calculating the distance
distance = duration*0.034/2;
// Starts the buzzer
if (distance < 20) {
  tone(buzzerPin, 100);
  delay(100);
  noTone(buzzerPin);
  Serial.println("Intruder");
}
}
