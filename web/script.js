/**
 * Script principal - Cisalhamento Geométrico
 * 
 * Responsabilidades:
 * 1. Gerenciar controles de entrada (sliders, radio buttons)
 * 2. Chamar backend Python via Eel
 * 3. Renderizar gráficos no Canvas
 * 4. Atualizar exibição de matriz e coordenadas
 */

// Estado da aplicação
let appState = {
    shx: 1.0,
    shy: 0.0,
    figura: "Quadrado",
    modo: "Horizontal",
    dados: null
};

// Cores conforme tema dark
const CORES = {
    original: "#95a5a6",
    transformada: "#3498db",
    deslocamento: "#e74c3c",
    grid: "#444",
    eixo: "#666",
    fundo: "#0f0f0f"
};

// Canvas e contexto
let canvas;
let ctx;
const ESCALA = 60; // pixels por unidade

/**
 * Inicializa o canvas e configura event listeners
 */
function inicializar() {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");

    // Event listeners para controles
    document.querySelectorAll("input[name='modo']").forEach(radio => {
        radio.addEventListener("change", atualizarModo);
    });

    document.querySelectorAll("input[name='figura']").forEach(radio => {
        radio.addEventListener("change", atualizarFigura);
    });

    document.getElementById("shx-slider").addEventListener("input", atualizarShx);
    document.getElementById("shy-slider").addEventListener("input", atualizarShy);
    document.getElementById("reset-btn").addEventListener("click", resetar);

    // Atualizar interface inicialmente
    atualizarInterfaceSliders();
    calcularEAtualizar();
}

/**
 * Atualiza o valor de shx e habilita/desabilita controles conforme o modo
 */
function atualizarShx(event) {
    appState.shx = parseFloat(event.target.value);
    document.getElementById("shx-value").textContent = appState.shx.toFixed(1);
    calcularEAtualizar();
}

/**
 * Atualiza o valor de shy e habilita/desabilita controles conforme o modo
 */
function atualizarShy(event) {
    appState.shy = parseFloat(event.target.value);
    document.getElementById("shy-value").textContent = appState.shy.toFixed(1);
    calcularEAtualizar();
}

/**
 * Atualiza o modo de cisalhamento e habilita/desabilita sliders
 */
function atualizarModo(event) {
    appState.modo = event.target.value;
    atualizarInterfaceSliders();
    calcularEAtualizar();
}

/**
 * Habilita/desabilita sliders conforme o modo selecionado
 */
function atualizarInterfaceSliders() {
    const shxSlider = document.getElementById("shx-slider");
    const shySlider = document.getElementById("shy-slider");

    if (appState.modo === "Horizontal") {
        shxSlider.disabled = false;
        shySlider.disabled = true;
    } else if (appState.modo === "Vertical") {
        shxSlider.disabled = true;
        shySlider.disabled = false;
    } else if (appState.modo === "Ambos") {
        shxSlider.disabled = false;
        shySlider.disabled = false;
    }
}

/**
 * Atualiza a figura selecionada
 */
function atualizarFigura(event) {
    appState.figura = event.target.value;
    calcularEAtualizar();
}

/**
 * Reseta todos os controles para os valores iniciais
 */
function resetar() {
    appState.shx = 1.0;
    appState.shy = 0.0;
    appState.figura = "Quadrado";
    appState.modo = "Horizontal";

    document.getElementById("shx-slider").value = 1.0;
    document.getElementById("shy-slider").value = 0.0;
    document.querySelector("input[name='modo'][value='Horizontal']").checked = true;
    document.querySelector("input[name='figura'][value='Quadrado']").checked = true;

    atualizarInterfaceSliders();
    document.getElementById("shx-value").textContent = "1.0";
    document.getElementById("shy-value").textContent = "0.0";

    calcularEAtualizar();
}

/**
 * Chama o backend Python e atualiza a interface
 */
async function calcularEAtualizar() {
    try {
        // Chamar função exposta do backend Python
        const resultado = await eel.calcular(
            appState.shx,
            appState.shy,
            appState.figura,
            appState.modo
        )();

        appState.dados = resultado;

        // Atualizar exibições
        atualizarMatriz();
        atualizarCoordenadas();
        desenharCanvas();
    } catch (erro) {
        console.error("Erro ao calcular transformação:", erro);
    }
}

/**
 * Atualiza a exibição da matriz de transformação
 */
function atualizarMatriz() {
    if (!appState.dados || !appState.dados.matriz) return;

    const matriz = appState.dados.matriz;
    let texto = "⎡ ";
    
    // Primeira linha
    for (let j = 0; j < 3; j++) {
        texto += matriz[0][j].toFixed(2).padStart(6);
    }
    texto += " ⎤\n⎢ ";
    
    // Segunda linha
    for (let j = 0; j < 3; j++) {
        texto += matriz[1][j].toFixed(2).padStart(6);
    }
    texto += " ⎥\n⎣ ";
    
    // Terceira linha
    for (let j = 0; j < 3; j++) {
        texto += matriz[2][j].toFixed(2).padStart(6);
    }
    texto += " ⎦";

    document.getElementById("matriz").textContent = texto;
}

