import google.generativeai as genai
from config import client_openai, MODEL_GEMINI, MODEL_GPT
import os
import json

# Configurar Gemini Nativo
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def llamar_ia(mensajes, tools=None, response_format=None):
    """
    Intenta llamar a Gemini (Nativo) primero. Si falla, usa GPT (OpenAI).
    """
    try:
        print(">>> [IA] Intentando con Gemini (Nativo)...", flush=True)
        
        # 1. Separar System Instruction de Mensajes y validar tipos
        system_instruction = ""
        gemini_messages = []
        
        for m in mensajes:
            # Manejar tanto diccionarios como objetos de mensaje de OpenAI
            role = getattr(m, 'role', m.get('role') if isinstance(m, dict) else None)
            content = getattr(m, 'content', m.get('content') if isinstance(m, dict) else "")
            
            if role == "system":
                system_instruction = content if content else ""
            elif role == "user":
                if content:
                    gemini_messages.append({"role": "user", "parts": [content]})
            elif role == "assistant":
                if content:
                    gemini_messages.append({"role": "model", "parts": [content]})
            # No enviamos 'tool' o mensajes con 'tool_calls' a Gemini Nativo por ahora
            # para evitar errores de esquema complejos en el fallback simple.

        # 2. Configurar Modelo
        model_kwargs = {"model_name": MODEL_GEMINI}
        if system_instruction:
            model_kwargs["system_instruction"] = system_instruction
            
        model = genai.GenerativeModel(**model_kwargs)
        
        # 3. Validar herramientas (si hay herramientas, forzamos GPT para estabilidad)
        if tools:
            raise Exception("Tools detected, redirecting to GPT for better tool-calling support")

        # 4. Generar Contenido (Llamada simple)
        if not gemini_messages:
            raise Exception("No valid user/model messages for Gemini")
            
        respuesta = model.generate_content(gemini_messages)
        print(">>> [IA] Respuesta de Gemini (Nativo) OK.", flush=True)
        
        # Simular objeto respuesta de OpenAI para compatibilidad
        class MockMessage:
            def __init__(self, text):
                self.content = text
                self.tool_calls = None
                self.role = "assistant"
                
        class MockChoice:
            def __init__(self, text):
                self.message = MockMessage(text)
                
        class MockResponse:
            def __init__(self, text):
                self.choices = [MockChoice(text)]
        
        return MockResponse(respuesta.text)

    except Exception as e:
        print(f">>> [IA] Gemini Nativo saltado/error: {e}", flush=True)
        print(">>> [IA] Usando GPT-4o-mini (Fallback)...", flush=True)
        return llamar_gpt(mensajes, tools, response_format)

def llamar_gpt(mensajes, tools=None, response_format=None):
    """Llamada directa a OpenAI GPT."""
    kwargs = {
        "model": MODEL_GPT,
        "messages": mensajes
    }
    if tools:
        kwargs["tools"] = tools
    if response_format:
        kwargs["response_format"] = response_format
        
    return client_openai.chat.completions.create(**kwargs)
