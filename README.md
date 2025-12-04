# LangChain minimal Docker example

This repository contains a minimal example to run a LangChain-based app that calls OpenAI, using Docker Compose.

Quick start

1. Copy `.env.example` to `.env` and set your OpenAI API key:

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY
```

2. Build and run with Docker Compose:

```bash
docker compose up --build
```

What this does
- Builds an image from `Dockerfile` (installs `requirements.txt` into the image).
- Runs `app/main.py`, which attempts to initialize a small LangChain agent (if compatible), falls back to an `LLMChain` call, and finally tries a direct OpenAI API call.

Notes
- Keep your real `.env` out of version control. `.env.example` shows required keys.
- LangChain has had API changes; the code includes fallbacks to remain compatible across minor LangChain versions. If you want a specific tested combination, pin versions in `requirements.txt` (for example `langchain==0.x.y`).
