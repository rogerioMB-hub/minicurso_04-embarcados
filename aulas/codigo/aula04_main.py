"""
Aula 4 - Triangulos e composicao de icones
Mini-curso 04 - Display TFT (ST7735) com MicroPython
"""
from machine import Pin, SPI
from ST7735 import TFT
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


def triangulo(p1, p2, p3, cor):
    """A biblioteca ST7735 nao tem uma funcao pronta para triangulos.
    Construimos um combinando tres chamadas a tft.line()."""
    tft.line(p1, p2, cor)
    tft.line(p2, p3, cor)
    tft.line(p3, p1, cor)


# --- Triangulo simples ---
triangulo((64, 10), (44, 40), (84, 40), TFT.YELLOW)


# --- Composicao: icone de uma casinha ---
def desenha_casa(x, y):
    # parede (retangulo preenchido)
    tft.fillrect((x, y + 20), (40, 30), TFT.GRAY)
    # telhado (triangulo, usando a funcao que criamos acima)
    triangulo((x + 20, y), (x - 5, y + 20), (x + 45, y + 20), TFT.RED)
    # porta (retangulo pequeno)
    tft.fillrect((x + 15, y + 35), (10, 15), TFT.NAVY)


desenha_casa(20, 80)

while True:
    time.sleep(1)
