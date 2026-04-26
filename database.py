import json
import os
from datetime import datetime

LEADS_FILE = "data/leads.json"
PREGUNTAS_FILE = "data/preguntas_sin_respuesta.json"

# Asegurar que el directorio data existe
os.makedirs("data", exist_ok=True)

def guardar_lead(nombre, email, interes):
    lead = {
        "fecha": datetime.now().isoformat(),
        "nombre": nombre,
        "email": email,
        "interes": interes
    }
    try:
        leads = []
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        leads.append(lead)
        with open(LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=4, ensure_ascii=False)
        return "Datos guardados correctamente. Me pondré en contacto contigo pronto."
    except Exception as e:
        return f"Error al guardar datos: {e}"

def registrar_pregunta(pregunta):
    item = {
        "fecha": datetime.now().isoformat(),
        "pregunta": pregunta
    }
    try:
        items = []
        if os.path.exists(PREGUNTAS_FILE):
            with open(PREGUNTAS_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
        items.append(item)
        with open(PREGUNTAS_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=4, ensure_ascii=False)
        return "Pregunta registrada para revisión técnica."
    except Exception as e:
        return f"Error al registrar pregunta: {e}"
