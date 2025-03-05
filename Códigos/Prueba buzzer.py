# platform: micropython-esp32
# send: wifi
# ip_mpy: 192.168.4.1
# serialport: 
# filename: main.py


import machine
import onewire
import ds18x20
import time

# Configuración del sensor DS18B20
ds_pin = machine.Pin(4)  # GPIO donde conectaste el sensor
ow = onewire.OneWire(ds_pin)
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

# Configuración del buzzer en el GPIO 5
buzzer = machine.PWM(machine.Pin(5))  # Ahora en GPIO 5

# Definir umbrales de temperatura
TEMP_FRIA = 20  # Grados Celsius (ajústalo según tu necesidad)
TEMP_CALIENTE = 40  # Grados Celsius (ajústalo también)

# Función para hacer sonar el buzzer 5 veces
def alertar_buzzer():
    for _ in range(5):  # Repetir 5 veces
        buzzer.freq(1500)  # Frecuencia de 1500 Hz
        buzzer.duty(512)  # Encender sonido
        time.sleep(0.3)  # Mantener sonido
        buzzer.duty(0)  # Apagar sonido
        time.sleep(0.3)  # Pausa entre pitidos

# Loop principal
while True:
    if not roms:
        print("⚠️ No se encontró el sensor DS18B20. Verifica la conexión.")
    else:
        ds.convert_temp()
        time.sleep(1)  # Esperar medición
        temp = ds.read_temp(roms[0])  # Leer temperatura

        print(f"🌡️ Temperatura: {temp:.2f} °C")

        # Verificar si la temperatura está fuera del rango
        if temp <= TEMP_FRIA or temp >= TEMP_CALIENTE:
            print("⚠️ Temperatura fuera de rango, activando alarma.")
            alertar_buzzer()

    time.sleep(2)  # Esperar antes de la siguiente lectura

