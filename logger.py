import json
from datetime import datetime
import os

LOG_FILE = "logs_interacciones.jsonl"

def log_interaccion(pregunta, respuesta, evaluacion_final, intentos):
    # Asegurar compatibilidad con el nuevo formato de diccionario de evaluación
    calidad = evaluacion_final.get("calidad", 0)
    comentario = evaluacion_final.get("comentario", "Sin comentarios")
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "pregunta": pregunta,
        "respuesta": respuesta,
        "evaluacion_final": {
            "calidad": calidad,
            "comentario": comentario,
            "aceptada": calidad >= 7  # Consideramos aceptable si es 7 o más
        },
        "intentos": intentos
    }
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def obtener_estadisticas():
    if not os.path.exists(LOG_FILE):
        return "No hay logs disponibles."
    
    total = 0
    aceptadas = 0
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                total += 1
                data = json.loads(line)
                if data["evaluacion_final"].get("aceptada", False):
                    aceptadas += 1
            except:
                continue
    
    return f"Total: {total} | Aceptadas: {aceptadas} ({ (aceptadas/total)*100 if total > 0 else 0 }%)"
