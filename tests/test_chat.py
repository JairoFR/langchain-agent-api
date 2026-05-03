# pytest levanta una versión de prueba de la app sin necesidad de correr uvicorn.
# TestClient de FastAPI/Starlette simula requests HTTP reales contra la app.
import pytest
from fastapi.testclient import TestClient
from main import app

# Cliente de prueba — reemplaza al curl en los tests
client = TestClient(app)


def test_health():
    """Verifica que el servidor esté vivo."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_responde():
    """Verifica que el endpoint /chat/ devuelve una respuesta válida."""
    response = client.post("/chat/", json={
        "message": "Hola",
        "session_id": "test_session"
    })
    assert response.status_code == 200

    data = response.json()
    # Verifica que los campos existen en la respuesta
    assert "response" in data
    assert "session_id" in data
    # Verifica que la respuesta no está vacía
    assert len(data["response"]) > 0
    # Verifica que el session_id se devuelve correctamente
    assert data["session_id"] == "test_session"


def test_chat_historial():
    """
    Verifica que el historial funciona:
    el agente debe recordar mensajes anteriores en la misma sesión.
    """
    session = "test_historial"

    # Primer mensaje
    r1 = client.post("/chat/", json={
        "message": "Mi nombre es Jairo",
        "session_id": session
    })
    assert r1.status_code == 200

    # Segundo mensaje — el agente debe recordar el nombre
    r2 = client.post("/chat/", json={
        "message": "¿Cómo me llamo?",
        "session_id": session
    })
    assert r2.status_code == 200
    # El nombre debe aparecer en la respuesta
    assert "Jairo" in r2.json()["response"]


def test_sesiones_independientes():
    """
    Verifica que dos sesiones distintas no comparten historial.
    """
    # Sesión A presenta un nombre
    client.post("/chat/", json={
        "message": "Mi nombre es Jairo",
        "session_id": "sesion_a"
    })

    # Sesión B no debería saber el nombre
    r = client.post("/chat/", json={
        "message": "¿Sabes cómo me llamo?",
        "session_id": "sesion_b"
    })
    assert r.status_code == 200
    # La sesión B no tiene contexto del nombre
    assert "Jairo" not in r.json()["response"]