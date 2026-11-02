# PasameEso

Crowd-sourced repository of class notes, practice exams and study guides for UPRRP students, organized by course and professor. Built for CCOM 4030 (Software Engineering) by Juan Ocasio, Alberto Barreto, Carlos Aparicio and Miguel A. Hernández.

The **SRS (v1.0)** defines *what* the system does and the **System Design (v1.2)** defines *how*. Code comments reference their IDs (e.g. `REQ.4.2`, `NFR-SEC-04`) so every piece of code traces back to a requirement.

**Stack:** Python 3 · Flask · SQLite · bcrypt · HTML5/CSS3 · Docker

---

## Getting started (first time)

You need **Python 3.11+** and **Git**.

```bash
git clone https://github.com/juanocasio03/Pasame-Eso.git
cd Pasame-Eso

# 1. Create a virtual environment (keeps this project's packages separate)
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your local settings file
cp .env.example .env               # Windows: copy .env.example .env

# 4. Create the database and fill it with sample data
flask --app app init-db
flask --app app seed-db

# 5. Run the app
flask --app app run --debug
```

Open <http://127.0.0.1:5000>. Sample logins created by `seed-db`:

| Role        | Username    | Password         |
|-------------|-------------|------------------|
| Moderator   | `moderator` | `moderator123`   |
| Contributor | `ana`       | `contributor123` |

(Login itself is still a TODO, so these work once `User.login()` is implemented.)

### Run the tests

```bash
pytest
```

Tests also run automatically on GitHub for every pull request (see the **Actions** tab).

### Run with Docker

```bash
cp .env.example .env    # set a real SECRET_KEY
docker compose up --build
```

The app is served at <http://localhost:8000>. The database and uploads live in a Docker volume, so they survive rebuilds.

---

## Project structure

The code follows the **MVC architecture** from System Design Section 2.

```
app/
├── __init__.py          # create_app(): wires config, database and controllers together
├── config.py            # all settings, read from .env (NFR-PORT-04)
├── db.py                # SQLite connection + `init-db` / `seed-db` commands
├── schema.sql           # database tables (System Design Section 5)
├── models/              # MODEL: data + business logic (UML classes, Section 3.2)
│   ├── user.py          #   register, login, deactivate, delete
│   ├── post.py          #   create, edit, delete, search, rate, comment
│   └── report.py        #   create, list_queue, resolve
├── controllers/         # CONTROLLER: URL routes (Flask blueprints)
│   ├── decorators.py    #   @login_required, @moderator_required (NFR-SEC-04)
│   ├── main.py          #   home feed + search, help page
│   ├── auth.py          #   register, login, logout
│   ├── posts.py         #   create/view/edit, rate, comment, report
│   └── moderation.py    #   moderator dashboard and report queue
├── templates/           # VIEW: HTML pages (Screens 1–5, Section 4)
├── static/css/style.css # VIEW: color palette and layout
└── utils/files.py       # SHA-256 fingerprints + file-type detection (REQ.4.2)
tests/                   # pytest tests
instance/                # created automatically: local database + uploads (NOT in Git)
```

**Where do I put my code?** A feature usually touches one model method, one controller route and one template. For example, duplicate detection (REQ.4.2) lives in `Post.create()` in `models/post.py`, is called from `create()` in `controllers/posts.py`, and shows its error in `templates/posts/create.html`. Methods that still need work raise `NotImplementedError` or are marked `TODO`.

---

## How we work (team workflow)

1. **Pick an issue** from the GitHub Projects board and assign yourself.
2. **Update main and create a branch**:
   ```bash
   git checkout main
   git pull
   git checkout -b feat/upload-duplicate-detection
   ```
   Branch prefixes: `feat/` new feature, `fix/` bug fix, `docs/` documentation, `test/` tests only.
3. **Commit small and often** with clear messages: `Add SHA-256 duplicate check (REQ.4.2)`.
4. **Push and open a pull request**:
   ```bash
   git push -u origin feat/upload-duplicate-detection
   ```
   Fill in the PR template, link the issue (`Closes #12`) and ask a teammate to review.
5. **Merge after one approval and green tests.** Never push directly to `main`.

### Rules

- **Never commit** `.env`, database files (`*.sqlite`, `*.db`) or anything in `instance/`. They're already in `.gitignore`.
- **Database changes go through `schema.sql` only.** After pulling a change to it, re-run `flask --app app init-db` and `flask --app app seed-db` (this wipes your local data).
- **Always use `?` placeholders in SQL**, never f-strings or `+`, to prevent SQL injection.
- **Add a test** for any logic you write in `models/` or `utils/`.
- Keep the SRS IDs in comments and PR descriptions so we can show traceability.
