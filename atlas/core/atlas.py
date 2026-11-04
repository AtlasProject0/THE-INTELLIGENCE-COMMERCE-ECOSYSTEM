import sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "atlas" / "memory" / "atlas.db"


def initialize():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                assigned_agent TEXT DEFAULT 'unassigned',
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL
            )
        """)


def create_task():
    title = input("Gorev basligi: ").strip()

    if not title:
        print("Baslik bos olamaz.")
        return

    description = input("Gorev aciklamasi: ").strip()

    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT INTO tasks
            (title, description, created_at)
            VALUES (?, ?, ?)
            """,
            (title, description, datetime.now().isoformat())
        )

    print("Gorev kaydedildi.")


def list_tasks():
    with sqlite3.connect(DB_PATH) as db:
        tasks = db.execute(
            "SELECT id, title, assigned_agent, status FROM tasks"
        ).fetchall()

    if not tasks:
        print("Henuz gorev yok.")
        return

    for task in tasks:
        print(
            f"#{task[0]} | {task[1]} | "
            f"Ajan: {task[2]} | Durum: {task[3]}"
        )


def main():
    initialize()
    print("ATLAS CORE baslatildi.")

    while True:
        print("\n1 - Gorev olustur")
        print("2 - Gorevleri listele")
        print("0 - Cikis")

        choice = input("Secimin: ").strip()

        if choice == "1":
            create_task()
        elif choice == "2":
            list_tasks()
        elif choice == "0":
            print("ATLAS kapatildi.")
            break
        else:
            print("Gecersiz secim.")


if __name__ == "__main__":
    main()