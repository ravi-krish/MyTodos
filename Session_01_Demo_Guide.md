# Session 1 — Demo Guide
## Setup & The CLI Mental Model

---

## Before You Start

Have these ready:
- Terminal open in a clean working directory (e.g. `~/demos/`)
- Claude Code installed (`claude --version` works)
- Python 3.10+ and Node.js 18+ installed
- Browser open at claude.ai

---

## Section 1: Project Setup Demo

### Step 1 — Write the PRD in Claude Chat

Open claude.ai in the browser. Use this prompt:

```
Write a Product Requirements Document for a Todo app called ClaudeTodo.
The app should let users create todos, mark them as complete, and delete them.
The frontend should be React (Vite). The backend should be Python FastAPI.
Keep the PRD clear and concise — one to two pages.
```

Copy the output. Save it as `PRD.md` in a new folder:

```bash
mkdir claudetodo
cd claudetodo
# paste the PRD content into PRD.md
```

Point out to the audience: "We always start with requirements. Claude Code builds better when it knows what to build."

---

### Step 2 — Launch Claude Code

```bash
claude
```

Wait for the prompt to appear. Explain: "This is interactive mode — a full session where Claude can read our files, write code, and run commands."

---

### Step 3 — Scaffold the Project

Type the following prompt inside the Claude Code session:

```
Read PRD.md and scaffold the ClaudeTodo project from it.

Create:
- backend/ with a FastAPI app (main.py) that has a single GET /health endpoint returning {"status": "ok"}
- backend/requirements.txt with fastapi and uvicorn
- frontend/ using Vite + React (run npm create vite@latest)
- frontend/src/App.jsx showing a "Hello ClaudeTodo" placeholder
- README.md with a brief project description

After creating the files, confirm the structure is correct.
```

**While Claude runs — narrate what you see in the terminal:**
- "Claude is reading PRD.md — that's the Read tool"
- "Now it's writing the backend structure — that's the Write tool"
- "It's running npm create vite to scaffold the frontend — that's Bash"
- "Now it's verifying the files exist — Glob again"

Let the tool loop run without interrupting.

---

### Step 4 — Run the Backend

Open a second terminal tab:

```bash
cd claudetodo/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open browser: `http://localhost:8000/health`

Show the response: `{"status": "ok"}`

"The backend is live. FastAPI is running. Claude wrote this from nothing but a PRD."

---

### Step 5 — Run the Frontend

Open a third terminal tab:

```bash
cd claudetodo/frontend
npm install
npm run dev
```

Open browser: `http://localhost:5173`

Show the "Hello ClaudeTodo" placeholder in the browser.

---

### Step 6 — Show the File Structure

Back in the first terminal:

```bash
ls -R claudetodo/
```

Or inside Claude Code:

```
Show me the project structure as a tree
```

Walk through the files. Point out what Claude created autonomously from the PRD.

---

## Wrap Up

Return to slides.

Say: "That entire project scaffold — both a working backend and a running frontend — from a single prompt. Now you're going to do the same thing in the lab."

---

## Troubleshooting

**npm create vite fails:** Run it manually — `cd frontend && npm create vite@latest . -- --template react` then let Claude know to continue.

**uvicorn not found:** `pip install uvicorn` then retry.

**Port 8000 in use:** Kill the existing process — `lsof -ti:8000 | xargs kill` — then rerun uvicorn.
