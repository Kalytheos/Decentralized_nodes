import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

NODE_NAME = os.environ.get("NODE_NAME", "N5")
NODE_PORT = int(os.environ.get("NODE_PORT", 5005))
FRASE = "Ebrios de entusiasmo entramos,"
ID = 3
PEERS = ["N2"]
PORTS = {"N2": 5002}

@app.route("/frase", methods=["GET"])
def get_frase():
    return jsonify({"nodo": NODE_NAME, "frase": FRASE, "id": ID, "peers": PEERS})

@app.route("/frases", methods=["GET"])
def get_all_frases():
    from_node = request.args.get("from")
    frases = [{"nodo": NODE_NAME, "frase": FRASE, "id": ID}]
    for peer in PEERS:
        if peer == from_node:
            continue
        try:
            url = f"http://{peer}:{PORTS[peer]}/frases?from={NODE_NAME}"
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                frases += r.json()
        except Exception:
            pass
    if not from_node:
        frases_ordenadas = [f["frase"] for f in sorted(frases, key=lambda x: x["id"])]
        frases_texto = " / ".join(frases_ordenadas)
        return jsonify([frases_texto])
    return jsonify(frases)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=NODE_PORT)
