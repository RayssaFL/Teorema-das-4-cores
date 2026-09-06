let coresPorEstado = {};
let vizinhosPorEstado = {};
let camadaEstados = null;   

const mapa = L.map("map").setView([-14.5, -51.9], 4);


function estiloEstado(feature) {
    const sigla = feature.properties.SIGLA;
    const color = coresPorEstado[sigla] || "#cccccc";
    return {
        fillColor: color,
        weight: 1.5,
        color: "#333",
        fillOpacity: 0.85
    };
}


function destacar(e) {
    const camada = e.target;
    camada.setStyle({
        weight: 3,
        color: "#000",
        fillOpacity: 1
    });
    camada.bringToFront();
}


function removerDestaque(e) {
    camadaEstados.resetStyle(e.target);
}

function aoClicar(e) {
    const feature = e.target.feature;
    const sigla = feature.properties.SIGLA;
    const nome = feature.properties.Estado;
    const vizinhos = vizinhosPorEstado[sigla] || [];
    const color = coresPorEstado[sigla] || "#cccccc";
    const painel = document.getElementById("state-info");
    painel.innerHTML = `
        <h3>${nome} (${sigla})</h3>
        <p>
            <span style="display:inline-block; width:14px; height:14px;
                        border-radius:50%; background:${color};
                        margin-right:6px; vertical-align:middle;"></span>
            Cor atribuída: ${color}
        </p>
        <p style="margin-top:10px;">
            <strong>Vizinhos (${vizinhos.length}):</strong>
            ${vizinhos.length ? vizinhos.join(", ") : "nenhum"}
        </p>
    `;
}

function aoAdicionarFeature(feature, camada) {
    camada.on({
        mouseover: destacar,
        mouseout: removerDestaque,
        click: aoClicar
    });
}

async function carregarDados() {
    try {
        const resposta = await fetch("/api/coloration");
        const dados = await resposta.json();
        console.log("Cores:", dados.colors);
        console.log("Vizinhos:", dados.neighbours);
        coresPorEstado = dados.colors;
        vizinhosPorEstado = dados.neighbours;
        const respostaGeo = await fetch("/br_states.json");
        const geojson = await respostaGeo.json();
        camadaEstados = L.geoJSON(geojson, {
            style: estiloEstado,
            onEachFeature: aoAdicionarFeature
        }).addTo(mapa);
        mapa.fitBounds(camadaEstados.getBounds());

    }
    catch (erro) {
        console.error(
            "Erro ao carregar dados:",
            erro
        );
        document.getElementById("map").innerHTML = "<p style='padding:20px;'>Erro ao carregar o mapa. Veja o console (F12).</p>";
    }

}


carregarDados();
