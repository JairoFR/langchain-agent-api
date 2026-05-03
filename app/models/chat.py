# Los modelos definen la "forma" de los datos que entran y salen de la API.
# Pydantic valida automáticamente que los datos cumplan el tipo esperado.
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Lo que el cliente envía al hacer POST /chat/"""
    message: str          # El mensaje del usuario, ej: "¿Qué es LangChain?"
    session_id: str = "default"  # ID para mantener historial por usuario/sesión

class ChatResponse(BaseModel):
    """Lo que la API devuelve al cliente"""
    response: str         # La respuesta generada por el agente IA
    session_id: str       # Devolvemos el session_id para que el cliente lo rastree