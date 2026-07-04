---
title: Como publicar este mini-curso
---

# Como publicar o Mini-curso 04

## 1. Criar o repositório no GitHub

1. Crie um repositório novo chamado `minicurso_04-embarcados` (público)
2. Arraste todos os arquivos e pastas deste material para a raiz do repositório, mantendo a estrutura de pastas (`aulas/`, `assets/`, etc.)
3. Faça o commit inicial:
   - **Título:** `Estrutura inicial do Mini-curso 04 (TFT ST7735 + MicroPython)`
   - **Descrição:** `Adiciona README, index, config Jekyll, 6 aulas, bibliotecas e diagramas Wokwi`

## 2. Ativar o GitHub Pages

1. No repositório, vá em **Settings → Pages**
2. Em **Source**, selecione a branch `main` (ou `master`) e a pasta `/ (root)`
3. Salve — o GitHub vai gerar uma URL do tipo `https://SEU-USUARIO.github.io/minicurso_04-embarcados/`

## 3. Ajustar as URLs absolutas no `index.md`

O tema **Cayman** não injeta `baseurl` automaticamente em links Markdown — por isso o `index.md` usa **URLs absolutas**. Antes de publicar, substitua todas as ocorrências de `SEU-USUARIO` pelo seu usuário/organização real do GitHub:

```
https://SEU-USUARIO.github.io/minicurso_04-embarcados/...
```

Você pode fazer isso diretamente na interface web do GitHub (editar o arquivo → usar "Find and replace" no editor).

## 4. Validar os diagramas do Wokwi

Todos os arquivos em `assets/diagrams/*.json` estão marcados como **"validar antes de publicar"**. Para cada aula:

1. Crie um novo projeto no [Wokwi](https://wokwi.com) (MicroPython + ESP32)
2. Copie o conteúdo do `diagram.json` correspondente
3. Copie o código de `aulas/codigo/aulaNN_main.py` para `main.py`
4. Copie `assets/libs/ST7735.py` e `assets/libs/sysfont.py` para o projeto Wokwi
5. Rode a simulação e confirme que o circuito e o código funcionam como esperado
6. Se precisar corrigir posições/conexões, atualize o `diagram.json` no repositório

## 5. Divulgar no Google Sites

O Google Sites **bloqueia iframes do GitHub** — a abordagem correta é usar **botões que abrem em nova aba**, apontando para a URL do GitHub Pages:

1. Na página do curso no Google Sites, insira um **botão**
2. Configure o link para `https://SEU-USUARIO.github.io/minicurso_04-embarcados/`
3. Marque a opção de abrir em **nova guia**

## Checklist final

- [ ] Repositório criado e arquivos enviados
- [ ] GitHub Pages ativado
- [ ] URLs do `index.md` corrigidas (usuário real)
- [ ] Todos os 6 `diagram.json` validados no Wokwi
- [ ] Botão no Google Sites configurado para abrir em nova aba
