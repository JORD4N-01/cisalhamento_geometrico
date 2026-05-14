#!/usr/bin/env python3
"""
Cisalhamento Geométrico - Transformações 2D com Eel
Backend Python para interface web moderna com HTML/CSS/JS

Este módulo implementa as transformações geométricas de cisalhamento (shear) 
horizontal e vertical sobre figuras 2D no plano cartesiano. As transformações 
são calculadas usando coordenadas homogêneas e matrizes 3×3.

Fórmulas implementadas:
    Cisalhamento Horizontal: x' = x + shx·y, y' = y
    Cisalhamento Vertical:   x' = x, y' = y + shy·x

O módulo utiliza Eel para comunicação entre backend Python (NumPy) e 
frontend web (HTML/CSS/JavaScript com Canvas API).

Uso:
    python cisalhamento.py
    
    Abre uma janela com interface web em http://localhost:8000
"""

import eel
import numpy as np

# Inicializar Eel apontando para a pasta web
eel.init('web')

# Figuras disponíveis (vértices em coordenadas cartesianas)
FIGURAS = {
    "Quadrado": [(-2, -2), (2, -2), (2, 2), (-2, 2)],
    "Triângulo": [(0, 3), (-3, -2), (3, -2)],
    "Casa": [(-2, -2), (2, -2), (2, 1), (0, 3), (-2, 1)]
}

