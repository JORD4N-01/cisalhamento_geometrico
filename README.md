# Cisalhamento Geométrico

Projeto acadêmico para demonstrar visualmente as transformações geométricas de cisalhamento horizontal e vertical sobre figuras 2D no plano cartesiano, com interface web moderna.

## Descrição

Este projeto implementa a transformação de cisalhamento (*shear*), que deforma uma figura deslocando seus pontos proporcionalmente à distância de um eixo de referência, sem alterar a área da figura.

### Fórmulas Implementadas

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

## Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.10+ | Backend e cálculos |
| NumPy | latest | Cálculo matricial e transformações |
| Eel | latest | Comunicação entre Python e JavaScript |
| HTML5/CSS3 | - | Markup e estilos da interface |
| JavaScript (ES6+) | - | Lógica frontend e renderização Canvas |
| Canvas API | - | Renderização 2D dos gráficos |

## Instalação

1. Clone ou baixe o projeto:
```bash
git clone <repositório>
cd cisalhamento_geometrico
```

2. Instale as dependências:
```bash
pip install numpy eel
```

> **Eel** é uma biblioteca que permite criar aplicações desktop com Python no backend e HTML/CSS/JavaScript no frontend, comunicando-se através de uma ponte nativa.

## Como Executar

```bash
python cisalhamento.py
```

## Funcionalidades

### Figuras Disponíveis
- **Quadrado**: [-2,-2], [2,-2], [2,2], [-2,2]
- **Triângulo**: [0,3], [-3,-2], [3,-2]
- **Casa**: [-2,-2], [2,-2], [2,1], [0,3], [-2,1]

### Modos de Cisalhamento
- **Horizontal**: Aplica x' = x + shx·y (deslocamento horizontal proporcional a Y)
- **Vertical**: Aplica y' = y + shy·x (deslocamento vertical proporcional a X)
- **Ambos**: Combina ambas as transformações sequencialmente

### Interface Moderna
- **Tema Dark**: Interface profissional com Chromium embutido
- **Header**: Título "Cisalhamento Geométrico" e instituição "CIESA · Manaus"
- **Footer**: Legenda visual de cores (original, transformado, deslocamento)
- **Canvas 2D**: Renderização em tempo real com:
  - Grade cartesiana
  - Figura original (cinza tracejado)
  - Figura transformada (azul sólido)
  - Linhas de deslocamento por vértice (vermelho)

### Controles da Interface
- **Tipo de cisalhamento**: Seleção via radio buttons
- **Fatores**: Sliders modernos para `shx` e `shy` (range: -3.0 a 3.0, step: 0.1)
- **Figura**: Seleção entre as três figuras disponíveis
- **Visualização em tempo real**:
  - Matriz de transformação 3×3 (coordenadas homogêneas)
  - Coordenadas dos vértices com precisão completa
- **Botão Resetar**: Retorna aos valores iniciais (shx=1, shy=0, Quadrado, Horizontal)

## Comportamento Esperado

- Ao iniciar, exibe o **quadrado** com **cisalhamento horizontal** e fator `shx = 1.0`
- Interface web com tema **dark** moderno e profissional (Chromium embutido via Eel)
- Sliders respondem em tempo real:
  - Modo **Horizontal**: slider `shx` ativo, `shy` inativo
  - Modo **Vertical**: slider `shy` ativo, `shx` inativo
  - Modo **Ambos**: ambos sliders ativos
- Canvas redesenha automaticamente ao detectar mudança
- Figura original permanece visível em cinza para comparação
- Linhas pontilhadas mostram o deslocamento de cada vértice
- Matriz de transformação (3×3) atualizada dinamicamente
- Coordenadas listadas com precisão completa (floats)
- Fontes Segoe UI para textos de interface, Courier New para dados técnicos

## Estrutura do Projeto

```
cisalhamento_geometrico/
├── CLAUDE.md              # Contexto do projeto para IA
├── cisalhamento.py        # Backend Python com Eel
├── README.md              # Este arquivo — Documentação do projeto
├── web/                   # Frontend web
│   ├── index.html         # Página principal (estrutura HTML)
│   ├── style.css          # Estilos da interface (tema dark)
│   └── script.js          # Lógica JavaScript e renderização Canvas
└── assets/                # Capturas de tela (opcional)
    └── preview.png
```

## Contexto Acadêmico

- **Disciplina**: Computação Gráfica / Álgebra Linear Aplicada
- **Instituição**: CIESA — Manaus, AM
- **Tema**: Transformações Geométricas 2D
- **Transformação**: Cisalhamento (item 4 da lista de projetos)

## Licença

Este projeto é desenvolvido para fins acadêmicos.
