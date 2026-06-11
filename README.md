# Admin Panel Generator — Python + SQL

> A terminal-based admin panel that auto-generates a full CRUD interface for any SQL database. Connects to SQLite or MySQL, detects your tables automatically, and provides a complete admin UI without writing any frontend code.

---

## Features

- **Auto-detects tables** — no configuration needed, just point it at a database
- **Full CRUD** — Create, Read, Update, Delete for every table
- **Smart primary key detection** — auto-skips auto-increment fields on insert
- **Search** — filter records by any column
- **CSV export** — export any table to a timestamped CSV file
- **SQLite + MySQL support** — works with both, swap connector in one line
- **Demo mode** — creates sample `users` and `products` tables if no DB exists

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/mrunaliyadav003/Admin-Panel-Generator-using-Python-Sql.git
cd Admin-Panel-Generator-using-Python-Sql

# Run (SQLite — no install needed)
python admin_panel.py
```

First run creates a demo database with `users` and `products` tables automatically.

---

## MySQL Setup

1. Install the MySQL connector:
```bash
pip install mysql-connector-python
```

2. Edit `mysql_connector.py` with your credentials:
```python
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "your_user",
    "password": "your_password",
    "database": "your_database"
}
```

3. Replace the `get_connection()` import in `admin_panel.py` with the MySQL version.

---

## How It Works

```
Start
  ↓
Connect to database (SQLite or MySQL)
  ↓
Auto-detect all tables + record counts
  ↓
User selects a table
  ↓
CRUD menu auto-generated from table schema
  ↓
View / Add / Edit / Delete / Search / Export
```

---

## Demo Screenshots

```
============================================================
  ADMIN PANEL GENERATOR — Python + SQL
============================================================

  Available tables:

  [1] users                          (3 records)
  [2] products                       (3 records)

  [0] Exit
```

```
============================================================
  VIEW ALL — USERS
============================================================

  id | name          | email                | role  | created_at
  ---+---------------+----------------------+-------+-----------
  1  | Alice Smith   | alice@example.com    | admin | 2026-06-11
  2  | Bob Jones     | bob@example.com      | user  | 2026-06-11
  3  | Carol White   | carol@example.com    | user  | 2026-06-11

  Total: 3 record(s)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Database | SQLite (built-in) / MySQL |
| ORM | None — raw SQL via `sqlite3` / `mysql-connector` |
| Interface | Terminal / CLI |

---

## Project Structure

```
Admin-Panel-Generator-using-Python-Sql/
├── admin_panel.py        # Main application — SQLite
├── mysql_connector.py    # MySQL connector (swap in for MySQL)
├── requirements.txt      # Dependencies
└── README.md
```

---

## Use Cases

- Quick admin interface for any existing database
- Prototype CRUD operations without building a web UI
- Data entry tool for non-technical users
- Learning project for Python + SQL interaction patterns

---

*Part of the Python portfolio at [github.com/mrunaliyadav003](https://github.com/mrunaliyadav003)*
