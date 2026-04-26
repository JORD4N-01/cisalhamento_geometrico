# CLAUDE.md — Cisalhamento Geométrico

Arquivo de contexto do projeto para uso com Claude (IA). Descreve o propósito, estrutura, tecnologias e convenções do projeto.

---

## Visão geral do projeto

**Nome:** Cisalhamento Geométrico  
**Tipo:** Projeto acadêmico — Computação Gráfica / Álgebra Linear  
**Linguagem:** Python 3.10+  
**Objetivo:** Implementar e visualizar interativamente as transformações geométricas de cisalhamento horizontal e vertical sobre figuras 2D no plano cartesiano.

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
| Python | 3.10+ | Linguagem base |
| NumPy | latest | Cálculo matricial e transformações |
| Matplotlib | latest | Renderização do plano cartesiano |
| ttkbootstrap | 1.20+ | Interface gráfica moderna com tema dark |
| Tkinter | built-in | Base para ttkbootstrap |

### Instalação das dependências

```bash
pip install numpy matplotlib ttkbootstrap
```

> ttkbootstrap é uma biblioteca moderna que substitui o Tkinter padrão com componentes estilizados e temas profissionais.

---

## Estrutura do projeto

```
cisalhamento/
├── CLAUDE.md          # Este arquivo
├── cisalhamento.py    # Arquivo principal
├── README.md          # Documentação do projeto
└── assets/            # Capturas de tela (opcional)
    └── preview.png
```

---

## Estrutura do código (`cisalhamento.py`)

### Funções matemáticas

```python
def cisalhamento_horizontal(pontos: np.ndarray, shx: float) -> np.ndarray:
    """Aplica x' = x + shx·y para cada vértice."""

def cisalhamento_vertical(pontos: np.ndarray, shy: float) -> np.ndarray:
    """Aplica y' = y + shy·x para cada vértice."""

def aplicar_transformacao(pontos: np.ndarray, shx: float, shy: float) -> np.ndarray:
    """Combina horizontal e vertical (modo Ambos)."""
```

### Figuras disponíveis

```python
FIGURAS = {
    "Quadrado":  [(-2,-2), (2,-2), (2,2), (-2,2)],
    "Triângulo": [(0,3), (-3,-2), (3,-2)],
    "Casa":      [(-2,-2), (2,-2), (2,1), (0,3), (-2,1)]
}
```

### Interface ttkbootstrap

```
Janela principal (ttk.Window com tema darkly)
├── Header — título e instituição
├── Frame principal
│   ├── Frame esquerdo — controles
│   │   ├── LabelFrame "Controles"
│   │   │   ├── LabelFrame "Tipo de cisalhamento"
│   │   │   │   ├── Radiobutton: Horizontal
│   │   │   │   ├── Radiobutton: Vertical
│   │   │   │   └── Radiobutton: Ambos
│   │   │   ├── LabelFrame "Fatores"
│   │   │   │   ├── Label: shx
│   │   │   │   ├── Scale (slider) shx  [-3.0 a 3.0]
│   │   │   │   ├── Label: valor shx
│   │   │   │   ├── Label: shy
│   │   │   │   ├── Scale (slider) shy  [-3.0 a 3.0]
│   │   │   │   └── Label: valor shy
│   │   │   ├── LabelFrame "Figura"
│   │   │   │   ├── Radiobutton: Quadrado
│   │   │   │   ├── Radiobutton: Triângulo
│   │   │   │   └── Radiobutton: Casa
│   │   │   ├── Button: Resetar
│   │   │   ├── LabelFrame "Matriz de Transformação"
│   │   │   │   └── Label: matriz formatada (Courier New)
│   │   │   └── LabelFrame "Coordenadas Transformadas"
│   │   │       └── Label: coordenadas (Courier New)
│   │   └── Frame direito — canvas
│   │       └── FigureCanvasTkAgg (Matplotlib embutido)
└── Footer — legenda de cores
```

### Fluxo de execução

```
Usuário ajusta controle (slider / botão)
        ↓
callback() atualiza shx, shy, modo ou figura
        ↓
aplicar_transformacao() recalcula os vértices
        ↓
Matplotlib redesenha o plano:
  - Figura original em cinza tracejado
  - Figura transformada em azul sólido
  - Linhas pontilhadas de deslocamento por vértice
        ↓
Labels atualizam a matriz e as coordenadas na interface
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
cd cisalhamento

# Instalar dependências
pip install numpy matplotlib

# Executar
python cisalhamento.py
```

---

## Comportamento esperado da interface

- Ao iniciar, exibe o **quadrado** com **cisalhamento horizontal** e fator `shx = 1.0`
- Interface com tema **darkly** moderno e profissional
- Sliders respondem em tempo real redesenhando o gráfico
- Ao trocar o modo para **Vertical**, o slider `shx` é desabilitado e `shy` é ativado
- No modo **Ambos**, os dois sliders ficam ativos simultaneamente
- A matriz de transformação é atualizada dinamicamente na interface
- As coordenadas dos vértices transformados são exibidas com 2 casas decimais
- **Botão Resetar** retorna todos os valores ao estado inicial
- **Footer** com legenda visual de cores (original, transformado, deslocamento)

---

## Contexto acadêmico

- **Disciplina:** Computação Gráfica / Álgebra Linear Aplicada
- **Instituição:** CIESA — Manaus, AM
- **Tema do trabalho:** Transformações Geométricas 2D
- **Transformação implementada:** Cisalhamento (item 4 da lista de projetos)

---

## Observações para o Claude

- O projeto é **acadêmico e introdutório** — priorizar clareza sobre performance
- Toda a lógica deve estar em **um único arquivo** `cisalhamento.py`
- Usar `ttkbootstrap` com tema **darkly** para interface moderna e profissional
- Usar `FigureCanvasTkAgg` para embutir o gráfico Matplotlib dentro da janela ttkbootstrap
- O canvas Matplotlib deve ser redesenhado a cada interação do usuário via `canvas.draw()`
- Manter a figura original sempre visível em cinza para comparação visual
- Implementar **header** com título e instituição, e **footer** com legenda de cores
- Usar fontes **Segoe UI** para textos e **Courier New** para dados técnicos
