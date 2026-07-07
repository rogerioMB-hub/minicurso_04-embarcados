"""
Aula 2 - Hello World: texto na tela
Mini-curso 04 - Display TFT (ST7735) com MicroPython
"""
from machine import Pin, SPI
from ST7735 import TFT
from sysfont import sysfont
import time

# --- Pinagem (ESP32) ---
PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 23, 5, 2, 4
# Pico: PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 19, 17, 20, 21

spi = SPI(2, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))
# Pico: spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
#              sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

# text(posicao, texto, cor, fonte, tamanho)
tft.text((5, 10), "Ola, mundo!", TFT.WHITE, sysfont, 1)
tft.text((5, 30), "PICO + TFT", TFT.CYAN, sysfont, 2)
# ESP32: tft.text((5, 30), "ESP32 + TFT", TFT.CYAN, sysfont, 2)

contador = 0
while True:
    # Antes de escrever o novo valor, apagamos a area onde o numero antigo estava.
    # Sem isso, os digitos ficariam sobrepostos e ilegiveis.
    tft.fillrect((5, 70), (110, 12), TFT.BLACK)
    tft.text((5, 70), "n = " + str(contador), TFT.YELLOW, sysfont, 1)
    contador += 1
    time.sleep(1)
