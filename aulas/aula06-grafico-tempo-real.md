---
title: Aula 6 — Gráfico de linha em tempo real
---

# Aula 6 — Gráfico de linha em tempo real

> **Duração estimada:** 30 minutos
> **Módulo:** 3 de 3 — Gráficos dinâmicos

---

## Objetivos

Ao final desta aula você será capaz de:

- Manter um **buffer** (lista) com um histórico de valores lidos
- Desenhar um gráfico de linha conectando pontos consecutivos do buffer
- Entender a ideia de um "buffer andando" (a cada nova leitura, descarta-se a mais antiga)

---

## 1. Conceito

### De uma barra a um gráfico

Na Aula 5, mostramos **um único valor** por vez (a leitura mais recente). Um gráfico de linha em tempo real — como um osciloscópio — mostra o **histórico** de valores, permitindo ver como eles mudaram ao longo do tempo.

Para isso, precisamos guardar não só a leitura atual, mas um conjunto das últimas N leituras, em uma lista (nosso **buffer**):

```python
valores = [0] * 120   # buffer com 120 posicoes, uma para cada coluna do grafico
```

### O buffer "andando" (buffer circular simplificado)

A cada nova leitura, queremos:

1. Descartar o valor **mais antigo** (posição 0 da lista)
2. Adicionar o valor **novo** no final da lista

```python
valores.pop(0)      # remove o mais antigo
valores.append(novo_valor)   # adiciona o mais recente no final
```

Esse padrão faz o gráfico parecer estar **rolando para a esquerda** a cada atualização — o valor mais novo sempre aparece à direita, empurrando o histórico para trás.

### Conectando os pontos

Para desenhar a linha do gráfico, percorremos o buffer aos pares (posição `i` e posição `i+1`) e ligamos cada par de pontos com `tft.line()` — exatamente como fizemos com os triângulos na Aula 4, só que agora com muito mais segmentos de reta.

---

## 2. Circuito

O circuito é **o mesmo da Aula 5** (com o potenciômetro). Use `assets/diagrams/diagram-tft-esp32-pot.json`.

> 💡 [Abrir simulação no Wokwi ↗](https://wokwi.com/projects/468654164907751425)
---

## 3. Código

📁 Arquivo completo: [`aulas/codigo/aula06_main.py`](./codigo/aula06_main.py)

```python
from machine import Pin, SPI, ADC
from ST7735 import TFT
import time

PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 23, 5, 2, 4
PIN_POT = 34
# Pico: PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 19, 17, 20, 21
# Pico: PIN_POT = 26

spi = SPI(2, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))
# Pico: spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
#              sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

pot = ADC(Pin(PIN_POT))
pot.atten(ADC.ATTN_11DB)
# Pico: pot = ADC(Pin(PIN_POT))

GRAFICO_X, GRAFICO_Y = 4, 10
GRAFICO_LARGURA, GRAFICO_ALTURA = 120, 130

valores = [0] * GRAFICO_LARGURA

tft.rect((GRAFICO_X - 1, GRAFICO_Y - 1),
         (GRAFICO_LARGURA + 2, GRAFICO_ALTURA + 2), TFT.WHITE)

while True:
    leitura = pot.read()
    altura_px = int((leitura / 4095) * (GRAFICO_ALTURA - 1))

    valores.pop(0)
    valores.append(altura_px)

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
```

> ⚠️ **Nota de correção:** se o gráfico parecer andar da direita para a esquerda (o valor mais novo entrando pela esquerda, ao invés da direita), é a orientação padrão do display — bem comum em módulos ST7735, já que varia conforme o fabricante/tab do chip. O trecho acima já inclui a correção: invertemos o mapeamento `coluna → x` para compensar. Se ainda assim sair invertido no seu display físico, também é possível resolver chamando `tft.rotation(0)`, `tft.rotation(1)`, `tft.rotation(2)` ou `tft.rotation(3)` logo após `tft.initr()` até encontrar a orientação correta.

### Explicando o código

- `valores[coluna]` guarda a **altura em pixels** da leitura naquela posição do gráfico — quanto maior o valor lido, mais alto (mais próximo do topo) o ponto aparece;
- A expressão `GRAFICO_ALTURA - 1 - valores[coluna]` inverte o eixo Y: como Y cresce para baixo na tela, precisamos "virar" o valor para que leituras maiores apareçam mais **acima**;
- Da mesma forma, `GRAFICO_LARGURA - 1 - coluna` inverte o eixo X, compensando a orientação espelhada do display (veja a nota de correção logo abaixo);
- Note que a cada iteração **todo o gráfico é apagado e redesenhado** — funciona, mas não é a forma mais eficiente (veja o desafio bônus).

---

## 4. Experimento

1. Se `GRAFICO_ALTURA = 130` e `valores[coluna] = 130`, em que posição Y (relativa ao topo do gráfico) o ponto será desenhado? E se `valores[coluna] = 0`?
2. Por que usamos `pop(0)` e `append()` ao invés de simplesmente sobrescrever `valores[0]` a cada leitura?
3. O que aconteceria com o gráfico se `time.sleep_ms(50)` fosse trocado por `time.sleep_ms(5)`? Pense tanto no visual quanto no desempenho.

---

## 5. Desafio

**Desafio principal:** adicione uma segunda linha horizontal fixa no meio do gráfico (50% da altura), como uma "linha de referência", para facilitar a visualização de quando o valor está acima ou abaixo da metade.

**Desafio bônus (otimização):** o código atual redesenha o gráfico **inteiro** a cada leitura, o que é desperdício — só a coluna mais nova realmente muda de posição relativa. Pesquise a técnica de **scroll de hardware** do ST7735 (métodos `setvscroll()` e `vscroll()`, presentes em `ST7735.py`) ou implemente uma versão que desenha **apenas a nova coluna**, deslocando o restante do desenho com `tft.image()`. Essa otimização é o tipo de problema que aparece em projetos reais de instrumentação com displays pequenos.

---

## Resumo da aula

- Um **buffer** guarda um histórico de valores, permitindo desenhar um gráfico ao invés de um único ponto
- O padrão `pop(0)` + `append()` implementa um buffer "andando", descartando o valor mais antigo a cada nova leitura
- É preciso inverter o eixo Y ao converter um valor lido em uma posição de pixel, já que Y cresce para baixo na tela
- Redesenhar a tela inteira a cada atualização funciona, mas tem um custo de desempenho — otimizações como scroll de hardware existem para casos onde isso importa

---

## 🎉 Fim do Mini-curso 04!

Parabéns por completar as 6 aulas! Você agora sabe:

- Ligar e inicializar um display TFT SPI (ST7735) via MicroPython, no ESP32 e no Raspberry Pi Pico
- Simular o circuito no Wokwi, mesmo sem um componente nativo disponível
- Desenhar texto, formas geométricas e gráficos dinâmicos

Como próximo passo, considere combinar o que aprendeu aqui com o **Mini-curso 02** (comunicação UART) para criar um projeto que receba dados de outro dispositivo e os exiba graficamente no TFT.

---

*← [Aula 5](./aula05-barra-progresso.md) | [Índice](../README.md)*
