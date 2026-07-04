# Links dos projetos Wokwi por aula

Preencha esta tabela com o link do projeto Wokwi público de cada aula, após validar o `diagram.json` correspondente.

| Aula | Tema | Link Wokwi |
|------|------|------------|
| 1 | Fundamentos SPI e primeira tela | _(preencher)_ |
| 2 | Hello World — texto na tela | _(preencher)_ |
| 3 | Linhas, retângulos e círculos | _(preencher)_ |
| 4 | Triângulos e composição de ícones | _(preencher)_ |
| 5 | Barra de progresso / medidor | _(preencher)_ |
| 6 | Gráfico de linha em tempo real | _(preencher)_ |

## Como criar cada projeto Wokwi

O circuito é **o mesmo em todas as aulas** — só o código muda. Para cada aula:

1. Acesse [wokwi.com](https://wokwi.com) e crie um novo projeto **MicroPython + ESP32**
2. Substitua o `diagram.json` pelo conteúdo de `assets/diagrams/diagram-tft-esp32.json` (já inclui a dependência do chip ST7735 — veja a Aula 1)
3. Cole o código de `aulas/codigo/aulaNN_main.py` em `main.py`
4. Crie dois novos arquivos no projeto Wokwi: `ST7735.py` e `sysfont.py`, colando o conteúdo de `assets/libs/`
5. Rode a simulação, confirme que funciona, e clique em **Share** para gerar o link público
6. Cole o link nesta tabela

> 💡 Dica: depois de montar o primeiro projeto (Aula 1) e confirmar que funciona, use **"Fork"** no Wokwi para criar as próximas aulas a partir dele, só trocando o `main.py`.
