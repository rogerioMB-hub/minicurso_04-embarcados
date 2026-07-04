"""
Aula 3 - Linhas, retangulos e circulos
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

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

# --- Linhas ---
# line(ponto_inicial, ponto_final, cor)
tft.line((0, 0), (127, 159), TFT.RED)
tft.line((127, 0), (0, 159), TFT.RED)

# --- Retangulo (somente contorno) ---
# rect(canto_superior_esquerdo, (largura, altura), cor)
tft.rect((10, 10), (40, 30), TFT.GREEN)

# --- Retangulo preenchido ---
tft.fillrect((70, 10), (40, 30), TFT.BLUE)

# --- Circulo (somente contorno) ---
# circle(centro, raio, cor)
tft.circle((30, 100), 20, TFT.YELLOW)

# --- Circulo preenchido ---
tft.fillcircle((90, 100), 20, TFT.CYAN)

while True:
    time.sleep(1)
