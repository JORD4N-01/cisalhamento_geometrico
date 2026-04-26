#!/usr/bin/env python3
"""
Cisalhamento Geométrico - Transformações 2D
Projeto acadêmico para demonstrar cisalhamento horizontal e vertical
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Figuras disponíveis
FIGURAS = {
    "Quadrado": [(-2, -2), (2, -2), (2, 2), (-2, 2)],
    "Triângulo": [(0, 3), (-3, -2), (3, -2)],
    "Casa": [(-2, -2), (2, -2), (2, 1), (0, 3), (-2, 1)]
}

def cisalhamento_horizontal(pontos: np.ndarray, shx: float) -> np.ndarray:
    """Aplica x' = x + shx·y para cada vértice."""
    matriz = np.array([
        [1, shx, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    
    # Converter para coordenadas homogêneas
    pontos_homogeneos = np.column_stack([pontos, np.ones(len(pontos))])
    
    # Aplicar transformação
    transformados = pontos_homogeneos @ matriz.T
    
    # Retornar apenas coordenadas x, y
    return transformados[:, :2]

def cisalhamento_vertical(pontos: np.ndarray, shy: float) -> np.ndarray:
    """Aplica y' = y + shy·x para cada vértice."""
    matriz = np.array([
        [1, 0, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ])
    
    # Converter para coordenadas homogêneas
    pontos_homogeneos = np.column_stack([pontos, np.ones(len(pontos))])
    
    # Aplicar transformação
    transformados = pontos_homogeneos @ matriz.T
    
    # Retornar apenas coordenadas x, y
    return transformados[:, :2]

def aplicar_transformacao(pontos: np.ndarray, shx: float, shy: float, modo: str) -> np.ndarray:
    """Combina horizontal e vertical (modo Ambos)."""
    if modo == "Horizontal":
        return cisalhamento_horizontal(pontos, shx)
    elif modo == "Vertical":
        return cisalhamento_vertical(pontos, shy)
    elif modo == "Ambos":
        # Aplicar ambas as transformações sequencialmente
        horizontal = cisalhamento_horizontal(pontos, shx)
        return cisalhamento_vertical(horizontal, shy)
    else:
        return pontos.copy()

def obter_matriz_transformacao(shx: float, shy: float, modo: str) -> np.ndarray:
    """Retorna a matriz de transformação atual."""
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
        # Matriz combinada
        return np.array([
            [1, shx, 0],
            [shy, 1 + shx * shy, 0],
            [0, 0, 1]
        ])
    else:
        return np.eye(3)

class CisalhamentoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cisalhamento Geométrico")
        self.root.geometry("1000x600")
        
        # Variáveis de controle
        self.modo_var = tk.StringVar(value="Horizontal")
        self.figura_var = tk.StringVar(value="Quadrado")
        self.shx_var = tk.DoubleVar(value=1.0)
        self.shy_var = tk.DoubleVar(value=0.0)
        
        # Criar interface
        self.criar_interface()
        
        # Desenhar inicial
        self.atualizar_visualizacao()
    
    def criar_interface(self):
        """Cria a interface gráfica Tkinter."""
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(0, weight=1)
        
        # Frame esquerdo - controles
        frame_controles = ttk.Frame(frame_principal, padding="10")
        frame_controles.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tipo de cisalhamento
        frame_tipo = ttk.LabelFrame(frame_controles, text="Tipo de cisalhamento", padding="10")
        frame_tipo.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(frame_tipo, text="Horizontal", variable=self.modo_var, 
                       value="Horizontal", command=self.atualizar_visualizacao).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(frame_tipo, text="Vertical", variable=self.modo_var, 
                       value="Vertical", command=self.atualizar_visualizacao).grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(frame_tipo, text="Ambos", variable=self.modo_var, 
                       value="Ambos", command=self.atualizar_visualizacao).grid(row=2, column=0, sticky=tk.W)
        
        # Fatores
        frame_fatores = ttk.LabelFrame(frame_controles, text="Fatores", padding="10")
        frame_fatores.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame_fatores, text="shx:").grid(row=0, column=0, sticky=tk.W)
        self.slider_shx = ttk.Scale(frame_fatores, from_=-3.0, to=3.0, variable=self.shx_var,
                                   orient=tk.HORIZONTAL, length=200, command=self.atualizar_visualizacao)
        self.slider_shx.grid(row=0, column=1, padx=(5, 0))
        self.label_shx = ttk.Label(frame_fatores, text="1.00")
        self.label_shx.grid(row=0, column=2, padx=(5, 0))
        
        ttk.Label(frame_fatores, text="shy:").grid(row=1, column=0, sticky=tk.W)
        self.slider_shy = ttk.Scale(frame_fatores, from_=-3.0, to=3.0, variable=self.shy_var,
                                   orient=tk.HORIZONTAL, length=200, command=self.atualizar_visualizacao)
        self.slider_shy.grid(row=1, column=1, padx=(5, 0))
        self.label_shy = ttk.Label(frame_fatores, text="0.00")
        self.label_shy.grid(row=1, column=2, padx=(5, 0))
        
        # Figura
        frame_figura = ttk.LabelFrame(frame_controles, text="Figura", padding="10")
        frame_figura.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(frame_figura, text="Quadrado", variable=self.figura_var, 
                       value="Quadrado", command=self.atualizar_visualizacao).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(frame_figura, text="Triângulo", variable=self.figura_var, 
                       value="Triângulo", command=self.atualizar_visualizacao).grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(frame_figura, text="Casa", variable=self.figura_var, 
                       value="Casa", command=self.atualizar_visualizacao).grid(row=2, column=0, sticky=tk.W)
        
        # Matriz de transformação
        frame_matriz = ttk.LabelFrame(frame_controles, text="Matriz de Transformação", padding="10")
        frame_matriz.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.label_matriz = ttk.Label(frame_matriz, text="", font=("Courier", 10))
        self.label_matriz.grid(row=0, column=0, sticky=tk.W)
        
        # Coordenadas transformadas
        frame_coords = ttk.LabelFrame(frame_controles, text="Coordenadas Transformadas", padding="10")
        frame_coords.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.label_coords = ttk.Label(frame_coords, text="", font=("Courier", 9))
        self.label_coords.grid(row=0, column=0, sticky=tk.W)
        
        # Frame direito - canvas
        frame_canvas = ttk.Frame(frame_principal, padding="10")
        frame_canvas.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Criar figura matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_canvas)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        frame_canvas.columnconfigure(0, weight=1)
        frame_canvas.rowconfigure(0, weight=1)
    
    def atualizar_visualizacao(self, *args):
        """Atualiza o gráfico e labels quando os controles mudam."""
        modo = self.modo_var.get()
        shx = self.shx_var.get()
        shy = self.shy_var.get()
        
        # Atualizar labels dos sliders
        self.label_shx.config(text=f"{shx:.2f}")
        self.label_shy.config(text=f"{shy:.2f}")
        
        # Habilitar/desabilitar sliders conforme o modo
        if modo == "Horizontal":
            self.slider_shx.config(state="normal")
            self.slider_shy.config(state="disabled")
        elif modo == "Vertical":
            self.slider_shx.config(state="disabled")
            self.slider_shy.config(state="normal")
        else:  # Ambos
            self.slider_shx.config(state="normal")
            self.slider_shy.config(state="normal")
        
        # Obter figura atual
        nome_figura = self.figura_var.get()
        pontos_originais = np.array(FIGURAS[nome_figura])
        
        # Aplicar transformação
        pontos_transformados = aplicar_transformacao(pontos_originais, shx, shy, modo)
        
        # Limpar e redesenhar
        self.ax.clear()
        
        # Configurar plano cartesiano
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title(f'Cisalhamento {modo} - {nome_figura}')
        
        # Desenhar figura original (cinza tracejado)
        orig_closed = np.vstack([pontos_originais, pontos_originais[0]])
        self.ax.plot(orig_closed[:, 0], orig_closed[:, 1], 'gray', linestyle='--', 
                    alpha=0.6, linewidth=1, label='Original')
        
        # Desenhar figura transformada (azul sólido)
        trans_closed = np.vstack([pontos_transformados, pontos_transformados[0]])
        self.ax.plot(trans_closed[:, 0], trans_closed[:, 1], 'blue', 
                    linewidth=2, label='Transformada')
        
        # Desenhar linhas de deslocamento
        for i in range(len(pontos_originais)):
            self.ax.plot([pontos_originais[i, 0], pontos_transformados[i, 0]], 
                        [pontos_originais[i, 1], pontos_transformados[i, 1]], 
                        'red', alpha=0.3, linestyle=':', linewidth=1)
        
        # Marcar vértices
        self.ax.scatter(pontos_originais[:, 0], pontos_originais[:, 1], 
                       c='gray', s=30, alpha=0.6, zorder=5)
        self.ax.scatter(pontos_transformados[:, 0], pontos_transformados[:, 1], 
                       c='blue', s=40, zorder=5)
        
        self.ax.legend()
        
        # Atualizar canvas
        self.canvas.draw()
        
        # Atualizar matriz de transformação
        matriz = obter_matriz_transformacao(shx, shy, modo)
        matriz_str = "┌                 ┐\n"
        matriz_str += f"│ {matriz[0,0]:6.2f} {matriz[0,1]:6.2f} {matriz[0,2]:6.2f} │\n"
        matriz_str += f"│ {matriz[1,0]:6.2f} {matriz[1,1]:6.2f} {matriz[1,2]:6.2f} │\n"
        matriz_str += f"│ {matriz[2,0]:6.2f} {matriz[2,1]:6.2f} {matriz[2,2]:6.2f} │\n"
        matriz_str += "└                 ┘"
        self.label_matriz.config(text=matriz_str)
        
        # Atualizar coordenadas
        coords_str = ""
        for i, (orig, trans) in enumerate(zip(pontos_originais, pontos_transformados)):
            coords_str += f"P{i+1}: ({orig[0]:5.2f}, {orig[1]:5.2f}) → ({trans[0]:5.2f}, {trans[1]:5.2f})\n"
        self.label_coords.config(text=coords_str.strip())

def main():
    """Função principal para executar a aplicação."""
    root = tk.Tk()
    app = CisalhamentoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
