---
title: Aula 1 — Fundamentos SPI e primeira tela colorida
---

# Aula 1 — Fundamentos SPI e primeira tela colorida

> **Duração estimada:** 30 minutos
> **Módulo:** 1 de 3 — Fundamentos e ligação

---

## Objetivos

Ao final desta aula você será capaz de:

- Explicar o que é o barramento **SPI** e por que ele é usado por displays TFT
- Identificar cada sinal do display (SCK, MOSI, CS, DC, RST, VCC, GND) e ligá-lo corretamente ao ESP32 ou ao Raspberry Pi Pico
- Adicionar o **chip customizado do ST7735** e a **biblioteca MicroPython** a um projeto no Wokwi
- Inicializar o display e pintar a tela inteira com uma cor sólida (`fill`)

---

## 1. Conceito

### O que é SPI?

**SPI** (*Serial Peripheral Interface*) é um barramento de comunicação série, muito usado para conectar microcontroladores a periféricos rápidos — displays, cartões SD, sensores. Diferente do I2C (que vocês usaram no Mini-curso 03), o SPI:

- Não tem endereços — cada dispositivo tem seu próprio pino **CS** (*Chip Select*) para ser "chamado";
- É mais rápido, pois usa linhas dedicadas para dados de saída (**MOSI**) e clock (**SCK**);
- Como o display TFT só *recebe* dados (não precisa responder nada de volta), não usamos o pino MISO (*Master In, Slave Out*).

### Os sinais do display TFT (ST7735)

| Sinal | Nome completo | Função |
|-------|----------------|--------|
| **SCK** | Serial Clock | Sincroniza cada bit transmitido |
| **MOSI** (ou SDA) | Master Out, Slave In | Os dados (pixels, comandos) saem do microcontrolador para o display por aqui |
| **CS** | Chip Select | Avisa ao display "a mensagem agora é para você" |
| **DC** (ou A0, DS) | Data/Command | Diz se o byte atual é um **comando** (ex: "limpe a tela") ou um **dado** (ex: "a cor deste pixel") |
| **RST** | Reset | Reinicia o controlador do display |
| **VCC / GND** | Alimentação | 3.3V e terra |

> 💡 **DC é o sinal mais "conceitual" dessa lista.** Ele existe porque o ST7735 recebe comandos e dados pela *mesma* linha (MOSI) — o DC é quem diz ao chip como interpretar o próximo byte.

---

## 2. Circuito

### Pinagem — ESP32

| Sinal TFT | Pino ESP32 |
|-----------|------------|
| VCC | 3V3 |
| GND | GND |
| SCK | GPIO 18 |
| MOSI (SDA) | GPIO 23 |
| CS | GPIO 5 |
| DC (A0/DS) | GPIO 2 |
| RST | GPIO 4 |

### Pinagem — Raspberry Pi Pico

| Sinal TFT | Pino Pico |
|-----------|-----------|
| VCC | 3V3(OUT) |
| GND | GND |
| SCK | GP18 |
| MOSI (SDA) | GP19 |
| CS | GP17 |
| DC (A0/DS) | GP20 |
| RST | GP21 |

> Repare que a numeração segue o mesmo padrão nas duas placas (SCK → MOSI → CS → DC → RST em sequência), para ficar mais fácil de memorizar.

---

## 3. Simulando no Wokwi

