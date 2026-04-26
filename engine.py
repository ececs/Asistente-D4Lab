from model_factory import llamar_ia
from database import guardar_lead, registrar_pregunta
import requests
import json
import os

# --- HERRAMIENTAS ---

def guardar_datos_cliente(nombre: str, email: str, interes: str):
    """Guarda los datos de un cliente potencial interesado en servicios."""
    return guardar_lead(nombre, email, interes)

def registrar_pregunta_sin_respuesta(pregunta: str):
    """Registra una pregunta que el asistente no pudo responder."""
    return registrar_pregunta(pregunta)

def obtener_resumen_leads():
    """Obtiene un resumen de los últimos leads captados."""
    return "Resumen: 5 nuevos interesados en TesIA esta semana."

def obtener_flujos_n8n():
    """Obtiene el resumen de los flujos activos en el servidor n8n local."""
    N8N_URL = os.getenv("N8N_URL", "http://192.168.31.199:5678/api/v1")
    N8N_API_KEY = os.getenv("N8N_API_KEY")
    
    if not N8N_API_KEY:
        return "Error: N8N_API_KEY no configurada."
    
    try:
        response = requests.get(
            f"{N8N_URL}/workflows",
            headers={"X-N8N-API-KEY": N8N_API_KEY},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json().get("data", [])
            resumen = [f"- {w['name']} (ID: {w['id']})" for w in data[:10]]
            return "Flujos en n8n:\n" + "\n".join(resumen) if resumen else "No hay flujos activos."
        return f"Error al acceder a n8n: {response.status_code}"
    except Exception as e:
        return f"Excepción al conectar con n8n: {e}"

def leer_codigo_proyecto(nombre_archivo: str):
    """Lee el contenido de un archivo del proyecto para su revisión."""
    # Seguridad: Solo permitimos leer archivos en el directorio actual
    base_name = os.path.basename(nombre_archivo)
    if not base_name.endswith(('.py', '.html', '.txt', '.env')):
        return "Error: Solo se permite leer archivos de código (.py, .html, .txt, .env)."
    
    try:
        with open(base_name, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error al leer archivo: {e}"

def listar_archivos_proyecto():
    """Lista todos los archivos de código en el directorio del proyecto."""
    archivos = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(('.py', '.html', '.txt', '.env'))]
    return "Archivos en el proyecto:\n" + "\n".join(archivos)

def crear_documento_wiki(titulo: str, contenido: str):
    """Guarda un documento de documentación en la carpeta wiki."""
    os.makedirs("wiki", exist_ok=True)
    # Limpiar título para nombre de archivo
    safe_title = "".join([c for c in titulo if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
    file_path = f"wiki/{safe_title}.md"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {titulo}\n\n{contenido}")
        return f"Documento '{titulo}' guardado correctamente en {file_path}."
    except Exception as e:
        return f"Error al guardar documento wiki: {e}"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "guardar_datos_cliente",
            "description": "Guarda los datos de un cliente interesado",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string"},
                    "email": {"type": "string"},
                    "interes": {"type": "string"}
                },
                "required": ["nombre", "email", "interes"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "registrar_pregunta_sin_respuesta",
            "description": "Registra dudas que el asistente no sabe responder",
            "parameters": {
                "type": "object",
                "properties": {
                    "pregunta": {"type": "string"}
                },
                "required": ["pregunta"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "obtener_resumen_leads",
            "description": "Muestra resumen de marketing"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "obtener_flujos_n8n",
            "description": "Consulta flujos activos en n8n"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "leer_codigo_proyecto",
            "description": "Lee el código de un archivo para revisarlo",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_archivo": {"type": "string", "description": "Nombre del archivo a leer (ej. server.py)"}
                },
                "required": ["nombre_archivo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_archivos_proyecto",
            "description": "Lista los archivos disponibles en el proyecto"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crear_documento_wiki",
            "description": "Guarda documentación técnica en un archivo .md",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "Título del documento"},
                    "contenido": {"type": "string", "description": "Contenido en formato Markdown"}
                },
                "required": ["titulo", "contenido"]
            }
        }
    }
]

def evaluar_respuesta(respuesta, pregunta, contexto, prompt_evaluador):
    """
    Evalúa la calidad de la respuesta usando un modelo supervisor.
    """
    prompt = f"""
{prompt_evaluador}

Pregunta: {pregunta}
Respuesta: {respuesta}
Contexto: {contexto[:300]}...

Responde en formato JSON: {{"calidad": 1-10, "comentario": "..."}}
"""
    try:
        mensajes = [{"role": "user", "content": prompt}]
        res = llamar_ia(mensajes, response_format={"type": "json_object"})
        content = res.choices[0].message.content
        # Limpiar posible markdown si viene de Gemini
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except:
        return {"calidad": 5, "comentario": "Error en evaluación"}
