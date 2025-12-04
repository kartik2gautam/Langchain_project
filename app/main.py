import os
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Allow starting the app for frontend work without an API key
    print("Warning: OPENAI_API_KEY not set. Chat will fail until set.")


# Agent will be created on startup
agent = None


def _create_agent():
    """Create and return the LangChain agent."""
    from langchain.agents import create_agent

    def get_weather(city: str) -> str:
        """Mock weather tool."""
        return f"It's always sunny in {city}!"

    return create_agent(
        model="gpt-4o-mini",
        tools=[get_weather],
        system_prompt="You are a helpful assistant",
    )


@app.on_event("startup")
def startup_event():
    global agent
    try:
        agent = _create_agent()
        print("Agent initialized")
    except Exception as e:
        agent = None
        print("Agent initialization failed:", e)


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if agent is None:
        return JSONResponse({"error": "agent not initialized"}, status_code=500)

    try:
        response = agent.invoke({"messages": [{"role": "user", "content": req.message}]})
        print("Agent response:", response)
        # Convert response to string for robust fallback across LangChain versions
        return {"reply": response['messages'][1].content}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# Serve frontend (built) if available. When `main.py` is at /app, frontend lives at /app/frontend
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend", "dist"))
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    @app.get("/", response_class=HTMLResponse)
    def index():
        return "<h1>Frontend not built. Run `npm install` and `npm run build` in `frontend/`.</h1>"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)