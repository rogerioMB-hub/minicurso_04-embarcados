---
title: Aula 4 — Triângulos e composição de ícones
---

# Aula 4 — Triângulos e composição de ícones

> **Duração estimada:** 30 minutos
> **Módulo:** 2 de 3 — Formas geométricas

---

## Objetivos

Ao final desta aula você será capaz de:

- Construir sua própria função de desenho combinando primitivas já existentes
- Desenhar triângulos usando três chamadas a `line()`
- Compor um ícone simples combinando várias formas geométricas

---

## 1. Conceito

### Nem toda forma vem pronta

Na Aula 3 vimos que a biblioteca `ST7735.py` já tem funções para linha, retângulo e círculo — mas **não tem uma função para triângulo**. Isso é muito comum em bibliotecas gráficas simples: elas fornecem os "blocos de construção" básicos, e cabe a quem programa **compor** formas mais complexas a partir deles.

Um triângulo é definido por três pontos: `p1`, `p2` e `p3`. Para desenhar seu contorno, basta ligar cada par de pontos com uma linha:

```
p1 ────────── p2
  ╲          ╱
    ╲      ╱
      ╲  ╱
       p3
```

Ou seja: `linha(p1, p2)` + `linha(p2, p3)` + `linha(p3, p1)`.

### Composição de ícones

A mesma ideia vale para desenhos mais elaborados: um ícone de casinha, por exemplo, nada mais é do que a **composição** de formas simples que vocês já conhecem:

- Um **retângulo preenchido** (a parede)
- Um **triângulo** (o telhado)
- Um **retângulo pequeno** (a porta)

Pensar em "que formas simples compõem esse desenho?" é uma habilidade central em computação gráfica — dos ícones de um sistema operacional aos personagens de um jogo 2D.

---

## 2. Circuito

O circuito é **o mesmo das aulas anteriores** — nenhuma mudança na ligação física. Use `assets/diagrams/diagram-tft-esp32.json`.

> 💡O link para a simulação é: (https://wokwi.com/projects/468653677153164289)

---

## 3. Código

📁 Arquivo completo: [`aulas/codigo/aula04_main.py`](./codigo/aula04_main.py)

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


def triangulo(p1, p2, p3, cor):
    """A biblioteca ST7735 nao tem uma funcao pronta para triangulos.
    Construimos um combinando tres chamadas a tft.line()."""
    tft.line(p1, p2, cor)
    tft.line(p2, p3, cor)
    tft.line(p3, p1, cor)


# Triangulo simples
triangulo((64, 10), (44, 40), (84, 40), TFT.YELLOW)


# Composicao: icone de uma casinha
def desenha_casa(x, y):
    tft.fillrect((x, y + 20), (40, 30), TFT.GRAY)               # parede
    triangulo((x + 20, y), (x - 5, y + 20), (x + 45, y + 20), TFT.RED)  # telhado
    tft.fillrect((x + 15, y + 35), (10, 15), TFT.NAVY)          # porta


desenha_casa(20, 80)

while True:
    time.sleep(1)
```

### Explicando o código

- A função `triangulo()` recebe três pontos e uma cor, e simplesmente desenha as três linhas que conectam os pontos;
- `desenha_casa(x, y)` recebe apenas a posição do **canto superior esquerdo da parede** e calcula, a partir dela, onde cada peça (parede, telhado, porta) deve ficar — assim é fácil desenhar a casa em qualquer lugar da tela, só mudando `x` e `y`.

---

## 4. Experimento

1. Nossa função `triangulo()` desenha apenas o **contorno**. O que você imagina que seria necessário para *preencher* o triângulo de cor sólida? (Não precisa implementar ainda — só descrever a ideia.)
2. Se você chamar `desenha_casa(0, 0)`, alguma parte do desenho vai ficar fora da tela? Por quê?
3. Troque a ordem dos três pontos na chamada de `triangulo()` (por exemplo, `p2, p1, p3`). O desenho muda?

---

## 5. Desafio

**Desafio principal:** adicione uma janela (um pequeno quadrado com uma cruz no meio, feita de duas linhas) na parede da casa.

**Desafio bônus:** implemente uma função `triangulo_preenchido(p1, p2, p3, cor)`. Uma forma simples de fazer isso é desenhar várias linhas horizontais (`hline`) entre as bordas do triângulo, percorrendo cada linha (`y`) de cima a baixo — essa técnica se chama **preenchimento por varredura** (*scanline fill*) e é a base de como motores gráficos preenchem polígonos.

---

## Resumo da aula

- Bibliotecas gráficas simples nem sempre têm todas as formas prontas — muitas vezes é preciso **compor** formas complexas a partir de primitivas mais simples
- Um triângulo pode ser desenhado com três chamadas a `line()`, unindo seus três vértices
- Ícones e desenhos mais elaborados são combinações de formas simples posicionadas relativas umas às outras

---

*← [Aula 3](./aula03-linhas-retangulos-circulos.md) | [Índice](../README.md) | Próxima → [Aula 5: Barra de progresso / medidor](./aula05-barra-progresso.md)*
