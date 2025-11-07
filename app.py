from flask import Flask, request, jsonify, send_from_directory
import json, os
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

DATA_FILE = "roadmap_data.json"
SHEETS_ID = "1y2jRf9G6WzHWDCoER7gjrEKL4LoepRuHdk5fsctzgNo"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Cargar credenciales desde variable de entorno (Render)
SERVICE_ACCOUNT_INFO = json.loads(os.environ["GOOGLE_CREDENTIALS"])
CREDS = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)

client = gspread.authorize(CREDS)
sheet = client.open_by_key(SHEETS_ID).sheet1



# ------------------------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"data": [], "estados": [], "meses": [], "cantidadSprints": 16}

def save_data(content):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    # Guardar también en Google Sheets
    sheet.clear()
    rows = [["Módulo", "Sprint", "Duración"]]
    for item in content["data"]:
        rows.append([item.get("modulo",""), item.get("sprint",""), item.get("duracion","")])
    sheet.update(rows)

# ------------------------------------

@app.route("/")
def index():
    return send_from_directory(".", "masvida_roadmap.html")

@app.route("/load")
def load():
    return jsonify(load_data())

@app.route("/save", methods=["POST"])
def save():
    content = request.get_json()
    save_data(content)
    return jsonify({"status": "ok"})

# ------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
