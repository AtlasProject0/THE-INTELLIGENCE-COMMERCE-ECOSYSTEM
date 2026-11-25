import sqlite3

from atlas.core import atlas


def test_initialize_creates_tasks_table(tmp_path, monkeypatch):
    db_path = tmp_path / "atlas_test.db"
    monkeypatch.setattr(atlas, "DB_PATH", db_path)

    atlas.initialize()

    with sqlite3.connect(db_path) as db:
        tables = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()

    assert ("tasks",) in tables


def test_create_task_saves_task(tmp_path, monkeypatch):
    db_path = tmp_path / "atlas_test.db"
    monkeypatch.setattr(atlas, "DB_PATH", db_path)

    atlas.initialize()

    answers = iter(["Test gorevi", "Test aciklamasi"])
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(answers)
    )

    atlas.create_task()

    with sqlite3.connect(db_path) as db:
        task = db.execute(
            "SELECT title, description, assigned_agent, status "
            "FROM tasks"
        ).fetchone()

    assert task == (
        "Test gorevi",
        "Test aciklamasi",
        "unassigned",
        "pending",
    )