def cisalhamento_horizontal(pontos: np.ndarray, shx: float) -> np.ndarray:
    """
    Aplica a transformação de cisalhamento horizontal aos vértices.
    
    A transformação horizontal desloca cada ponto proporcionalmente à sua 
    coordenada Y, mantendo a coordenada Y inalterada.
    
    Fórmula: x' = x + shx·y, y' = y
    
    Matriz de transformação (coordenadas homogêneas):
        ⎡ 1  shx  0 ⎤
        ⎢ 0   1   0 ⎥
        ⎣ 0   0   1 ⎦
    
    Args:
        pontos: Array NumPy com shape (n, 2) contendo as coordenadas (x, y).
        shx: Fator de cisalhamento horizontal. Valores maiores causam maior deformação.
    
    Returns:
        Array NumPy com shape (n, 2) contendo as coordenadas transformadas.
    
    Exemplo:
        >>> pontos = np.array([[0, 0], [1, 0], [1, 1]])
        >>> resultado = cisalhamento_horizontal(pontos, 1.0)
        >>> resultado
        array([[0., 0.],
               [1., 0.],
               [2., 1.]])
    """
    matriz = np.array([
        [1, shx, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    
    # Converter para coordenadas homogêneas
    pontos_homogeneos = np.column_stack([pontos, np.ones(len(pontos))])
    
    # Aplicar transformação: P' = P · M^T
    transformados = pontos_homogeneos @ matriz.T
    
    # Retornar apenas coordenadas x, y (descartar homogêneas)
    return transformados[:, :2]


def cisalhamento_vertical(pontos: np.ndarray, shy: float) -> np.ndarray:
    """
    Aplica a transformação de cisalhamento vertical aos vértices.
    
    A transformação vertical desloca cada ponto proporcionalmente à sua 
    coordenada X, mantendo a coordenada X inalterada.
    
    Fórmula: x' = x, y' = y + shy·x
    
    Matriz de transformação (coordenadas homogêneas):
        ⎡ 1   0   0 ⎤
        ⎢ shy  1   0 ⎥
        ⎣ 0   0   1 ⎦
    
    Args:
        pontos: Array NumPy com shape (n, 2) contendo as coordenadas (x, y).
        shy: Fator de cisalhamento vertical. Valores maiores causam maior deformação.
    
    Returns:
        Array NumPy com shape (n, 2) contendo as coordenadas transformadas.
    
    Exemplo:
        >>> pontos = np.array([[0, 0], [1, 0], [1, 1]])
        >>> resultado = cisalhamento_vertical(pontos, 1.0)
        >>> resultado
        array([[0., 0.],
               [1., 1.],
               [1., 2.]])
    """
    matriz = np.array([
        [1, 0, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ])
    
    # Converter para coordenadas homogêneas
    pontos_homogeneos = np.column_stack([pontos, np.ones(len(pontos))])
    
    # Aplicar transformação: P' = P · M^T
    transformados = pontos_homogeneos @ matriz.T
    
    # Retornar apenas coordenadas x, y (descartar homogêneas)
    return transformados[:, :2]


def aplicar_transformacao(pontos: np.ndarray, shx: float, shy: float, modo: str) -> np.ndarray:
    """
    Aplica a transformação geométrica conforme o modo especificado.
    
    Disponibiliza três modos de transformação:
    - Horizontal: Apenas cisalhamento horizontal (shx)
    - Vertical:   Apenas cisalhamento vertical (shy)
    - Ambos:      Cisalhamento horizontal E vertical sequencialmente
    
    Args:
        pontos: Array NumPy com shape (n, 2) contendo as coordenadas (x, y).
        shx: Fator de cisalhamento horizontal.
        shy: Fator de cisalhamento vertical.
        modo: Uma das strings: "Horizontal", "Vertical", "Ambos".
    
    Returns:
        Array NumPy com shape (n, 2) contendo as coordenadas transformadas.
    
    Raises:
        ValueError: Se modo não for um dos valores esperados.
    """
    if modo == "Horizontal":
        return cisalhamento_horizontal(pontos, shx)
    elif modo == "Vertical":
        return cisalhamento_vertical(pontos, shy)
    elif modo == "Ambos":
        # Aplicar ambas as transformações sequencialmente
        # Primeiro horizontal, depois vertical
        horizontal = cisalhamento_horizontal(pontos, shx)
        return cisalhamento_vertical(horizontal, shy)
    else:
        raise ValueError(f"Modo desconhecido: {modo}. Use 'Horizontal', 'Vertical' ou 'Ambos'.")


def obter_matriz_transformacao(shx: float, shy: float, modo: str) -> np.ndarray:
    """
    Retorna a matriz 3×3 de transformação no modo especificado.
    
    As matrizes utilizam coordenadas homogêneas para representar 
    transformações 2D de forma unificada.
    
    Args:
        shx: Fator de cisalhamento horizontal.
        shy: Fator de cisalhamento vertical.
        modo: Uma das strings: "Horizontal", "Vertical", "Ambos".
    
    Returns:
        Array NumPy com shape (3, 3) contendo a matriz de transformação.
        
    Referência:
        Para o modo "Ambos", a matriz resultante é H · V onde:
        - H é a matriz de cisalhamento horizontal
        - V é a matriz de cisalhamento vertical
    """
    if modo == "Horizontal":
        return np.array([
            [1, shx, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
    elif modo == "Vertical":
        return np.array([
            [1, 0, 0],
            [shy, 1, 0],
            [0, 0, 1]
        ])
    elif modo == "Ambos":
        # Matriz combinada: H · V
        # Resultado: aplicar horizontal primeiro, depois vertical
        return np.array([
            [1, shx, 0],
            [shy, 1 + shx * shy, 0],
            [0, 0, 1]
        ])
    else:
        return np.eye(3)


@eel.expose
def calcular(shx: float, shy: float, figura: str, modo: str) -> dict:
    """
    Calcula a transformação geométrica e retorna os dados formatados.
    
    Esta função é exposta ao JavaScript via Eel e serve como ponto de 
    entrada principal para o cálculo das transformações. Ela coordena:
    1. Obtenção dos vértices da figura escolhida
    2. Aplicação da transformação geométrica
    3. Cálculo da matriz resultante
    4. Formatação dos dados para retorno JSON
    
    Args:
        shx (float): Fator de cisalhamento horizontal. Intervalo: [-3, 3].
        shy (float): Fator de cisalhamento vertical. Intervalo: [-3, 3].
        figura (str): Nome da figura a transformar. Opções: "Quadrado", "Triângulo", "Casa".
        modo (str): Tipo de cisalhamento. Opções: "Horizontal", "Vertical", "Ambos".
    
    Returns:
        dict: Dicionário com a seguinte estrutura:
            {
                "original": [[x1, y1], [x2, y2], ...],  # Vértices originais
                "transformado": [[x1', y1'], [x2', y2'], ...],  # Vértices após transformação
                "matriz": [[m00, m01, m02], [m10, m11, m12], [m20, m21, m22]],  # Matriz 3×3
                "coords": [  # Lista com informações de cada vértice
                    {
                        "label": "P1",
                        "orig": [x, y],
                        "trans": [x', y']
                    },
                    ...
                ]
            }
    
    Exemplos de uso (via JavaScript):
        const resultado = await eel.calcular(1.0, 0.0, "Quadrado", "Horizontal")();
        const resultado = await eel.calcular(0.0, 1.5, "Triângulo", "Vertical")();
        const resultado = await eel.calcular(1.0, 1.0, "Casa", "Ambos")();
    
    Notas:
        - Se a figura especificada não existir, usa "Quadrado" como padrão.
        - Os valores das coordenadas são retornados como floats com precisão completa.
        - A matriz retornada é sempre 3×3 (coordenadas homogêneas).
    """
    # 1. Obter vértices da figura escolhida
    if figura not in FIGURAS:
        figura = "Quadrado"
    
    pontos_originais = np.array(FIGURAS[figura])
    
    # 2. Aplicar transformação conforme o modo
    pontos_transformados = aplicar_transformacao(pontos_originais, shx, shy, modo)
    
    # 3. Obter a matriz de transformação
    matriz = obter_matriz_transformacao(shx, shy, modo)
    
    # 4. Formatar os dados para retorno JSON
    result = {
        "original": pontos_originais.tolist(),
        "transformado": pontos_transformados.tolist(),
        "matriz": matriz.tolist(),
        "coords": [
            {
                "label": f"P{i+1}",
                "orig": [float(orig[0]), float(orig[1])],
                "trans": [float(trans[0]), float(trans[1])]
            }
            for i, (orig, trans) in enumerate(zip(pontos_originais, pontos_transformados))
        ]
    }
    
    return result


def main():
    """
    Inicia o servidor Eel e abre a interface web.
    
    O servidor fica em execução esperando conexões. A janela da aplicação
    será aberta automaticamente com a interface web em http://localhost:8000
    
    Atalhos úteis durante execução:
        - Fechar a janela: Encerra o servidor Eel
        - Atualizar página (F5): Recarrega a interface web
        - Abrir DevTools (F12): Abre ferramentas de desenvolvedor
    
    Para interromper via terminal:
        - Ctrl+C para parar o servidor
    """
    eel.start('index.html', size=(1100, 700))


if __name__ == '__main__':
    main()
