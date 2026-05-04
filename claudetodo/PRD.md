# Product Requirements Document
## ClaudeTodo

**Version:** 1.0  
**Date:** April 28, 2026  
**Status:** Draft

---

## 1. Overview

ClaudeTodo is a lightweight task management web application that allows users to create, complete, and delete personal todos. It is built with a React (Vite) frontend and a Python FastAPI backend, communicating over a REST API.

---

## 2. Goals

- Deliver a fast, minimal todo experience with zero friction.
- Provide a clean REST API that can support future clients (mobile, CLI).
- Serve as a reference implementation for a Vite + FastAPI full-stack project.

---

## 3. User Stories

| # | As a user, I want to…                        | So that…                              |
|---|----------------------------------------------|---------------------------------------|
| 1 | Create a new todo with a title               | I can track things I need to do       |
| 2 | See all my todos in a list                   | I have a clear view of pending work   |
| 3 | Mark a todo as complete (and unmark it)      | I can track progress                  |
| 4 | Delete a todo                                | I can remove items I no longer need   |

---

## 4. Functional Requirements

### 4.1 Frontend (React + Vite)

- **Todo List View** — Display all todos on initial load, fetched from the API. Each item shows title, completion status (checkbox), and a delete button.
- **Add Todo** — An input field + submit button at the top of the list. Submitting a non-empty title calls the create API and appends the new item to the list without a full page reload.
- **Toggle Complete** — Clicking the checkbox calls the update API and reflects the new state immediately in the UI.
- **Delete Todo** — Clicking the delete button calls the delete API and removes the item from the list immediately.
- **Empty State** — Show a friendly message when no todos exist.
- **Error Handling** — Display a non-blocking error message if any API call fails.

### 4.2 Backend (Python FastAPI)

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| GET    | `/todos`          | Return all todos                   |
| POST   | `/todos`          | Create a new todo                  |
| PATCH  | `/todos/{id}`     | Update `completed` status by ID    |
| DELETE | `/todos/{id}`     | Delete a todo by ID                |

- All responses use JSON.
- Todos are stored in-memory (a Python list) for v1.0; persistence is out of scope.
- CORS is enabled to allow the Vite dev server (`localhost:5173`) to communicate with the API (`localhost:8000`).

### 4.3 Data Model

```json
{
  "id": "string (UUID)",
  "title": "string",
  "completed": "boolean",
  "created_at": "ISO 8601 datetime"
}
```

---

## 5. Non-Functional Requirements

| Concern        | Requirement                                                    |
|----------------|----------------------------------------------------------------|
| Performance    | API responses under 100ms on localhost                         |
| Usability      | App is usable without documentation; UI is self-explanatory    |
| Compatibility  | Supports latest stable Chrome, Firefox, and Safari             |
| Code Quality   | Backend uses Pydantic models for request/response validation   |

---

## 6. Out of Scope (v1.0)

- User authentication / multi-user support
- Database persistence (PostgreSQL, SQLite, etc.)
- Due dates, priorities, or categories
- Drag-and-drop reordering
- Deployment / Docker configuration

---

## 7. Tech Stack Summary

| Layer     | Technology            |
|-----------|-----------------------|
| Frontend  | React 18, Vite 5      |
| Backend   | Python 3.11, FastAPI  |
| API Style | REST / JSON           |
| State     | React `useState`      |
| Storage   | In-memory (v1.0)      |

---

## 8. Success Criteria

- A user can complete the full create → complete → delete lifecycle with no console errors.
- All four API endpoints return correct status codes (`200`, `201`, `204`, `404`).
- The frontend reflects all state changes without requiring a page refresh.
