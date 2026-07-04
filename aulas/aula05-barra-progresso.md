---
title: Aula 5 — Barra de progresso / medidor
---

# Aula 5 — Barra de progresso / medidor

> **Duração estimada:** 30 minutos
> **Módulo:** 3 de 3 — Gráficos dinâmicos

---

## Objetivos

Ao final desta aula você será capaz de:

- Ler um valor analógico (potenciômetro) usando `machine.ADC`
- Converter uma leitura analógica em uma porcentagem
- Mapear essa porcentagem para a largura de um retângulo, criando uma barra de progresso dinâmica

---

## 1. Conceito

### Uma nova peça no circuito: o potenciômetro

Até agora, nossas telas mostravam sempre a mesma informação. A partir desta aula, vamos exibir **dados que mudam em tempo real** — e para isso, precisamos de uma fonte de dados. Vamos usar um **potenciômetro** (um resistor variável) ligado a uma entrada analógica do microcontrolador.

### Do valor bruto à porcentagem

O conversor analógico-digital (**ADC**) do ESP32 lê uma tensão (0 a 3.3V) e a transforma em um número inteiro entre **0 e 4095** (12 bits: 2¹² = 4096 valores possíveis). Para transformar isso numa porcentagem:

```
percentual = leitura / 4095
```

E para transformar essa porcentagem na **largura em pixels** de uma barra:

```
largura_em_pixels = percentual * largura_maxima_da_barra
```

Esse tipo de conversão — de uma escala de valores para outra — é chamado de **mapeamento** (*mapping*), e é uma das operações mais comuns ao conectar sensores a displays.

### Evitando o efeito "piscante"

Se, a cada leitura, apagarmos a barra **inteira** e a redesenharmos, o display pode parecer "piscar". Uma técnica simples para minimizar isso é sempre apagar e redesenhar apenas a **área interna** da barra (o preenchimento), mantendo o contorno fixo desenhado uma única vez, fora do loop.

---

## 2. Circuito

⚠️ Esta aula usa um **circuito diferente das anteriores**: adicionamos um potenciômetro. Use `assets/diagrams/diagram-tft-esp32-pot.json`.

