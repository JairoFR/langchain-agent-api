# LangChain Agent API — P5

API conversacional con memoria de sesión construida con FastAPI, LangChain y Groq.

## Stack

- **FastAPI** — framework web async
- **LangChain** — orquestación del agente IA
- **Groq API** — LLM ultrarrápido (llama-3.1-8b-instant)
- **Pydantic V2** — validación de datos
- **Pytest** — tests automatizados

```bash
## Estructura
langchain-agent-api/
├── main.py                  # Punto de entrada
├── app/
│   ├── core/
│   │   ├── agente.py        # Lógica LangChain + historial por sesión
│   │   └── config.py        # Variables de entorno
│   ├── models/
│   │   └── chat.py          # Schemas Pydantic (request/response)
│   └── routers/
│       └── chat.py          # Endpoints FastAPI
├── tests/
│   └── test_chat.py         # 4 tests automatizados
├── .env.example
├── requirements.txt
└── Dockerfile
```

## Instalación

```bash
git clone https://github.com/JairoFR/langchain-agent-api
cd langchain-agent-api
python -m venv env && source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Uso

```bash
uvicorn main:app --reload
```

### Endpoint principal
POST /chat/

**Request:**
```json
{
  "message": "Hola, ¿qué puedes hacer?",
  "session_id": "jairo"
}
```

**Response:**
```json
{
  "response": "Puedo ayudarte con...",
  "session_id": "jairo"
}
```

### Otros endpoints
GET /health     → {"status": "ok"}
GET /docs       → Swagger UI interactivo

## Tests

```bash
pytest tests/test_chat.py -v
```

4 tests cubiertos:
- `test_health` — servidor activo
- `test_chat_responde` — respuesta válida del agente
- `test_chat_historial` — memoria de sesión funciona
- `test_sesiones_independientes` — sesiones aisladas entre usuarios

## Cómo funciona
Usuario → POST /chat/ → router → agente.py → LangChain → Groq API → respuesta
↕
historial en memoria
(por session_id)

Cada `session_id` mantiene su propio historial de conversación en memoria.
Sesiones distintas no comparten contexto.

## Variables de entorno

| Variable | Descripción |
|---|---|
| `GROQ_API_KEY` | API key de Groq (console.groq.com) |

##Uso

- [x] Agente conversacional básico
- [x] Historial por sesión en memoria