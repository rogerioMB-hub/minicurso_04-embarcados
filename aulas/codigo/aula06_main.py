"""
Aula 6 - Grafico de linha em tempo real ("osciloscopio" simples)
Mini-curso 04 - Display TFT (ST7735) com MicroPython
"""
from machine import Pin, SPI, ADC
from ST7735 import TFT
import time

# --- Pinagem (ESP32) ---
PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 23, 5, 2, 4
PIN_POT = 34
# Pico: PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 19, 17, 20, 21
# Pico: PIN_POT = 26

spi = SPI(2, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

pot = ADC(Pin(PIN_POT))
pot.atten(ADC.ATTN_11DB)
# Pico: pot = ADC(Pin(PIN_POT))

GRAFICO_X, GRAFICO_Y = 4, 10
GRAFICO_LARGURA, GRAFICO_ALTURA = 120, 130

# Buffer com um valor de altura (em pixels) para cada coluna do grafico
valores = [0] * GRAFICO_LARGURA

tft.rect((GRAFICO_X - 1, GRAFICO_Y - 1),
         (GRAFICO_LARGURA + 2, GRAFICO_ALTURA + 2), TFT.WHITE)

while True:
    leitura = pot.read()  # 0 a 4095
    altura_px = int((leitura / 4095) * (GRAFICO_ALTURA - 1))

    # Descarta o valor mais antigo e adiciona o novo no final (buffer "andando")
    valores.pop(0)
    valores.append(altura_px)

    # Apaga a area do grafico e redesenha todos os segmentos de reta
    tft.fillrect((GRAFICO_X, GRAFICO_Y), (GRAFICO_LARGURA, GRAFICO_ALTURA), TFT.BLACK)

    # O eixo X deste display sai espelhado (comportamento comum em modulos ST7735,
    # que varia conforme o fabricante/tab do chip). Por isso invertemos aqui o
    # mapeamento coluna -> x, para que o valor mais novo (fim do buffer) sempre
    # apareca a direita, e o mais antigo (inicio do buffer) saia pela esquerda.
    for coluna in range(GRAFICO_LARGURA - 1):
        x1 = GRAFICO_X + (GRAFICO_LARGURA - 1 - coluna)
        x2 = GRAFICO_X + (GRAFICO_LARGURA - 1 - (coluna + 1))
        y1 = GRAFICO_Y + (GRAFICO_ALTURA - 1 - valores[coluna])
        y2 = GRAFICO_Y + (GRAFICO_ALTURA - 1 - valores[coluna + 1])
        tft.line((x1, y1), (x2, y2), TFT.GREEN)

    time.sleep_ms(50)
