"""
Aula 1 - Fundamentos SPI e primeira tela colorida
Mini-curso 04 - Display TFT (ST7735) com MicroPython
"""
from machine import Pin, SPI
from ST7735 import TFT
import time

# --- Pinagem (ESP32) ---
PIN_SCK  = 18   # Clock do SPI
PIN_MOSI = 23   # Dados (MOSI / SDA)
PIN_CS   = 5    # Chip Select
PIN_DC   = 2    # Data/Command (tambem chamado de A0 ou DS)
PIN_RST  = 4    # Reset

# Pico: PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 19, 17, 20, 21

spi = SPI(2, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))
# Pico: spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
#              sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()      # inicializa o controlador como ST7735 (tab preto/vermelho)
tft.rgb(True)     # ordem de cores RGB (troque para False se as cores saírem trocadas)

cores = [TFT.RED, TFT.GREEN, TFT.BLUE, TFT.WHITE, TFT.BLACK]
nomes = ["vermelho", "verde", "azul", "branco", "preto"]

while True:
    for cor, nome in zip(cores, nomes):
        print("Pintando a tela de", nome)
        tft.fill(cor)
        time.sleep(1)
