# ClaudeTodo

A lightweight task management web app built with React (Vite) + Python (FastAPI).

## Structure

```
claudetodo/
├── backend/          # FastAPI REST API
│   ├── main.py
│   └── requirements.txt
├── frontend/         # React + Vite UI
│   └── src/App.jsx
└── PRD.md
```

## Getting started

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# API available at http://localhost:8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
# UI available at http://localhost:5173
```

## API

| Method | Endpoint      | Description          |
|--------|---------------|----------------------|
| GET    | /health       | Health check         |
| GET    | /todos        | List all todos       |
| POST   | /todos        | Create a todo        |
| PATCH  | /todos/{id}   | Toggle completed     |
| DELETE | /todos/{id}   | Delete a todo        |
