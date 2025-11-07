from flask import Flask, request, jsonify, send_from_directory
import json, os
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

DATA_FILE = "roadmap_data.json"
SHEETS_ID = "1y2jRf9G6WzHWDCoER7gjrEKL4LoepRuHdk5fsctzgNo"
ROADMAP_SHEET_NAME = "Roadmap"  # Nombre de la hoja principal
ESTADOS_SHEET_NAME = "Estados"  # Nombre de la hoja de estados

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Cargar credenciales desde variable de entorno (Render)
SERVICE_ACCOUNT_INFO = json.loads(os.environ["GOOGLE_CREDENTIALS"])
CREDS = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)

client = gspread.authorize(CREDS)
spreadsheet = client.open_by_key(SHEETS_ID)
sheet = spreadsheet.worksheet(ROADMAP_SHEET_NAME)
estados_sheet = spreadsheet.worksheet(ESTADOS_SHEET_NAME)



# ------------------------------------

def load_states_from_sheets():
    try:
        estados_data = estados_sheet.get_all_records()
        estados = []
        for estado in estados_data:
            estados.append({
                'id': estado['id'],
                'nombre': estado['nombre'],
                'color': estado['color']
            })
        return estados
    except Exception as e:
        print(f"Error loading states: {e}")
        return []

def save_states_to_sheets(estados):
    try:
        # Limpiar hoja actual
        estados_sheet.clear()
        # Establecer encabezados
        estados_sheet.append_row(['id', 'nombre', 'color'])
        # Agregar estados
        for estado in estados:
            estados_sheet.append_row([
                estado['id'],
                estado['nombre'],
                estado['color']
            ])
        return True
    except Exception as e:
        print(f"Error saving states: {e}")
        return False

def load_data():
    try:
        # Cargar datos del roadmap
        records = sheet.get_all_records()
        # Cargar estados
        estados = load_states_from_sheets()
        
        data = {
            "data": records,
            "estados": estados,
            "meses": [],
            "cantidadSprints": 16
        }
        
        # Actualizar archivo local
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return data
    except Exception as e:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"data": [], "estados": [], "meses": [], "cantidadSprints": 16}

def save_data(content):
    # Guardar en archivo local
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    # Guardar roadmap en Google Sheets
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

@app.route("/vistas", methods=["GET"])
def get_views():
    data = load_data()
    return jsonify(data.get("vistas", []))


@app.route("/vistas", methods=["POST"])
def save_views():
    data = load_data()
    new_views = request.get_json()
    data["vistas"] = new_views
    save_data(data)
    return jsonify({"status": "ok"})

@app.route("/save_states", methods=["POST"])
def save_states():
    estados = request.get_json()
    
    # Guardar en archivo local
    data = load_data()
    data["estados"] = estados
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    # Guardar en Google Sheets
    save_states_to_sheets(estados)
    
    return jsonify({"status": "ok"})

# ------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

