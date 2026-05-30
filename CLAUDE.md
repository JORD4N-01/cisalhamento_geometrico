# CLAUDE.md — Cisalhamento Geométrico

Arquivo de contexto do projeto para uso com Claude (IA). Descreve o propósito, estrutura, tecnologias e convenções do projeto.

---

## Visão geral do projeto

**Nome:** Cisalhamento Geométrico  
**Tipo:** Projeto acadêmico — Computação Gráfica / Álgebra Linear  
**Linguagem:** Python 3.10+ (Backend) + HTML/CSS/JavaScript (Frontend)  
**Objetivo:** Implementar e visualizar interativamente as transformações geométricas de cisalhamento horizontal e vertical sobre figuras 2D no plano cartesiano através de uma interface web moderna.

---

## Descrição

Este projeto demonstra a transformação de cisalhamento (*shear*), que deforma uma figura deslocando seus pontos proporcionalmente à distância de um eixo de referência, sem alterar a área da figura.

### Fórmulas implementadas

**Cisalhamento horizontal:**
```
x' = x + shx · y
y' = y
```

**Cisalhamento vertical:**
```
x' = x
y' = y + shy · x
```

**Em forma matricial (coordenadas homogêneas):**
```
Horizontal:        Vertical:
| 1  shx  0 |     | 1    0  0 |
| 0   1   0 |     | shy  1  0 |
| 0   0   1 |     | 0    0  1 |
```

---

## Tecnologias utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.10+ | Backend e cálculos |
| NumPy | latest | Cálculo matricial e transformações |
| Eel | latest | Comunicação entre Python e JavaScript |
| HTML5/CSS3 | - | Markup e estilos da interface |
| JavaScript (ES6+) | - | Lógica frontend e renderização Canvas |
| Canvas API | - | Renderização 2D dos gráficos |

### Instalação das dependências

```bash
pip install numpy eel
```

> **Eel** é uma biblioteca que permite criar aplicações desktop com Python no backend e HTML/CSS/JavaScript no frontend, comunicando-se através de uma ponte nativa. O frontend roda em um navegador Chromium embutido.

---

## Estrutura do projeto

```
cisalhamento_geometrico/
├── CLAUDE.md              # Este arquivo — contexto para IA
├── cisalhamento.py        # Backend Python com Eel
├── README.md              # Documentação do projeto
├── web/                   # Frontend web
│   ├── index.html         # Página principal
│   ├── style.css          # Estilos da interface
│   └── script.js          # Lógica JavaScript e Canvas
└── assets/                # Capturas de tela (opcional)
    └── preview.png
```

---

## Arquitetura e Componentes

### Backend Python (`cisalhamento.py`)

Implementa a lógica matemática de transformações e serve uma API para o frontend via Eel.

**Funções principais:**
- `cisalhamento_horizontal(pontos, shx)` — Aplica x' = x + shx·y
- `cisalhamento_vertical(pontos, shy)` — Aplica y' = y + shy·x
- `aplicar_transformacao(pontos, shx, shy, modo)` — Orquestra as transformações
- `obter_matriz_transformacao(shx, shy, modo)` — Retorna a matriz 3×3
- `calcular(shx, shy, figura, modo)` — **Função exposta via Eel** — Calcula transformação e retorna JSON com:
  - Vértices originais
  - Vértices transformados
  - Matriz de transformação
  - Coordenadas formatadas de cada vértice

**Figuras disponíveis:**
```python
FIGURAS = {
    "Quadrado":  [(-2,-2), (2,-2), (2,2), (-2,2)],
    "Triângulo": [(0,3), (-3,-2), (3,-2)],
    "Casa":      [(-2,-2), (2,-2), (2,1), (0,3), (-2,1)]
}
```

### Frontend Web (`web/`)

Interface moderna renderizada em Canvas API com comunicação via Eel.

**Estrutura HTML (index.html):**
```
<body>
  <header>Título e Instituição</header>
  <div class="main">
    <aside class="controls">
      - Seletor: Tipo de Cisalhamento (Horizontal/Vertical/Ambos)
      - Sliders: shx [-3, 3], shy [-3, 3]
      - Seletor: Figura (Quadrado/Triângulo/Casa)
      - Botão: Resetar
      - Exibição: Matriz de Transformação (3×3)
      - Exibição: Coordenadas Transformadas
    </aside>
    <section class="canvas-container">
      <canvas id="canvas"></canvas>
    </section>
  </div>
  <footer>Legenda de cores</footer>
</body>
```

