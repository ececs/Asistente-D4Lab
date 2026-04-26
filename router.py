from model_factory import llamar_ia
import json

def clasificar_intencion(mensaje, historial):
    """
    Clasifica la intención del usuario para delegar al agente correcto.
    """
    prompt = f"""
Clasifica el siguiente mensaje de usuario en una de estas categorías:
- COMERCIAL: Consultas sobre servicios, precios, contratación de D4Lab o TesIA.
- MARKETING: Ideas de contenido, embudos de venta, estrategia de crecimiento.
- TECNICO: Dudas sobre n8n, automatización, IA, infraestructura local.
- OPERACIONES: Gestión de tareas, organización, dudas internas de Eudaldo.
- CALIDAD: Revisión de código, detección de errores, seguridad, buenas prácticas.
- DOCUMENTACION: Creación de manuales, explicaciones técnicas, Wiki del proyecto.
- ESTUDIANTE: Dudas de alumnos, temario de oposiciones, motivación, consejos de estudio.

Historial reciente: {historial[-2:] if historial else "Ninguno"}
Mensaje: "{mensaje}"

Responde UNICAMENTE con el nombre de la categoría en minúsculas (comercial, marketing, tecnico, operaciones).
"""
    
    mensajes = [{"role": "user", "content": prompt}]
    respuesta = llamar_ia(mensajes)
    
    intencion = respuesta.choices[0].message.content.strip().lower()
    
    # Validar que sea una de las opciones
    validas = ["comercial", "marketing", "tecnico", "operaciones", "calidad", "documentacion", "estudiante"]
    for v in validas:
        if v in intencion:
            return v
            
    return "comercial" # Por defecto
