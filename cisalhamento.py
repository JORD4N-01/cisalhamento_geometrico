#!/usr/bin/env python3
"""
Cisalhamento Geométrico - Transformações 2D
Projeto acadêmico para demonstrar cisalhamento horizontal e vertical
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

# Configurar tema dark do matplotlib
plt.style.use('dark_background')

# Cores do tema
CORES = {
    'fundo': '#1e1e2e',
    'painel': '#2a2a3e',
    'header': '#181825',
    'grid': '#313244',
    'original': '#6c7086',
    'transformado': '#89b4fa',
    'deslocamento': '#f38ba8',
    'texto': '#cdd6f4',
    'texto_secundario': '#a6adc8'
}

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
        self.root.title("Cisalhamento Geométrico — CIESA")
        self.root.geometry("1000x650")
        self.root.minsize(1000, 650)
        
        # Configurar fontes
        self.fonte_padrao = ('Segoe UI', 10)
        self.fonte_titulo = ('Segoe UI', 12, 'bold')
        self.fonte_mono = ('Courier New', 10)
        self.fonte_mono_pequena = ('Courier New', 9)
        
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
        """Cria a interface gráfica com ttkbootstrap."""
        # Frame principal
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Criar header
        self.criar_header()
        
        # Frame esquerdo - controles
        frame_controles = ttk.LabelFrame(frame_principal, text="Controles")
        frame_controles.pack(side=LEFT, fill=BOTH, padx=(0, 10))
        
        # Tipo de cisalhamento
        frame_tipo = ttk.LabelFrame(frame_controles, text="Tipo de cisalhamento")
        frame_tipo.pack(fill=X, padx=10, pady=(10, 5))
        
        self.criar_radiobutton_estilizado(frame_tipo, "Horizontal", 0, 0, self.modo_var, "Horizontal")
        self.criar_radiobutton_estilizado(frame_tipo, "Vertical", 1, 0, self.modo_var, "Vertical")
        self.criar_radiobutton_estilizado(frame_tipo, "Ambos", 2, 0, self.modo_var, "Ambos")
        
        # Fatores
        frame_fatores = ttk.LabelFrame(frame_controles, text="Fatores")
        frame_fatores.pack(fill=X, padx=10, pady=5)
        
        # Slider shx
        ttk.Label(frame_fatores, text="shx:").grid(row=0, column=0, sticky=W, padx=5, pady=2)
        self.slider_shx = ttk.Scale(frame_fatores, from_=-3.0, to=3.0, variable=self.shx_var,
                                   orient=HORIZONTAL, length=200,
                                   command=self.atualizar_visualizacao)
        self.slider_shx.grid(row=0, column=1, padx=(5, 10), pady=2)
        self.label_shx = ttk.Label(frame_fatores, text="1.00", width=6)
        self.label_shx.grid(row=0, column=2, padx=(0, 5), pady=2)
        
        # Slider shy
        ttk.Label(frame_fatores, text="shy:").grid(row=1, column=0, sticky=W, padx=5, pady=2)
        self.slider_shy = ttk.Scale(frame_fatores, from_=-3.0, to=3.0, variable=self.shy_var,
                                   orient=HORIZONTAL, length=200,
                                   command=self.atualizar_visualizacao)
        self.slider_shy.grid(row=1, column=1, padx=(5, 10), pady=2)
        self.label_shy = ttk.Label(frame_fatores, text="0.00", width=6)
        self.label_shy.grid(row=1, column=2, padx=(0, 5), pady=2)
        
        # Figura
        frame_figura = ttk.LabelFrame(frame_controles, text="Figura")
        frame_figura.pack(fill=X, padx=10, pady=5)
        
        self.criar_radiobutton_estilizado(frame_figura, "Quadrado", 0, 0, self.figura_var, "Quadrado")
        self.criar_radiobutton_estilizado(frame_figura, "Triângulo", 1, 0, self.figura_var, "Triângulo")
        self.criar_radiobutton_estilizado(frame_figura, "Casa", 2, 0, self.figura_var, "Casa")
        
        # Botão Resetar
        self.botao_resetar = ttk.Button(frame_controles, text="Resetar",
                                       command=self.resetar_valores)
        self.botao_resetar.pack(pady=10, padx=10)
        
        # Matriz de transformação
        frame_matriz = ttk.LabelFrame(frame_controles, text="Matriz de Transformação")
        frame_matriz.pack(fill=X, padx=10, pady=5)
        
        self.label_matriz = tk.Label(frame_matriz, text="", font=self.fonte_mono, 
                                    bg=CORES['painel'], fg=CORES['texto'], justify=LEFT)
        self.label_matriz.pack(padx=5, pady=5)
        
        # Coordenadas transformadas
        frame_coords = ttk.LabelFrame(frame_controles, text="Coordenadas Transformadas")
        frame_coords.pack(fill=X, padx=10, pady=(5, 10))
        
        self.label_coords = tk.Label(frame_coords, text="", font=self.fonte_mono_pequena, 
                                     bg=CORES['painel'], fg=CORES['texto'], justify=LEFT)
        self.label_coords.pack(padx=5, pady=5)
        
        # Frame direito - canvas
        frame_canvas = ttk.Frame(frame_principal)
        frame_canvas.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Criar figura matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7), facecolor=CORES['fundo'])
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_canvas)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Criar footer
        self.criar_footer()
    
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
        
        # Configurar plano cartesiano com tema dark
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor(CORES['fundo'])
        
        # Grid sutil com linhas tracejadas
        self.ax.grid(True, alpha=0.3, linestyle='--', color=CORES['grid'], linewidth=0.5)
        
        # Eixos principais
        self.ax.axhline(y=0, color=CORES['texto_secundario'], linewidth=1, alpha=0.8)
        self.ax.axvline(x=0, color=CORES['texto_secundario'], linewidth=1, alpha=0.8)
        
        # Configurar eixos com setas
        self.ax.set_xlabel('X', color=CORES['texto'], fontsize=12)
        self.ax.set_ylabel('Y', color=CORES['texto'], fontsize=12)
        self.ax.set_title(f'Cisalhamento {modo} - {nome_figura}', 
                         color=CORES['texto'], fontsize=14, pad=20)
        
        # Configurar ticks
        self.ax.tick_params(colors=CORES['texto_secundario'])
        
        # Desenhar figura original (cinza tracejado com preenchimento transparente)
        orig_closed = np.vstack([pontos_originais, pontos_originais[0]])
        self.ax.fill(orig_closed[:, 0], orig_closed[:, 1], color=CORES['original'], 
                     alpha=0.2, edgecolor=CORES['original'], linestyle='--', linewidth=1.5)
        
        # Desenhar figura transformada (azul sólido com preenchimento semitransparente)
        trans_closed = np.vstack([pontos_transformados, pontos_transformados[0]])
        self.ax.fill(trans_closed[:, 0], trans_closed[:, 1], color=CORES['transformado'], 
                     alpha=0.4, edgecolor=CORES['transformado'], linewidth=2.5)
        
        # Desenhar linhas de deslocamento
        for i in range(len(pontos_originais)):
            self.ax.plot([pontos_originais[i, 0], pontos_transformados[i, 0]], 
                        [pontos_originais[i, 1], pontos_transformados[i, 1]], 
                        color=CORES['deslocamento'], alpha=0.5, linestyle=':', linewidth=1.5)
        
        # Marcar vértices com círculos preenchidos
        self.ax.scatter(pontos_originais[:, 0], pontos_originais[:, 1], 
                       c=CORES['original'], s=60, alpha=0.8, zorder=5, 
                       edgecolors='white', linewidth=1)
        self.ax.scatter(pontos_transformados[:, 0], pontos_transformados[:, 1], 
                       c=CORES['transformado'], s=80, zorder=5, 
                       edgecolors='white', linewidth=1.5)
        
        # Legenda no canto superior direito
        self.ax.legend(['Original', 'Transformada'], loc='upper right', 
                      facecolor=CORES['painel'], edgecolor=CORES['texto'],
                      labelcolor=CORES['texto'], framealpha=0.9)
        
        # Adicionar setas nos eixos
        self.ax.annotate('', xy=(7, 0), xytext=(6.5, 0),
                        arrowprops=dict(arrowstyle='->', color=CORES['texto'], lw=2))
        self.ax.annotate('', xy=(0, 7), xytext=(0, 6.5),
                        arrowprops=dict(arrowstyle='->', color=CORES['texto'], lw=2))
        
        # Atualizar canvas
        self.canvas.draw()
        
        # Atualizar matriz de transformação
        matriz = obter_matriz_transformacao(shx, shy, modo)
        matriz_str = "┌                     ┐\n"
        matriz_str += f"│ {matriz[0,0]:7.2f} {matriz[0,1]:7.2f} {matriz[0,2]:7.2f} │\n"
        matriz_str += f"│ {matriz[1,0]:7.2f} {matriz[1,1]:7.2f} {matriz[1,2]:7.2f} │\n"
        matriz_str += f"│ {matriz[2,0]:7.2f} {matriz[2,1]:7.2f} {matriz[2,2]:7.2f} │\n"
        matriz_str += "└                     ┘"
        self.label_matriz.config(text=matriz_str)
        
        # Atualizar coordenadas
        coords_str = ""
        for i, (orig, trans) in enumerate(zip(pontos_originais, pontos_transformados)):
            coords_str += f"P{i+1}: ({orig[0]:5.2f}, {orig[1]:5.2f}) → ({trans[0]:5.2f}, {trans[1]:5.2f})\n"
        self.label_coords.config(text=coords_str.strip())
    
    def criar_header(self):
        """Cria o header fixo com título e instituição."""
        header = ttk.Frame(self.root)
        header.pack(fill=X)
        
        # Título à esquerda
        titulo = ttk.Label(header, text="Cisalhamento Geométrico", 
                          font=('Segoe UI', 16, 'bold'))
        titulo.pack(side=LEFT, padx=20, pady=10)
        
        # Instituição à direita
        instituicao = ttk.Label(header, text="CIESA · Computação Gráfica", 
                              font=('Segoe UI', 12))
        instituicao.pack(side=RIGHT, padx=20, pady=10)
    
    def criar_footer(self):
        """Cria o footer com legenda de cores."""
        footer = ttk.Frame(self.root)
        footer.pack(fill=X, side=BOTTOM)
        
        # Legenda de cores
        legenda_frame = ttk.Frame(footer)
        legenda_frame.pack(expand=True)
        
        # Quadrado original
        quad_original = tk.Canvas(legenda_frame, width=15, height=15, 
                                  bg=CORES['header'], highlightthickness=0)
        quad_original.create_rectangle(2, 2, 13, 13, fill=CORES['original'], 
                                      outline=CORES['original'])
        quad_original.grid(row=0, column=0, padx=5)
        ttk.Label(legenda_frame, text="Original", 
                 font=self.fonte_padrao).grid(row=0, column=1, padx=(0, 20))
        
        # Quadrado transformado
        quad_transformado = tk.Canvas(legenda_frame, width=15, height=15, 
                                     bg=CORES['header'], highlightthickness=0)
        quad_transformado.create_rectangle(2, 2, 13, 13, fill=CORES['transformado'], 
                                          outline=CORES['transformado'])
        quad_transformado.grid(row=0, column=2, padx=5)
        ttk.Label(legenda_frame, text="Transformado", 
                 font=self.fonte_padrao).grid(row=0, column=3, padx=(0, 20))
        
        # Linha de deslocamento
        linha_desloc = tk.Canvas(legenda_frame, width=15, height=15, 
                                bg=CORES['header'], highlightthickness=0)
        linha_desloc.create_line(2, 7, 13, 7, fill=CORES['deslocamento'], 
                                width=2, dash=(2, 2))
        linha_desloc.grid(row=0, column=4, padx=5)
        ttk.Label(legenda_frame, text="Deslocamento", 
                 font=self.fonte_padrao).grid(row=0, column=5)
    
    def criar_radiobutton_estilizado(self, parent, texto, linha, coluna, variavel, valor):
        """Cria um radiobutton estilizado com ttkbootstrap."""
        rb = ttk.Radiobutton(parent, text=texto, variable=variavel, value=valor,
                           command=self.atualizar_visualizacao)
        rb.grid(row=linha, column=coluna, sticky=W, pady=2, padx=5)
        
        return rb
    
    def resetar_valores(self):
        """Reseta todos os valores para o estado inicial."""
        self.modo_var.set("Horizontal")
        self.figura_var.set("Quadrado")
        self.shx_var.set(1.0)
        self.shy_var.set(0.0)
        self.atualizar_visualizacao()

def main():
    """Função principal para executar a aplicação."""
    root = ttk.Window(themename="darkly")
    app = CisalhamentoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
