**Project Overview**  
-ClaudeTodo is a simple web apps to for ToDo Notes

**Tech Stack**  
- Backend: Python 3.10+, FastAPI, SQLAlchemy 2.0 ORM, Azure SQL Server (pyodbc + ODBC Driver 18)
- Frontend: React 18 with Vite, plain CSS, functional components only

**Code Style**  
- Python: snake_case for all names, type hints on every function and return value
- JavaScript: camelCase for variables, PascalCase for React components
- No inline CSS -- all styles go in .css files

**Archtectural Rules**  
- All API routes in `backend/main.py`
- All frontend API calls go through `frontend/src/api.js`
- Frontend state with React hooks only

**Command**  
- Backend: `uvicorn main:app --reload (run from `backend\`)
- Frontend: `npm run dev` (run from `frontend/`)


