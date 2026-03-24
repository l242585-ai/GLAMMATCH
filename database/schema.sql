-- GlamMatch Database Schema
-- Sprint 1 — SQLite

CREATE TABLE IF NOT EXISTS users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL,
    email     TEXT    UNIQUE NOT NULL,
    password  TEXT    NOT NULL,
    undertone TEXT,
    body_type TEXT,
    created   TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS wardrobe (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    filename  TEXT    NOT NULL,
    category  TEXT,
    style_tag TEXT,
    added     TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS quiz_log (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL,
    type     TEXT    NOT NULL,
    answers  TEXT    NOT NULL,
    result   TEXT    NOT NULL,
    taken    TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS bookmarks (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tip_id  TEXT    NOT NULL,
    UNIQUE(user_id, tip_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