**Lógica JavaScript (script.js):**
- Gerencia estado da aplicação (shx, shy, figura, modo)
- Listeners em controles para atualizar estado
- Chamadas assíncronas para `eel.calcular()` (backend Python)
- Renderização Canvas:
  - Grade cartesiana em cinza
  - Figura original em cinza tracejado
  - Figura transformada em azul sólido
  - Linhas de deslocamento em vermelho

**Estilos CSS (style.css):**
- Tema dark profissional
- Layout flexbox responsivo
- Sliders e controles estilizados
- Fonte Segoe UI para interface, Courier New para dados técnicos

### Fluxo de execução (Eel Bridge)

```
Usuário interage com controle na página web
        ↓
JavaScript listener captura mudança (change/input event)
        ↓
Atualiza appState e valida valores
        ↓
Chamada assíncrona: await eel.calcular(shx, shy, figura, modo)()
        ↓
[PONTE EEL]
        ↓
Python: função calcular() processa com NumPy
        ↓
Retorna JSON com dados calculados
        ↓
[PONTE EEL]
        ↓
JavaScript recebe resultado
        ↓
Atualiza UI:
  - Canvas redesenhado com requestAnimationFrame
  - Figura original em cinza
  - Figura transformada em azul
  - Linhas de deslocamento em vermelho
  - Matriz formatada
  - Coordenadas listadas
```

---

## Convenções do código

- Nomes de variáveis e funções em **snake_case** em português
- Comentários em português
- Cada função deve ter docstring explicando a transformação aplicada
- Separar claramente a lógica matemática da interface gráfica
- Não misturar código Tkinter dentro das funções de cálculo

---

## Como executar

```bash
# Clonar ou baixar o projeto
cd cisalhamento_geometrico

# Instalar dependências
pip install numpy eel

# Executar
python cisalhamento.py
```

O servidor Eel abrirá automaticamente uma janela com a interface web em `http://localhost:8000`.

---

## Comportamento esperado da interface

- Ao iniciar, exibe o **quadrado** com **cisalhamento horizontal** e fator `shx = 1.0`
- Interface web com tema **dark** moderno e profissional (Chromium embutido)
- Sliders respondem em tempo real:
  - Modo **Horizontal**: slider `shx` ativo, `shy` inativo (padrão 0)
  - Modo **Vertical**: slider `shy` ativo, `shx` inativo (padrão 0)
  - Modo **Ambos**: ambos sliders ativos
- Canvas redesenha automaticamente ao detectar mudança (com debounce)
- Matriz de transformação (3×3) atualizada dinamicamente
- Coordenadas de cada vértice exibidas com precisão completa (floats)
- **Botão Resetar**: retorna aos valores iniciais (shx=1, shy=0, Quadrado, Horizontal)
- **Footer**: legenda visual com cores das linhas (cinza=original, azul=transformado, vermelho=deslocamento)

---

## Contexto acadêmico

- **Disciplina:** Computação Gráfica / Álgebra Linear Aplicada
- **Instituição:** CIESA — Manaus, AM
- **Tema do trabalho:** Transformações Geométricas 2D
- **Transformação implementada:** Cisalhamento (item 4 da lista de projetos)

---

## Observações para o Claude

- O projeto é **acadêmico e introdutório** — priorizar clareza e correteza matemática
- **Backend** em `cisalhamento.py`: lógica pura com NumPy, funções expostas via `@eel.expose`
- **Frontend** em `web/`: HTML5/CSS3 estruturado, JavaScript puro (sem frameworks)
- Canvas API para renderização 2D — não usar bibliotecas gráficas adicionais
- Manter a figura original sempre visível em cinza para comparação visual
- Implementar **header** com título "Cisalhamento Geométrico" e "CIESA Manaus"
- Implementar **footer** com legenda de cores (original, transformado, deslocamento)
- Usar **Segoe UI** para textos de interface, **Courier New** para dados técnicos
- Garantir que a comunicação Eel seja assíncrona (`async/await` em JavaScript)
- Valores de entrada: `shx, shy ∈ [-3, 3]` com step 0.1
