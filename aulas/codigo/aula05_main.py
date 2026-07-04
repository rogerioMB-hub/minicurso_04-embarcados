"""
Aula 5 - Barra de progresso / medidor
Mini-curso 04 - Display TFT (ST7735) com MicroPython
"""
from machine import Pin, SPI, ADC
from ST7735 import TFT
from sysfont import sysfont
import time

# --- Pinagem (ESP32) ---
PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 23, 5, 2, 4
PIN_POT = 34   # entrada analogica ligada ao potenciometro
# Pico: PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 19, 17, 20, 21
# Pico: PIN_POT = 26  (ADC0)

spi = SPI(2, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

pot = ADC(Pin(PIN_POT))
pot.atten(ADC.ATTN_11DB)   # permite ler todo o intervalo de 0 a 3.3V
# Pico: pot = ADC(Pin(PIN_POT))  # no RP2040 nao existe atten(), o padrao ja cobre 0-3.3V

BARRA_X, BARRA_Y = 10, 60
BARRA_LARGURA, BARRA_ALTURA = 108, 20

tft.text((10, 20), "Nivel:", TFT.WHITE, sysfont, 1)
tft.rect((BARRA_X, BARRA_Y), (BARRA_LARGURA, BARRA_ALTURA), TFT.WHITE)

while True:
    leitura = pot.read()                 # 0 a 4095 no ESP32
    percentual = leitura / 4095

    largura_preenchida = int(percentual * (BARRA_LARGURA - 4))

    # apaga o preenchimento anterior e desenha o novo
    tft.fillrect((BARRA_X + 2, BARRA_Y + 2),
                 (BARRA_LARGURA - 4, BARRA_ALTURA - 4), TFT.BLACK)
    tft.fillrect((BARRA_X + 2, BARRA_Y + 2),
                 (largura_preenchida, BARRA_ALTURA - 4), TFT.GREEN)

    # atualiza o texto percentual
    tft.fillrect((60, 20), (60, 12), TFT.BLACK)
    tft.text((60, 20), str(int(percentual * 100)) + "%", TFT.YELLOW, sysfont, 1)

    time.sleep_ms(200)
