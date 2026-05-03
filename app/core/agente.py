# Este es el corazón del proyecto: aquí vive la lógica del agente IA.
# LangChain actúa como el "orquestador" que conecta el historial con el LLM.

from langchain_groq import ChatGroq
# HumanMessage = mensaje del usuario
# SystemMessage = instrucciones iniciales al modelo (personalidad, idioma, etc.)
from langchain_core.messages import HumanMessage, SystemMessage
# InMemoryChatMessageHistory guarda el historial de conversación en RAM
from langchain_core.chat_history import InMemoryChatMessageHistory
from app.core.config import settings

# Diccionario que guarda un historial por cada session_id.
# Clave: session_id (str) → Valor: historial de mensajes
# Ejemplo: {"jairo": [HumanMessage(...), AIMessage(...), ...]}
_sessions: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Retorna el historial de conversación para una sesión dada.
    Si no existe, crea uno nuevo vacío.
    Esto permite que cada usuario tenga su propia conversación independiente.
    """
    if session_id not in _sessions:
        _sessions[session_id] = InMemoryChatMessageHistory()
    return _sessions[session_id]


def get_llm() -> ChatGroq:
    """
    Crea y retorna una instancia del modelo LLM (Groq + LLaMA3).
    - api_key: se obtiene del .env via settings
    - model: llama3-8b-8192 es rápido y gratuito en Groq
    - temperature: 0.7 = respuestas creativas pero coherentes (0=robótico, 1=muy creativo)
    """
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama-3.1-8b-instant",
        temperature=0.7,
    )


async def chat_with_agent(message: str, session_id: str) -> str:
    """
    Función principal: recibe un mensaje y devuelve la respuesta del agente.
    Es async porque la llamada al LLM es una operación de red (I/O).
    """
    llm = get_llm()

    # Recuperamos (o creamos) el historial de esta sesión
    history = get_session_history(session_id)

    # Guardamos el nuevo mensaje del usuario en el historial
    history.add_user_message(message)

    # Construimos la lista completa de mensajes para enviar al LLM:
    # [SystemMessage, ...todos los mensajes anteriores..., último HumanMessage]
    # El * desempaqueta la lista history.messages dentro de la nueva lista
    messages = [
        SystemMessage(content="Eres un asistente útil y conciso. Responde siempre en el idioma del usuario."),
        *history.messages,  # Incluye todo el historial: humano + IA alternados
    ]

    # ainvoke = llamada asíncrona al modelo. Envía todos los mensajes y espera respuesta.
    response = await llm.ainvoke(messages)

    # response.content contiene el texto de la respuesta del modelo
    assistant_reply = response.content

    # Guardamos la respuesta del modelo en el historial para la próxima vuelta
    history.add_ai_message(assistant_reply)

    return assistant_reply