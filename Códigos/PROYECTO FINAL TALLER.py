import machine
import time
import onewire
import ds18x20
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# Pines
sensor_pin = 4  # Pin del sensor DS18B20
buzzer_pin = 5  # Pin del buzzer
i2c_scl = 22    # Pin SCL del LCD
i2c_sda = 21    # Pin SDA del LCD

# Configuración del sensor
ds_sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(sensor_pin)))
roms = ds_sensor.scan()

# Configuración del buzzer
buzzer = machine.Pin(buzzer_pin, machine.Pin.OUT)

# Configuración del LCD
I2C_ADDR = 0x27  # Dirección del LCD
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(i2c_scl), sda=Pin(i2c_sda), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

# Verifica si el sensor está conectado
if not roms:
    print("⚠️ No se encontró ningún sensor DS18B20")
    lcd.putstr("Sensor no encontrado")
    while True:
        pass  # Se queda aquí si no detecta el sensor

print(f"✅ Sensor encontrado: {roms}")

def activar_buzzer():
    for _ in range(5):  # Suena 5 veces
        buzzer.on()
        time.sleep(0.2)
        buzzer.off()
        time.sleep(2)  # Pausa de 2 segundos entre cada beep

while True:
    ds_sensor.convert_temp()
    time.sleep(1)  # Espera la conversión de temperatura
    temp = ds_sensor.read_temp(roms[0])  # Lee la temperatura

    print(f"La temperatura del líquido es: {temp:.2f}°C")  # Muestra la temperatura en consola
    
    # Limpia la pantalla y muestra la temperatura
    lcd.clear()
    lcd.putstr(f"Temp: {temp:.2f}C")

    if temp < 19:
        print("⚠️ Temperatura baja, líquido frío")
        lcd.clear()
        lcd.putstr("Temp. baja!")
        activar_buzzer()

    elif temp > 30:
        print("🔥 Líquido muy caliente")
        lcd.clear()
        lcd.putstr("Líquido caliente!")
        activar_buzzer()

    time.sleep(2)  # Pausa antes de la siguiente lectura
