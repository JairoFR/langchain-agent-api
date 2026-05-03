# El router define los endpoints HTTP de este módulo.
# FastAPI usa decoradores (@router.post) para mapear rutas a funciones.
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.core.agente import chat_with_agent

# prefix="/chat" → todas las rutas de este router empiezan con /chat
# tags=["chat"]  → agrupa los endpoints en la documentación de Swagger UI
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal: POST /chat/
    
    Recibe un JSON con { "message": "...", "session_id": "..." }
    Devuelve un JSON con { "response": "...", "session_id": "..." }
    
    response_model=ChatResponse le dice a FastAPI cómo serializar la respuesta
    y qué mostrar en la documentación automática (/docs).
    """
    try:
        # Llamamos al agente pasando el mensaje y la sesión
        reply = await chat_with_agent(request.message, request.session_id)

        # Retornamos el modelo de respuesta con los datos
        return ChatResponse(response=reply, session_id=request.session_id)

    except Exception as e:
        # Si algo falla (API key inválida, timeout, etc.), devolvemos error 500
        # detail=str(e) muestra el mensaje de error original para debug
        raise HTTPException(status_code=500, detail=str(e))