"""
Admin Panel Generator using Python + SQL
Connects to a SQLite/MySQL database and auto-generates
a fully functional CRUD admin panel for any table.
"""

import sqlite3
import os
from datetime import datetime


# ── CONFIG ─────────────────────────────────────────────────────────────
DB_FILE = "admin_panel.db"


# ── DATABASE CONNECTION ─────────────────────────────────────────────────
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def get_tables(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return [row[0] for row in cursor.fetchall()]


def get_columns(conn, table):
    cursor = conn.execute(f"PRAGMA table_info({table})")
    return cursor.fetchall()


def get_all_rows(conn, table):
    cursor = conn.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()


def get_row_by_id(conn, table, pk_col, pk_val):
    cursor = conn.execute(f"SELECT * FROM {table} WHERE {pk_col} = ?", (pk_val,))
    return cursor.fetchone()


def insert_row(conn, table, columns, values):
    cols = ", ".join(columns)
    placeholders = ", ".join(["?" for _ in values])
    conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", values)
    conn.commit()


def update_row(conn, table, columns, values, pk_col, pk_val):
    set_clause = ", ".join([f"{col} = ?" for col in columns])
    conn.execute(f"UPDATE {table} SET {set_clause} WHERE {pk_col} = ?", values + [pk_val])
    conn.commit()


def delete_row(conn, table, pk_col, pk_val):
    conn.execute(f"DELETE FROM {table} WHERE {pk_col} = ?", (pk_val,))
    conn.commit()


# ── DISPLAY HELPERS ─────────────────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_table(rows, columns):
    if not rows:
        print("  (no records found)")
        return
    col_names = [col[1] for col in columns]
    widths = [max(len(str(col_names[i])), max(len(str(row[i])) for row in rows)) for i in range(len(col_names))]
    header = " | ".join(str(col_names[i]).ljust(widths[i]) for i in range(len(col_names)))
    separator = "-+-".join("-" * w for w in widths)
    print("\n  " + header)
    print("  " + separator)
    for row in rows:
        print("  " + " | ".join(str(row[i]).ljust(widths[i]) for i in range(len(row))))
    print(f"\n  Total: {len(rows)} record(s)")


# ── CRUD OPERATIONS ─────────────────────────────────────────────────────
def view_records(conn, table):
    print_header(f"VIEW ALL — {table.upper()}")
    columns = get_columns(conn, table)
    rows = get_all_rows(conn, table)
    print_table(rows, columns)
    input("\n  Press Enter to continue...")


def add_record(conn, table):
    print_header(f"ADD RECORD — {table.upper()}")
    columns = get_columns(conn, table)
    # Skip auto-increment primary key
    editable = [col for col in columns if not (col[5] == 1 and col[2] == 'INTEGER')]
    if not editable:
        editable = [col for col in columns if col[5] != 1]
    values = []
    col_names = []
    for col in editable:
        col_name = col[1]
        col_type = col[2]
        not_null = col[3]
        default = col[4]
        prompt = f"  {col_name} ({col_type})"
        if default:
            prompt += f" [default: {default}]"
        if not not_null:
            prompt += " (optional)"
        prompt += ": "
        val = input(prompt).strip()
        if val == "" and default:
            val = default
        col_names.append(col_name)
        values.append(val if val else None)
    try:
        insert_row(conn, table, col_names, values)
        print("\n  Record added successfully!")
    except Exception as e:
        print(f"\n  Error: {e}")
    input("  Press Enter to continue...")


def edit_record(conn, table):
    print_header(f"EDIT RECORD — {table.upper()}")
    columns = get_columns(conn, table)
    pk_col = next((col[1] for col in columns if col[5] == 1), columns[0][1])
    pk_val = input(f"  Enter {pk_col} to edit: ").strip()
    row = get_row_by_id(conn, table, pk_col, pk_val)
    if not row:
        print(f"\n  No record found with {pk_col} = {pk_val}")
        input("  Press Enter to continue...")
        return
    print("\n  Current values (press Enter to keep):")
    editable = [col for col in columns if col[1] != pk_col]
    new_values = []
    col_names = []
    for col in editable:
        col_name = col[1]
        current = row[col_name]
        val = input(f"  {col_name} [{current}]: ").strip()
        col_names.append(col_name)
        new_values.append(val if val else current)
    try:
        update_row(conn, table, col_names, new_values, pk_col, pk_val)
        print("\n  Record updated successfully!")
    except Exception as e:
        print(f"\n  Error: {e}")
    input("  Press Enter to continue...")


def delete_record(conn, table):
    print_header(f"DELETE RECORD — {table.upper()}")
    columns = get_columns(conn, table)
    pk_col = next((col[1] for col in columns if col[5] == 1), columns[0][1])
    pk_val = input(f"  Enter {pk_col} to delete: ").strip()
    row = get_row_by_id(conn, table, pk_col, pk_val)
    if not row:
        print(f"\n  No record found with {pk_col} = {pk_val}")
        input("  Press Enter to continue...")
        return
    print(f"\n  About to delete: {dict(row)}")
    confirm = input("  Confirm delete? (yes/no): ").strip().lower()
    if confirm == "yes":
        try:
            delete_row(conn, table, pk_col, pk_val)
            print("\n  Record deleted successfully!")
        except Exception as e:
            print(f"\n  Error: {e}")
    else:
        print("\n  Delete cancelled.")
    input("  Press Enter to continue...")


def search_records(conn, table):
    print_header(f"SEARCH — {table.upper()}")
    columns = get_columns(conn, table)
    col_names = [col[1] for col in columns]
    print("  Columns: " + ", ".join(col_names))
    col = input("  Search in column: ").strip()
    if col not in col_names:
        print("  Column not found.")
        input("  Press Enter to continue...")
        return
    term = input("  Search term: ").strip()
    cursor = conn.execute(f"SELECT * FROM {table} WHERE {col} LIKE ?", (f"%{term}%",))
    rows = cursor.fetchall()
    print_table(rows, columns)
    input("\n  Press Enter to continue...")


def export_to_csv(conn, table):
    print_header(f"EXPORT — {table.upper()}")
    columns = get_columns(conn, table)
    rows = get_all_rows(conn, table)
    filename = f"{table}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    col_names = [col[1] for col in columns]
    with open(filename, "w") as f:
        f.write(",".join(col_names) + "\n")
        for row in rows:
            f.write(",".join(str(v) if v is not None else "" for v in row) + "\n")
    print(f"\n  Exported {len(rows)} records to {filename}")
    input("  Press Enter to continue...")


# ── TABLE MENU ──────────────────────────────────────────────────────────
def table_menu(conn, table):
    while True:
        clear()
        print_header(f"ADMIN PANEL — {table.upper()}")
        columns = get_columns(conn, table)
        rows = get_all_rows(conn, table)
        print(f"\n  Table: {table}")
        print(f"  Columns: {', '.join(col[1] for col in columns)}")
        print(f"  Records: {len(rows)}")
        print("\n  [1] View all records")
        print("  [2] Add record")
        print("  [3] Edit record")
        print("  [4] Delete record")
        print("  [5] Search records")
        print("  [6] Export to CSV")
        print("  [0] Back to table list")
        choice = input("\n  Choose: ").strip()
        if choice == "1":
            view_records(conn, table)
        elif choice == "2":
            add_record(conn, table)
        elif choice == "3":
            edit_record(conn, table)
        elif choice == "4":
            delete_record(conn, table)
        elif choice == "5":
            search_records(conn, table)
        elif choice == "6":
            export_to_csv(conn, table)
        elif choice == "0":
            break


# ── MAIN MENU ───────────────────────────────────────────────────────────
def main():
    conn = get_connection()
    # Seed demo data if DB is empty
    tables = get_tables(conn)
    if not tables:
        print("  No tables found. Creating demo database...")
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                category TEXT
            );
            INSERT INTO users (name, email, role) VALUES
                ('Alice Smith', 'alice@example.com', 'admin'),
                ('Bob Jones', 'bob@example.com', 'user'),
                ('Carol White', 'carol@example.com', 'user');
            INSERT INTO products (name, price, stock, category) VALUES
                ('Laptop', 999.99, 10, 'Electronics'),
                ('Mouse', 29.99, 50, 'Electronics'),
                ('Desk', 249.00, 5, 'Furniture');
        """)
        conn.commit()
        print("  Demo tables created: users, products\n")

    while True:
        clear()
        print_header("ADMIN PANEL GENERATOR — Python + SQL")
        tables = get_tables(conn)
        print("\n  Available tables:\n")
        for i, table in enumerate(tables, 1):
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  [{i}] {table:<30} ({count} records)")
        print("\n  [0] Exit")
        choice = input("\n  Select table: ").strip()
        if choice == "0":
            print("\n  Goodbye!\n")
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tables):
                table_menu(conn, tables[idx])
        except ValueError:
            pass
    conn.close()


if __name__ == "__main__":
    main()