/**
 * Atualiza a exibição das coordenadas transformadas
 */
function atualizarCoordenadas() {
    if (!appState.dados || !appState.dados.coords) return;

    const coordsDiv = document.getElementById("coords");
    coordsDiv.innerHTML = "";

    appState.dados.coords.forEach(coord => {
        const item = document.createElement("div");
        item.className = "coord-item";

        const label = document.createElement("span");
        label.className = "coord-label";
        label.textContent = coord.label;

        const orig = document.createElement("span");
        orig.textContent = `[${coord.orig[0].toFixed(2)}, ${coord.orig[1].toFixed(2)}]`;

        const trans = document.createElement("span");
        trans.textContent = `[${coord.trans[0].toFixed(2)}, ${coord.trans[1].toFixed(2)}]`;

        item.appendChild(label);
        item.appendChild(orig);
        item.appendChild(trans);
        coordsDiv.appendChild(item);
    });
}

/**
 * Desenha o canvas com:
 * 1. Grid e eixos
 * 2. Figura original (cinza tracejado)
 * 3. Figura transformada (azul)
 * 4. Linhas de deslocamento (vermelho)
 */
function desenharCanvas() {
    if (!appState.dados) return;

    const w = canvas.width;
    const h = canvas.height;
    const cx = w / 2;
    const cy = h / 2;

    // Limpar canvas
    ctx.fillStyle = CORES.fundo;
    ctx.fillRect(0, 0, w, h);

    // Desenhar grid
    desenharGrid(cx, cy);

    // Desenhar eixos
    desenharEixos(cx, cy);

    // Desenhar figura original
    desenharFigura(
        appState.dados.original,
        CORES.original,
        true,  // tracejado
        cx,
        cy
    );

    // Desenhar linhas de deslocamento (antes da figura transformada)
    desenharDeslocamentos(
        appState.dados.original,
        appState.dados.transformado,
        cx,
        cy
    );

    // Desenhar figura transformada
    desenharFigura(
        appState.dados.transformado,
        CORES.transformada,
        false, // sólido
        cx,
        cy
    );
}

/**
 * Desenha o grid de fundo
 */
function desenharGrid(cx, cy) {
    ctx.strokeStyle = CORES.grid;
    ctx.lineWidth = 0.5;

    // Linhas verticais
    for (let i = -10; i <= 10; i++) {
        const x = cx + i * ESCALA;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }

    // Linhas horizontais
    for (let i = -10; i <= 10; i++) {
        const y = cy - i * ESCALA;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

/**
 * Desenha os eixos X e Y
 */
function desenharEixos(cx, cy) {
    ctx.strokeStyle = CORES.eixo;
    ctx.lineWidth = 2;

    // Eixo X
    ctx.beginPath();
    ctx.moveTo(0, cy);
    ctx.lineTo(canvas.width, cy);
    ctx.stroke();

    // Eixo Y
    ctx.beginPath();
    ctx.moveTo(cx, 0);
    ctx.lineTo(cx, canvas.height);
    ctx.stroke();

    // Origem
    ctx.fillStyle = CORES.eixo;
    ctx.fillRect(cx - 2, cy - 2, 4, 4);
}

/**
 * Desenha uma figura (polígono)
 */
function desenharFigura(pontos, cor, tracejado, cx, cy) {
    if (pontos.length === 0) return;

    ctx.strokeStyle = cor;
    ctx.fillStyle = cor;
    ctx.lineWidth = tracejado ? 2 : 3;

    if (tracejado) {
        ctx.setLineDash([5, 5]);
    } else {
        ctx.setLineDash([]);
    }

    // Desenhar polígono
    ctx.beginPath();
    const x0 = cx + pontos[0][0] * ESCALA;
    const y0 = cy - pontos[0][1] * ESCALA;
    ctx.moveTo(x0, y0);

    for (let i = 1; i < pontos.length; i++) {
        const x = cx + pontos[i][0] * ESCALA;
        const y = cy - pontos[i][1] * ESCALA;
        ctx.lineTo(x, y);
    }

    ctx.closePath();
    ctx.stroke();

    ctx.setLineDash([]);
}

/**
 * Desenha as linhas de deslocamento entre vértices originais e transformados
 */
function desenharDeslocamentos(original, transformado, cx, cy) {
    ctx.strokeStyle = CORES.deslocamento;
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);

    for (let i = 0; i < original.length; i++) {
        const x1 = cx + original[i][0] * ESCALA;
        const y1 = cy - original[i][1] * ESCALA;
        const x2 = cx + transformado[i][0] * ESCALA;
        const y2 = cy - transformado[i][1] * ESCALA;

        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();

        // Desenhar círculo pequeno em cada vértice original
        ctx.fillStyle = CORES.deslocamento;
        ctx.beginPath();
        ctx.arc(x1, y1, 4, 0, 2 * Math.PI);
        ctx.fill();
    }

    ctx.setLineDash([]);
}

// Inicializar quando o DOM estiver pronto
document.addEventListener("DOMContentLoaded", inicializar);
