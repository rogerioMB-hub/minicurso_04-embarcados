---
title: Aula 3 — Linhas, retângulos e círculos
---

# Aula 3 — Linhas, retângulos e círculos

> **Duração estimada:** 30 minutos
> **Módulo:** 2 de 3 — Formas geométricas

---

## Objetivos

Ao final desta aula você será capaz de:

- Desenhar linhas, retângulos e círculos usando as primitivas da biblioteca ST7735
- Diferenciar formas de **contorno** (apenas a borda) de formas **preenchidas**
- Usar o sistema de coordenadas do display (origem no canto superior esquerdo)

---

## 1. Conceito

### O sistema de coordenadas

O display TFT de 128×160 pixels usa o **canto superior esquerdo como origem `(0, 0)`**. O eixo X cresce para a direita, e o eixo Y cresce **para baixo** (diferente do plano cartesiano da matemática, onde Y cresce para cima!).

```
(0,0) ───────────────► X (até 127)
  │
  │
  │
  ▼
  Y (até 159)
```

### As primitivas de desenho

A biblioteca `ST7735.py` oferece funções prontas para as formas mais comuns:

| Função | O que desenha |
|--------|----------------|
| `line(p1, p2, cor)` | Uma linha reta entre dois pontos |
| `hline(p, comprimento, cor)` | Uma linha horizontal |
| `vline(p, comprimento, cor)` | Uma linha vertical |
| `rect(p, (largura, altura), cor)` | Retângulo — **somente contorno** |
| `fillrect(p, (largura, altura), cor)` | Retângulo **preenchido** |
| `circle(centro, raio, cor)` | Círculo — **somente contorno** |
| `fillcircle(centro, raio, cor)` | Círculo **preenchido** |

> 💡 Repare no padrão: toda forma preenchida tem o prefixo `fill` na frente do nome da forma de contorno correspondente. Esse padrão vai ser importante na próxima aula, quando formos criar nossa própria função para triângulos.

---

## 2. Circuito

O circuito é **o mesmo das Aulas 1 e 2** — nenhuma mudança na ligação física. Use `assets/diagrams/diagram-tft-esp32.json`.

---

## 3. Código

📁 Arquivo completo: [`aulas/codigo/aula03_main.py`](./codigo/aula03_main.py)

```python
from machine import Pin, SPI
from ST7735 import TFT
import time

PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 23, 5, 2, 4
# Pico: PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 19, 17, 20, 21

spi = SPI(2, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

# Linhas
tft.line((0, 0), (127, 159), TFT.RED)
tft.line((127, 0), (0, 159), TFT.RED)

# Retangulo (somente contorno)
tft.rect((10, 10), (40, 30), TFT.GREEN)

# Retangulo preenchido
tft.fillrect((70, 10), (40, 30), TFT.BLUE)

# Circulo (somente contorno)
tft.circle((30, 100), 20, TFT.YELLOW)

# Circulo preenchido
tft.fillcircle((90, 100), 20, TFT.CYAN)

while True:
    time.sleep(1)
```

### Explicando o código

- As duas primeiras linhas desenham um "X" ligando os quatro cantos da tela;
- `rect((10, 10), (40, 30), ...)` desenha um retângulo cujo canto superior esquerdo fica em `(10, 10)`, com 40 pixels de largura e 30 de altura;
- `circle((30, 100), 20, ...)` desenha um círculo **centrado** em `(30, 100)` com raio de 20 pixels.

---

## 4. Experimento

1. Se um círculo tem `centro = (30, 100)` e `raio = 20`, quais são as coordenadas do ponto mais à esquerda e mais à direita do círculo?
2. O que acontece se você desenhar um retângulo com `largura` ou `altura` negativa? Teste e explique o resultado.
3. Qual a diferença visual entre `rect()` e `fillrect()` quando ambos usam a mesma cor de fundo da tela?

---

## 5. Desafio

**Desafio principal:** desenhe um "alvo" (círculos concêntricos, como um alvo de dardo) no centro da tela, alternando entre duas cores, com pelo menos 3 círculos de raios diferentes.

**Desafio bônus:** crie uma barra de "termômetro" vertical: um retângulo de contorno fixo (representando o tubo de vidro) e, dentro dele, um retângulo preenchido cuja altura você pode alterar mudando uma variável no código (simulando o nível do mercúrio).

---

## Resumo da aula

- O display usa um sistema de coordenadas com origem no canto superior esquerdo e eixo Y crescendo para baixo
- Toda forma tem uma versão de **contorno** e uma versão **preenchida** (`fill` + nome da forma)
- `line`, `rect`, `fillrect`, `circle` e `fillcircle` são as primitivas básicas de desenho da biblioteca

---

*← [Aula 2](./aula02-hello-world-texto.md) | [Índice](../README.md) | Próxima → [Aula 4: Triângulos e composição de ícones](./aula04-triangulos-composicao.md)*
