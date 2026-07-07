---
title: Mini-curso 04 — Display TFT com MicroPython
---

![Banner do curso](https://rogeriomb-hub.github.io/minicurso_04-embarcados/assets/banner.png)

# Display TFT (ST7735) com MicroPython

Bem-vindo ao Mini-curso 04! Aqui você vai aprender a controlar um **display TFT SPI de 1.8"** usando **MicroPython**, desenhando formas geométricas, escrevendo texto e plotando gráficos — no **ESP32** e no **Raspberry Pi Pico**.

Todas as aulas podem ser feitas **simulando no Wokwi**, direto do navegador, sem precisar de nenhuma peça física.

## Aulas

| # | Aula | Tema |
|---|------|------|
| 1 | [Fundamentos SPI e primeira tela](https://rogeriomb-hub.github.io/minicurso_04-embarcados/aulas/aula01-fundamentos-spi) | Pinagem, biblioteca, `fill_screen` |
| 2 | [Hello World — texto na tela](https://rogeriomb-hub.github.io/minicurso_04-embarcados/aulas/aula02-hello-world-texto) | Fontes e cores |
| 3 | [Linhas, retângulos e círculos](https://rogeriomb-hub.github.io/minicurso_04-embarcados/aulas/aula03-linhas-retangulos-circulos) | Primitivas de desenho |
| 4 | [Triângulos e composição de ícones](https://rogeriomb-hub.github.io/minicurso_04-embarcados/aulas/aula04-triangulos-composicao) | Combinação de formas |
| 5 | [Barra de progresso / medidor](https://rogeriomb-hub.github.io/minicurso_04-embarcados/aulas/aula05-barra-progresso) | Mapeamento de valores |
| 6 | [Gráfico de linha em tempo real](https://rogeriomb-hub.github.io/minicurso_04-embarcados/aulas/aula06-grafico-tempo-real) | Buffer e plotagem |


## Pré-requisitos

- Ter feito (ou revisado) o **Mini-curso 01** — lógica digital e operadores bitwise
- Noções básicas de MicroPython (variáveis, funções, laços `for`/`while`)
- Uma conta gratuita no [Wokwi](https://wokwi.com) (ou hardware físico: ESP32/Pico + display TFT 1.8" ST7735)

## Como simular no Wokwi

O Wokwi não tem um componente pronto para o ST7735 — usamos um **chip criado pela comunidade**. O passo a passo completo está na **Aula 1**, incluindo o `diagram.json` já configurado com a dependência do chip.
