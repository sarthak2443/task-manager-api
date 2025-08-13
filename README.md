# Task Manager API (Flask + JWT)

A minimal, tidy REST API with JWT auth, role-based access, pagination, and Swagger docs.

## Quickstart

```bash
# 1) create venv
python -m venv .venv && . .venv/Scripts/activate  # on Windows
# or: source .venv/bin/activate                    # on macOS/Linux

# 2) install deps
pip install -r requirements.txt

# 3) env (optional)
set JWT_SECRET_KEY=change-this   # Windows CMD
# export JWT_SECRET_KEY=change-this  # macOS/Linux

# 4) init db
flask --app run db init
flask --app run db migrate -m "init"
flask --app run db upgrade

# 5) run
python run.py

## Quickstart

Tested on Postman
<img width="1280" height="755" alt="image" src="https://github.com/sarthak2443/task-manager-api/main/image.png">


