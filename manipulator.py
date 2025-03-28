import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# --- PINY ---
PWM_PIN = 18     # Sterowanie serwem (PWM)
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
    time.sleep(0.3)  # Krótszy czas oczekiwania
    pwm.ChangeDutyCycle(0)

# --- ZMIENNA DO PRZECHOWYWANIA STANU ---
position = 0  # 0 = zamknięte, 1 = otwarte

# --- FUNKCJA OBSŁUGI PRZYCISKU ---
def button_pressed(channel):
    global position
    if position == 0:
        set_angle(180)
        position = 1
        print("Otwarte")
    else:
        set_angle(0)
        position = 0
        print("Zamknięte")

# --- DETEKCJA PRZYCISKU ---
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=300)

# --- GŁÓWNA PĘTLA ---
try:
    print("Czekam na wciśnięcie przycisku...")
    while True:
        time.sleep(1)  # Zmniejsza obciążenie procesora

except KeyboardInterrupt:
    print("Zatrzymano program")

finally:
    pwm.stop()
    GPIO.cleanup()
