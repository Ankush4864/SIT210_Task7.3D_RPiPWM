

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Define pins
Trigger = 17
Echo = 18
Buzzer = 2

# Set up pins
GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)
GPIO.setup(Buzzer, GPIO.OUT)

# Initialize the buzzer
pwm = GPIO.PWM(Buzzer, 1000)
pwm.start(0)

# Initialize duty_cycle
duty_cycle = 0

# Define functions
def getDistance():
    # Trigger the SRO4
    GPIO.output(Trigger, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trigger, GPIO.LOW)

    # Get the start time
    while GPIO.input(Echo) == False:
        startTime = time.time()

    # Get the finishing time
    while GPIO.input(Echo) == True:
        finishTime = time.time()

    # Calculate the distance
    totalTime = finishTime - startTime
    distance = (totalTime * 34300) / 2

    return distance

try:
    while True:
        # Get the distance and print it to the terminal
        distance = getDistance()
        print(distance)

        # Limit the distance which will affect the buzzer to 1 meter
        if distance > 100:
            distance = 100

        if distance < 0:
            distance = 0

        # Calculate the duty cycle based on distance
        # When the object is near, make the buzzer loud (high duty cycle)
        # When the object is far, make the buzzer softer (low duty cycle)
        # When the object is more than 1 meter away, turn off the buzzer
        if distance >= 100:
            pwm.ChangeDutyCycle(0)  # Turn off the buzzer
        else:
            duty_cycle = 100 - (distance / 100) * 100
            pwm.ChangeDutyCycle(duty_cycle)

        # Print the distance and buzzer duty cycle
        print(f"Distance: {distance} cm, Duty Cycle: {duty_cycle}%")

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
