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
-- ============= SPRINT 2 =============

CREATE TABLE IF NOT EXISTS photo_analysis (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    skin_tone   TEXT,
    undertone   TEXT,
    face_shape  TEXT,
    photo_saved INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS product_recommendations (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    category     TEXT NOT NULL,
    sub_category TEXT,
    undertone    TEXT NOT NULL,
    brand        TEXT,
    product_name TEXT NOT NULL,
    shade_name   TEXT,
    swatch_color TEXT,
    product_link TEXT
);

CREATE TABLE IF NOT EXISTS wishlist (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    saved_at   TEXT DEFAULT (datetime('now')),
    UNIQUE(user_id, product_id),
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES product_recommendations(id)
);

CREATE TABLE IF NOT EXISTS style_suggestions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    face_shape      TEXT NOT NULL,
    category        TEXT NOT NULL,
    suggestion_name TEXT NOT NULL,
    description     TEXT
);

CREATE TABLE IF NOT EXISTS style_bookmarks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL,
    suggestion_id INTEGER NOT NULL,
    UNIQUE(user_id, suggestion_id),
    FOREIGN KEY (user_id)       REFERENCES users(id),
    FOREIGN KEY (suggestion_id) REFERENCES style_suggestions(id)
);