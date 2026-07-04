---
title: Aula 2 — Hello World, texto na tela
---

# Aula 2 — Hello World: texto na tela

> **Duração estimada:** 30 minutos
> **Módulo:** 1 de 3 — Fundamentos e ligação

---

## Objetivos

Ao final desta aula você será capaz de:

- Escrever texto na tela usando uma **fonte bitmap**
- Controlar cor, tamanho e posição do texto
- Apagar e redesenhar apenas a parte da tela que muda (evitando "sujeira" na tela)

---

## 1. Conceito

### Como o display desenha uma letra?

Um display TFT não sabe o que é a letra "A" — ele só sabe pintar pixels. Por isso, uma **biblioteca de fonte** (nosso `sysfont.py`) guarda, para cada caractere, um pequeno "desenho" feito de bits: cada bit ligado vira um pixel pintado.

Nossa fonte usa caracteres de **5×8 pixels**: 5 colunas de 8 bits cada. Veja como o "0" (zero) é armazenado, olhando o início do arquivo `sysfont.py`:

```python
sysfont = {"Width": 5, "Height": 8, "Start": 0, "End": 254, "Data": bytearray([
  ...
])}
```

- `Width` / `Height`: dimensões de cada caractere, em pixels
- `Start` / `End`: intervalo de códigos ASCII cobertos pela fonte
- `Data`: os bytes com o desenho de cada caractere, um atrás do outro

O método `tft.text()` faz o trabalho de percorrer essa tabela para você — não é preciso entender os bits um a um, mas é bom saber que **toda fonte bitmap funciona assim por trás dos panos**.

### O problema da "sujeira" na tela

Diferente do terminal do seu computador, o display **não limpa sozinho** o que já foi desenhado. Se você escrever um número novo em cima de um número antigo sem apagar antes, os dois vão se misturar visualmente. Por isso, sempre que um valor muda, o padrão é:

1. Apagar a área antiga (desenhando um retângulo preenchido com a cor de fundo)
2. Desenhar o valor novo no mesmo lugar

---

## 2. Circuito

O circuito é **o mesmo da Aula 1** — nenhuma mudança na ligação física. Use o mesmo `diagram.json` (`assets/diagrams/diagram-tft-esp32.json`).

> 💡O link para a simulação é: (https://wokwi.com/projects/468653382476036097)

---

## 3. Código

📁 Arquivo completo: [`aulas/codigo/aula02_main.py`](./codigo/aula02_main.py)

```python
from machine import Pin, SPI
from ST7735 import TFT
from sysfont import sysfont
import time

PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 23, 5, 2, 4
# Pico: PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 19, 17, 20, 21

spi = SPI(2, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

# text(posicao, texto, cor, fonte, tamanho)
tft.text((5, 10), "Ola, mundo!", TFT.WHITE, sysfont, 1)
tft.text((5, 30), "ESP32 + TFT", TFT.CYAN, sysfont, 2)

contador = 0
while True:
    # Apaga a area onde o numero antigo estava antes de escrever o novo
    tft.fillrect((5, 70), (110, 12), TFT.BLACK)
    tft.text((5, 70), "n = " + str(contador), TFT.YELLOW, sysfont, 1)
    contador += 1
    time.sleep(1)
```

### Explicando o código

- `tft.text((x, y), texto, cor, fonte, tamanho)` desenha uma string começando na posição `(x, y)`;
- O parâmetro `tamanho` (aqui `1` e `2`) multiplica o tamanho de cada caractere — `2` deixa o texto com o dobro da largura e altura;
- Note o `tft.fillrect(...)` **antes** de cada atualização do contador — sem essa linha, os números ficariam sobrepostos.

---

## 4. Experimento

1. Remova a linha `tft.fillrect(...)` que apaga o contador antigo e rode novamente. O que acontece na tela depois de alguns segundos?
2. Qual é a largura aproximada, em pixels, de "Ola, mundo!" com tamanho `1`? *(Dica: `Width` da fonte × número de caracteres)*
3. O que acontece se você tentar desenhar texto numa posição `x` muito próxima da borda direita da tela (128 pixels de largura)?

---

## 5. Desafio

**Desafio principal:** modifique o código para mostrar, junto com o contador, um texto que muda de cor a cada 10 números (por exemplo, branco de 0 a 9, amarelo de 10 a 19, vermelho de 20 a 29...).

**Desafio bônus:** ao invés de um contador, mostre o tempo decorrido desde que o programa começou, formatado como `MM:SS` (minutos:segundos). *(Dica: use `time.ticks_ms()` e `time.ticks_diff()`.)*

---

## Resumo da aula

- Fontes bitmap guardam o desenho de cada caractere como uma matriz de bits
- `tft.text()` cuida de converter texto em pixels usando essa matriz
- Toda vez que um valor exibido muda, é preciso **apagar a área antiga antes de desenhar a nova** — o display não faz isso sozinho

---

*← [Aula 1](./aula01-fundamentos-spi.md) | [Índice](../README.md) | Próxima → [Aula 3: Linhas, retângulos e círculos](./aula03-linhas-retangulos-circulos.md)*
