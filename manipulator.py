import pigpio
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# --- PINY ---
PWM_PIN = 18     # Sterowanie serwem
BUTTON_PIN = 23  # Przycisk

# --- KONFIGURACJA GPIO ---
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- INICJALIZACJA PIGPIO ---
pi = pigpio.pi()  # Tworzymy instancję pigpio

# --- FUNKCJA USTAWIANIA KĄTA ---
def set_angle(angle):
    pulse_width = int((angle / 180) * 2000 + 500)  # 0° = 500µs, 180° = 2500µs
    pi.set_servo_pulsewidth(PWM_PIN, pulse_width)

# --- SERWO STARTUJE W POZYCJI ZAMKNIĘTEJ ---
set_angle(0)
print("Serwo zamknięte")

# --- ZMIENNA PRZECHOWUJĄCA STAN SERWA ---
position = 0  # 0 = zamknięte, 1 = otwarte

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Przycisk wciśnięty
            position = 1 - position  # Zmiana stanu (0 -> 1 lub 1 -> 0)

            if position == 1:
                set_angle(180)  # Otwórz serwo
                print("Otwarte")
            else:
                set_angle(0)  # Zamknij serwo
                print("Zamknięte")

            while GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Czekaj na puszczenie przycisku
                time.sleep(0.1)

        time.sleep(0.1)  # Mała przerwa między sprawdzeniami

except KeyboardInterrupt:
    print("Zatrzymano program")

finally:
    set_angle(0)  # Zamknięcie serwa przy wyjściu
    pi.set_servo_pulsewidth(PWM_PIN, 0)  # Wyłączenie PWM
    pi.stop()
    GPIO.cleanup()
