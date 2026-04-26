from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import json
import os
from config import client_openai
from model_factory import llamar_ia
from extractor import extraer_datos
from engine import (
    evaluar_respuesta, TOOLS, 
    guardar_datos_cliente, registrar_pregunta_sin_respuesta, 
    obtener_resumen_leads, obtener_flujos_n8n,
    leer_codigo_proyecto, listar_archivos_proyecto, crear_documento_wiki
)
from agents_registry import obtener_prompts_agente
from router import clasificar_intencion
from vector_store import indexar_texto, buscar_contexto
from logger import log_interaccion

app = FastAPI()

# 1. Cargar datos e indexar
perfil, resumen = extraer_datos()
indexar_texto(perfil, "curriculum_pdf")
indexar_texto(resumen, "resumen_txt")
if os.path.exists("conocimiento_extra.txt"):
    with open("conocimiento_extra.txt", "r", encoding="utf-8") as f:
        indexar_texto(f.read(), "proyectos_extra")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    mensaje = data.get("message")
    historial = data.get("history", [])
    
    try:
        # 1. ORQUESTACIÓN
        agente_nombre = clasificar_intencion(mensaje, historial)
        print(f"\n>>> [ORQUESTADOR] Delegando a: {agente_nombre.upper()}", flush=True)
        
        # 2. Contexto y Prompts
        contexto_relevante = buscar_contexto(mensaje)
        prompt_sistema_base, prompt_evaluador = obtener_prompts_agente(perfil, resumen, agente_nombre)
        prompt_con_contexto = prompt_sistema_base + f"\n\n## CONTEXTO RELEVANTE RECUPERADO:\n{contexto_relevante}\n"
        
        # 3. Preparar mensajes
        mensajes = [{"role": "system", "content": prompt_con_contexto}]
        for h in historial:
            mensajes.append({"role": "user", "content": h[0]})
            mensajes.append({"role": "assistant", "content": h[1]})
        mensajes.append({"role": "user", "content": mensaje})
        
        # 4. Chat + Tools (vía model_factory)
        respuesta = llamar_ia(mensajes, tools=TOOLS)
        
        msg_respuesta = respuesta.choices[0].message
        
        if msg_respuesta.tool_calls:
            print(f">>> [{agente_nombre.upper()}] Usando herramientas...", flush=True)
            mensajes.append(msg_respuesta)
            for tool_call in msg_respuesta.tool_calls:
                nombre_funcion = tool_call.function.name
                argumentos = json.loads(tool_call.function.arguments)
                
                if nombre_funcion == "guardar_datos_cliente":
                    resultado = guardar_datos_cliente(**argumentos)
                elif nombre_funcion == "registrar_pregunta_sin_respuesta":
                    resultado = registrar_pregunta_sin_respuesta(**argumentos)
                elif nombre_funcion == "obtener_resumen_leads":
                    resultado = obtener_resumen_leads()
                elif nombre_funcion == "obtener_flujos_n8n":
                    resultado = obtener_flujos_n8n()
                elif nombre_funcion == "leer_codigo_proyecto":
                    resultado = leer_codigo_proyecto(**argumentos)
                elif nombre_funcion == "listar_archivos_proyecto":
                    resultado = listar_archivos_proyecto()
                elif nombre_funcion == "crear_documento_wiki":
                    resultado = crear_documento_wiki(**argumentos)
                else:
                    resultado = "Error: Función no encontrada."
                
                mensajes.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": nombre_funcion,
                    "content": resultado
                })
            
            # Segunda llamada tras herramientas
            segunda_res = llamar_ia(mensajes)
            respuesta_chat = segunda_res.choices[0].message.content
        else:
            respuesta_chat = msg_respuesta.content

        # 5. Calidad
        evaluacion = evaluar_respuesta(respuesta_chat, mensaje, str(historial), prompt_evaluador)
        log_interaccion(mensaje, respuesta_chat, evaluacion, 1)
        
        return {
            "response": respuesta_chat,
            "agent": agente_nombre
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error interno: {error_msg}")
        return {"response": f"❌ Error interno: {error_msg}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
