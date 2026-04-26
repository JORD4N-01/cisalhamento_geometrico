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
| Tkinter | built-in | Interface gráfica |

## Instalação

1. Clone ou baixe o projeto:
```bash
git clone <repositório>
cd cisalhamento_geometrico
```

2. Instale as dependências:
```bash
pip install numpy matplotlib
```

> Tkinter já vem incluído na instalação padrão do Python. Não requer instalação separada.

## Como Executar

```bash
python cisalhamento.py
```

## Funcionalidades

### Figuras Disponíveis
- **Quadrado**: [-2,-2], [2,-2], [2,2], [-2,2]
- **Triângulo**: [0,3], [-3,-2], [3,-2]
- **Casa**: [-2,-2], [2,-2], [2,1], [0,3], [-2,1]

### Controles da Interface
- **Tipo de cisalhamento**: Horizontal, Vertical ou Ambos
- **Fatores**: Sliders para ajustar shx e shy (range: -3.0 a 3.0)
- **Figura**: Seleção entre as três figuras disponíveis
- **Visualização em tempo real**: Matriz de transformação e coordenadas dos vértices

### Comportamento Esperado
- Ao iniciar, exibe o quadrado com cisalhamento horizontal e fator `shx = 1.0`
- Sliders respondem em tempo real redesenhando o gráfico
- Ao trocar o modo, os sliders são habilitados/desabilitados conforme necessário
- A figura original permanece visível em cinza para comparação
- Linhas pontilhadas mostram o deslocamento de cada vértice

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
