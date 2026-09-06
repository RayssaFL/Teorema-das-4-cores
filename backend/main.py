from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder="../frontend", static_url_path="")

labels = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
borders = {
    'AC': ['AM', 'RO'],
    'AL': ['BA', 'PE', 'SE'],
    'AP': ['PA'],
    'AM': ['AC', 'MT', 'PA', 'RO', 'RR'],
    'BA': ['AL', 'ES', 'GO', 'MG', 'PE', 'PI', 'SE', 'TO'],
    'CE': ['PB', 'PE', 'PI', 'RN'],
    'DF': ['GO', 'MG'],
    'ES': ['BA', 'MG', 'RJ'],
    'GO': ['BA', 'DF', 'MG', 'MS', 'MT', 'TO'],
    'MA': ['PA', 'PI', 'TO'],
    'MT': ['AM', 'GO', 'MS', 'PA', 'RO', 'TO'],
    'MS': ['GO', 'MG', 'MT', 'PR', 'SP'],
    'MG': ['BA', 'DF', 'ES', 'GO', 'MS', 'RJ', 'SP'],
    'PA': ['AP', 'AM', 'MA', 'MT', 'RR', 'TO'],
    'PB': ['CE', 'PE', 'RN'],
    'PR': ['MS', 'SC', 'SP'],
    'PE': ['AL', 'BA', 'CE', 'PB', 'PI'],
    'PI': ['BA', 'CE', 'MA', 'PE', 'TO'],
    'RJ': ['ES', 'MG', 'SP'],
    'RN': ['CE', 'PB'],
    'RS': ['SC'],
    'RO': ['AC', 'AM', 'MT'],
    'RR': ['AM', 'PA'],
    'SC': ['PR', 'RS'],
    'SP': ['MG', 'MS', 'PR', 'RJ'],
    'SE': ['AL', 'BA'],
    'TO': ['BA', 'GO', 'MA', 'MT', 'PA', 'PI']
}

colors = [
    "#009c3b",
    "#ffdf00",
    "#00569c",  
    "#B70000"   
]

def greedy_alg():
    order = sorted(labels, key=lambda state: len(borders[state]), reverse=True)
    coloration = {}
    for state in order:
        colors_neighbours = []
        for neighbour in borders[state]:
            if neighbour in coloration:
                colors_neighbours.append(
                    coloration[neighbour]
                )

        for color in colors:
            if color not in colors_neighbours:
                coloration[state] = color
                break

    return coloration

result = greedy_alg()

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/api/coloration")
def coloration():
    return jsonify({
        "colors":result,
        "neighbours": borders
    })

@app.route("/br_states.json")
def geojson():
    return send_from_directory("../frontend", "br_states.json")

if __name__ == "__main__":
    for state, color in result.items():
        print(f"{state}:{color}")

    print()
    print("Servidor iniciado!")
    print("Acesse: http://127.0.0.1:5000")

    app.run(debug=True)