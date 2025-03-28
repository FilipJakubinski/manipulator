import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# --- PINY ---
PWM_PIN = 18  # Sterowanie serwem (PWM)
BUTTON_PIN = 23  # Przycisk

# --- KONFIGURACJA GPIO ---
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- INICJALIZACJA PWM (50Hz dla serwa) ---
pwm = GPIO.PWM(PWM_PIN, 50)
pwm.start(0)


# --- FUNKCJA USTAWIANIA KĄTA ---
def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Czekaj, aż serwo się ustawi
    pwm.ChangeDutyCycle(0)  # Zatrzymanie PWM, aby uniknąć drgań


# --- USTAWIAMY SERWO NA ZAMKNIĘTE ---
set_angle(0)
print("Serwo ustawione na zamknięte")

try:
    print("Czekam na wciśnięcie przycisku...")

    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Wciśnięty przycisk
            set_angle(180)  # Otwórz serwo
            print("Otwarte")

            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.1)  # Czekaj, aż użytkownik puści przycisk

            print("Zamykam...")
            set_angle(0)  # Zamknij serwo

except KeyboardInterrupt:
    print("Zatrzymano program")

finally:
    pwm.stop()
    GPIO.cleanup()
