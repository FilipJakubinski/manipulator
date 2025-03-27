import RPi.GPIO as GPIO
#import Jetson.GPIO as GPIO
import time

# Użyj numeracji BOARD (fizyczne numery pinów)
GPIO.setmode(GPIO.BCM)

# Pin 32 = PWM0 = GPIO13
PWM_PIN = 18
GPIO.setup(PWM_PIN, GPIO.OUT)

# Utwórz obiekt PWM na 50 Hz (typowe dla serw)
pwm = GPIO.PWM(PWM_PIN, 50)
pwm.start(0)  # Start z 0% wypełnienia

def set_angle(angle):
    # Przekształcenie kąta (0-180) na wypełnienie (duty cycle)
    duty = 2 + (angle / 18)  # działa dobrze dla MG996R
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Czas na ruch
    pwm.ChangeDutyCycle(0)  # Zatrzymaj sygnał, by serwo nie drżało

try:
    while True:
        x=int(input())
        if x==0:
            set_angle(10)
            time.sleep(5)
        else:
            set_angle(50)
            time.sleep(5)

except KeyboardInterrupt:
    print("Zatrzymano program")

finally:
    pwm.stop()
    GPIO.cleanup