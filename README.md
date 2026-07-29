# JobTracker

A personal tool for tracking job applications — company, role, status, and
notes — built to replace the spreadsheet I was using to track my own job
search.

## Status

🚧 In development. Backend skeleton is up and running (FastAPI + SQLModel +
SQLite), with `GET /applications` working end-to-end. Create/update/delete
endpoints, tests, and the frontend are in progress.

## Tech stack

- **Backend:** FastAPI, SQLModel, SQLite
- **Frontend:** React (Vite) — coming soon
- **Testing:** pytest

## What it does (planned)

- Log a job application: company, role, status, notes, applied date
- Move an application through statuses: `applied → interviewing → offer / rejected`
- Filter and view applications by status
- (Stretch) Simple stats — how many applications are at each stage

## Running it locally

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`

Visit `http://localhost:8000/docs` for interactive API docs.
