# OSPOLY_Chatbot_WhatsApp

A ready-to-run Flask web app with a WhatsApp-style chat UI, a pull-down menu of common questions, and an admin area to add/edit/delete Q&A.

## Features
- WhatsApp-inspired chat interface
- Pull-down menu + clickable question list
- SQLite database with your Q&A pre-seeded
- Admin login (default `admin` / `admin123` — change in production)
- Full CRUD for questions and answers

## Quick Start
```bash
# 1) Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Initialize the database (creates DB and seeds content)
flask --app app init-db

# 4) Run the server
flask --app app run  # or: python app.py
```

Open http://127.0.0.1:5000 in your browser.

- Admin area: http://127.0.0.1:5000/admin (login then manage Q&A)
- Default admin: `admin` / `admin123`

## Notes
- Change `SECRET_KEY` (env var) for security in production.
- The UI mimics WhatsApp styling but does not connect to WhatsApp APIs.