⚠️ **Importante:** o Wokwi **não tem um componente pronto** para o ST7735 (diferente do LCD e do OLED que vocês usaram no Mini-curso 03). Vamos usar um **chip criado pela comunidade** ([`martysweet/st7735-wokwi-chip`](https://github.com/martysweet/st7735-wokwi-chip), licença MIT).

> 💡 [Abrir simulação no Wokwi ↗](https://wokwi.com/projects/468652961129872385)

### Passo a passo

1. Acesse [wokwi.com](https://wokwi.com) e crie um novo projeto **"MicroPython on ESP32"**
2. Abra o arquivo `diagram.json` do projeto e **substitua todo o conteúdo** pelo `diagram.json` abaixo (também disponível em `assets/diagrams/diagram-tft-esp32.json`)
3. Crie dois novos arquivos no projeto, com o botão **"+"** ao lado da lista de arquivos:
   - `ST7735.py` → cole o conteúdo de `assets/libs/ST7735.py`
   - `sysfont.py` → cole o conteúdo de `assets/libs/sysfont.py`
4. Cole o código da seção 4 abaixo em `main.py`
5. Clique em **▶ Run** para iniciar a simulação

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
    ["display:GND", "esp:GND.1", "black", []]
  ],
  "dependencies": {
    "chip-st7735": "github:martysweet/st7735-wokwi-chip@1.0.4"
  }
}
```

> A chave `"dependencies"` é o que diz ao Wokwi para baixar e compilar o chip do ST7735 automaticamente — você não precisa compilar nada manualmente.

---

## 4. Código

📁 Arquivo completo: [`aulas/codigo/aula01_main.py`](./codigo/aula01_main.py)

```python
from machine import Pin, SPI
from ST7735 import TFT
import time

# --- Pinagem (ESP32) ---
PIN_SCK  = 18
PIN_MOSI = 23
PIN_CS   = 5
PIN_DC   = 2
PIN_RST  = 4

# Pico: PIN_SCK, PIN_MOSI, PIN_CS, PIN_DC, PIN_RST = 18, 19, 17, 20, 21

spi = SPI(2, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))
# Pico: spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
#              sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI))

tft = TFT(spi, PIN_DC, PIN_RST, PIN_CS)
tft.initr()      # inicializa o controlador como ST7735
tft.rgb(True)

cores = [TFT.RED, TFT.GREEN, TFT.BLUE, TFT.WHITE, TFT.BLACK]
nomes = ["vermelho", "verde", "azul", "branco", "preto"]

while True:
    for cor, nome in zip(cores, nomes):
        print("Pintando a tela de", nome)
        tft.fill(cor)
        time.sleep(1)
```

### Explicando o código

- `SPI(2, ...)` cria o barramento SPI usando o periférico de hardware nº 2 do ESP32 (chamado de VSPI), nos pinos que definimos;
- `TFT(spi, PIN_DC, PIN_RST, PIN_CS)` cria o objeto que representa nosso display, associando-o aos três pinos de controle;
- `tft.initr()` envia a sequência de comandos de inicialização específica do ST7735 (existem variantes `initb()`, `initg()`, `initb2()` para outras versões de fabricação do chip — se as cores saírem estranhas na bancada real, é o primeiro lugar para investigar);
- `tft.fill(cor)` pinta a tela inteira com uma cor sólida.

---

## 5. Experimento

Responda no seu caderno ou compartilhe com o professor:

1. O que acontece se você trocar `tft.rgb(True)` por `tft.rgb(False)`? Por que isso acontece?
2. O pino **DC** está em nível baixo ou alto quando o display está recebendo um **comando**? E quando está recebendo um **dado** (cor de pixel)? *(Dica: veja o método `_writecommand` dentro de `ST7735.py`)*
3. Por que o display **não precisa** de um pino MISO?

---

## 6. Desafio

**Desafio principal:** modifique o código para que a tela cicle apenas entre duas cores (por exemplo, vermelho e azul), com uma pausa de 0.5 segundos entre cada uma — como um alerta piscante.

**Desafio bônus:** crie sua própria cor personalizada usando `ST7735.TFTColor(r, g, b)` (onde r, g, b vão de 0 a 255) e adicione-a à lista de cores. Tente criar um tom de laranja ou roxo.

---

## Resumo da aula

- O **SPI** conecta o microcontrolador ao display usando linhas dedicadas de clock (SCK) e dados (MOSI), mais um pino de seleção (CS)
- O pino **DC** distingue comandos de dados na mesma linha MOSI
- O Wokwi não tem um componente nativo para o ST7735 — usamos um **chip customizado da comunidade**, referenciado via `dependencies` no `diagram.json`
- `tft.fill(cor)` pinta a tela inteira — é a operação mais básica de desenho

---

*[Índice](../README.md) | Próxima → [Aula 2: Hello World — texto na tela](./aula02-hello-world-texto.md)*
