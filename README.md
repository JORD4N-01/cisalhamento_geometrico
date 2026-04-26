# Cisalhamento Geométrico

Projeto acadêmico para demonstrar visualmente as transformações geométricas de cisalhamento horizontal e vertical sobre figuras 2D no plano cartesiano.

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
| Python | 3.10+ | Linguagem base |
| NumPy | latest | Cálculo matricial e transformações |
| Matplotlib | latest | Renderização do plano cartesiano |
| ttkbootstrap | 1.20+ | Interface gráfica moderna com tema dark |
| Tkinter | built-in | Base para ttkbootstrap |

## Instalação

1. Clone ou baixe o projeto:
```bash
git clone <repositório>
cd cisalhamento_geometrico
```

2. Instale as dependências:
```bash
pip install numpy matplotlib ttkbootstrap
```

> ttkbootstrap é uma biblioteca moderna que substitui o Tkinter padrão com componentes estilizados e temas profissionais.

## Como Executar

```bash
python cisalhamento.py
```

## Funcionalidades

### Figuras Disponíveis
- **Quadrado**: [-2,-2], [2,-2], [2,2], [-2,2]
- **Triângulo**: [0,3], [-3,-2], [3,-2]
- **Casa**: [-2,-2], [2,-2], [2,1], [0,3], [-2,1]

### Interface Moderna
- **Tema Dark**: Interface profissional com tema darkly do ttkbootstrap
- **Header**: Título "Cisalhamento Geométrico" e instituição "CIESA · Computação Gráfica"
- **Footer**: Legenda visual de cores (original, transformado, deslocamento)

### Controles da Interface
- **Tipo de cisalhamento**: Horizontal, Vertical ou Ambos
- **Fatores**: Sliders modernos para ajustar shx e shy (range: -3.0 a 3.0)
- **Figura**: Seleção entre as três figuras disponíveis
- **Visualização em tempo real**: Matriz de transformação e coordenadas dos vértices
- **Botão Resetar**: Retorna todos os valores ao estado inicial

### Comportamento Esperado
- Ao iniciar, exibe o quadrado com cisalhamento horizontal e fator `shx = 1.0`
- Interface com tema darkly moderno e profissional
- Sliders respondem em tempo real redesenhando o gráfico
- Ao trocar o modo, os sliders são habilitados/desabilitados conforme necessário
- A figura original permanece visível em cinza para comparação
- Linhas pontilhadas mostram o deslocamento de cada vértice
- Fontes Segoe UI para textos e Courier New para dados técnicos

## Estrutura do Projeto

```
cisalhamento_geometrico/
├── CLAUDE.md          # Contexto do projeto para IA
├── cisalhamento.py    # Arquivo principal com toda a implementação
├── README.md          # Documentação do projeto
└── assets/            # Capturas de tela (opcional)
```

## Contexto Acadêmico

- **Disciplina**: Computação Gráfica / Álgebra Linear Aplicada
- **Instituição**: CIESA — Manaus, AM
- **Tema**: Transformações Geométricas 2D
- **Transformação**: Cisalhamento (item 4 da lista de projetos)

## Licença

Este projeto é desenvolvido para fins acadêmicos.
