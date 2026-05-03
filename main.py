# Punto de entrada de la aplicación FastAPI.
# Uvicorn ejecuta este archivo cuando corres: uvicorn main:app --reload
from fastapi import FastAPI
from app.routers.chat import router as chat_router

# Instancia principal de la app. El título aparece en /docs (Swagger UI)
app = FastAPI(title="LangChain Agent API")

# Registramos el router de chat. Todos sus endpoints quedan disponibles.
# El router tiene prefix="/chat", así que el endpoint queda en POST /chat/
app.include_router(chat_router)


@app.get("/health")
def health():
    """
    Endpoint simple para verificar que la API está viva.
    Útil para Docker healthchecks y monitoreo.
    GET /health → {"status": "ok"}
    """
    return {"status": "ok"}