> 💡O link para a simulação é: (https://wokwi.com/projects/468654060624766977)

### Pinagem adicional

| Sinal | Pino ESP32 | Pino Pico |
|-------|------------|-----------|
| Potenciômetro (sinal) | GPIO 34 (ADC1) | GP26 (ADC0) |
| Potenciômetro (VCC) | 3V3 | 3V3(OUT) |
| Potenciômetro (GND) | GND | GND |

> 💡 No ESP32, usamos o **GPIO 34** porque é um pino **somente de entrada**, ideal para leitura analógica — ele não pode ser usado como saída, mas isso não é um problema aqui.

### `diagram.json` (validar antes de publicar)

```json
{
  "version": 1,
  "author": "Mini-curso 04 - Sistemas Embarcados",
  "editor": "wokwi",
  "parts": [
    {
      "type": "wokwi-esp32-devkit-v1",
      "id": "esp",
      "top": 0,
      "left": 0,
      "attrs": { "env": "micropython-20231227-v1.22.0" }
    },
    {
      "type": "chip-st7735",
      "id": "display",
      "top": -80,
      "left": 250,
      "attrs": {}
    },
    {
      "type": "wokwi-potentiometer",
      "id": "pot1",
      "top": 120,
      "left": 250,
      "attrs": {}
    }
  ],
  "connections": [
    ["esp:TX0", "$serialMonitor:RX", "", []],
    ["esp:RX0", "$serialMonitor:TX", "", []],
    ["display:SCK", "esp:D18", "gold", []],
    ["display:MOSI", "esp:D23", "blue", []],
    ["display:CS", "esp:D5", "green", []],
    ["display:DS", "esp:D2", "orange", []],
    ["display:RST", "esp:D4", "gray", []],
    ["display:VCC", "esp:3V3", "red", []],
    ["display:GND", "esp:GND.1", "black", []],
    ["pot1:SIG", "esp:D34", "purple", []],
    ["pot1:VCC", "esp:3V3", "red", []],
    ["pot1:GND", "esp:GND.2", "black", []]
  ],
  "dependencies": {
    "chip-st7735": "github:martysweet/st7735-wokwi-chip@1.0.4"
  }
}
```

---

## 3. Código

📁 Arquivo completo: [`aulas/codigo/aula05_main.py`](./codigo/aula05_main.py)

```python
from machine import Pin, SPI, ADC
from ST7735 import TFT
from sysfont import sysfont
import time

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
pot.atten(ADC.ATTN_11DB)   # permite ler todo o intervalo de 0 a 3.3V
# Pico: pot = ADC(Pin(PIN_POT))  # nao existe atten() no RP2040

BARRA_X, BARRA_Y = 10, 60
BARRA_LARGURA, BARRA_ALTURA = 108, 20

tft.text((10, 20), "Nivel:", TFT.WHITE, sysfont, 1)
tft.rect((BARRA_X, BARRA_Y), (BARRA_LARGURA, BARRA_ALTURA), TFT.WHITE)

while True:
    leitura = pot.read()
    percentual = leitura / 4095

    largura_preenchida = int(percentual * (BARRA_LARGURA - 4))

    tft.fillrect((BARRA_X + 2, BARRA_Y + 2),
                 (BARRA_LARGURA - 4, BARRA_ALTURA - 4), TFT.BLACK)
    tft.fillrect((BARRA_X + 2, BARRA_Y + 2),
                 (largura_preenchida, BARRA_ALTURA - 4), TFT.GREEN)

    tft.fillrect((60, 20), (60, 12), TFT.BLACK)
    tft.text((60, 20), str(int(percentual * 100)) + "%", TFT.YELLOW, sysfont, 1)

    time.sleep_ms(200)
```

### Explicando o código

- `pot.atten(ADC.ATTN_11DB)` configura o ADC do ESP32 para ler toda a faixa de 0 a 3.3V (sem essa linha, a leitura fica limitada a uma faixa bem menor);
- O contorno da barra (`tft.rect`) é desenhado **uma única vez, fora do loop** — só o preenchimento interno é redesenhado a cada leitura;
- No Wokwi, clique e arraste o botão do potenciômetro simulado para ver a barra reagir em tempo real.

---

## 4. Experimento

1. Se `leitura = 2048`, qual será o `percentual` aproximado? E a `largura_preenchida`, considerando `BARRA_LARGURA = 108`?
2. Por que subtraímos `4` de `BARRA_LARGURA` e `BARRA_ALTURA` ao calcular o preenchimento interno? *(Dica: pense na espessura do contorno desenhado por `tft.rect()`.)*
3. O que aconteceria visualmente se removêssemos a linha que apaga o preenchimento antigo antes de desenhar o novo?

---

## 5. Desafio

**Desafio principal:** mude a cor da barra de acordo com o nível — verde abaixo de 50%, amarelo entre 50% e 80%, vermelho acima de 80% (como um medidor de bateria).

**Desafio bônus:** transforme a barra retangular em um **medidor circular** (como um velocímetro), desenhando um arco preenchido com `fillcircle` e `fillrect` recortando a parte que não deve aparecer, proporcional ao percentual lido.

---

## Resumo da aula

- O **ADC** transforma uma tensão analógica em um número entre 0 e 4095 (no ESP32)
- **Mapear** um valor de uma escala para outra (leitura → porcentagem → pixels) é uma operação central ao conectar sensores a displays
- Redesenhar só a parte que muda (e manter o contorno fixo) evita o efeito "piscante" na tela

---

*← [Aula 4](./aula04-triangulos-composicao.md) | [Índice](../README.md) | Próxima → [Aula 6: Gráfico de linha em tempo real](./aula06-grafico-tempo-real.md)*
