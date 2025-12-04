Frontend and running locally

If you want to run the React frontend during development:

1. Install frontend dependencies and run the dev server:

```bash
cd frontend
npm install
npm run dev
```

2. Run the backend (in another terminal):

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

To serve the built frontend from the Python backend (so backend serves static files):

```bash
cd frontend
npm install
npm run build
# then run the backend; it will serve files from `frontend/dist`
uvicorn app.main:app --reload
```
