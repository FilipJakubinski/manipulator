import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# --- PINY ---
PWM_PIN = 18     # Sterowanie serwem (PWM)
#OUTPUT_PIN = 23  # Wyjście – domyślnie HIGH, przy przycisku LOW
BUTTON_PIN = 23  # Przycisk

# --- KONFIGURACJA GPIO ---
GPIO.setup(PWM_PIN, GPIO.OUT)
#GPIO.setup(OUTPUT_PIN, GPIO.OUT)
#GPIO.output(OUTPUT_PIN, GPIO.HIGH)  # Domyślnie HIGH

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- INICJALIZACJA PWM (50Hz dla serwa) ---
pwm = GPIO.PWM(PWM_PIN, 50)
pwm.start(0)

# --- FUNKCJA USTAWIANIA KĄTA ---
def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

try:
    print("Czekam na wciśnięcie przycisku...")

    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            set_angle(180)
            GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            print("otwarte")
        else:
            set_angle(0)
            print("zamykam")

except KeyboardInterrupt:
    print("Zatrzymano program")

finally:
    pwm.stop()
    GPIO.cleanup()