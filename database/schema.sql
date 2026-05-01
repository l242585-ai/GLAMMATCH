-- GlamMatch Database Schema
-- Sprint 1, 2 & 3 — SQLite

-- ============================================================
-- SPRINT 1 TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    email      TEXT    UNIQUE NOT NULL,
    password   TEXT    NOT NULL,
    undertone  TEXT,
    body_type  TEXT,
    face_shape TEXT,
    created    TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS wardrobe (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    filename  TEXT    NOT NULL,
    category  TEXT,
    style_tag TEXT,
    color     TEXT,
    added     TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS quiz_log (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type    TEXT    NOT NULL,
    answers TEXT    NOT NULL,
    result  TEXT    NOT NULL,
    taken   TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS bookmarks (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tip_id  TEXT    NOT NULL,
    UNIQUE(user_id, tip_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    token   TEXT    PRIMARY KEY,
    user_id INTEGER NOT NULL,
    expires TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================================
-- SPRINT 2 TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS photo_analysis (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    skin_tone   TEXT,
    undertone   TEXT,
    face_shape  TEXT,
    photo_saved INTEGER DEFAULT 0,
    created_at  TEXT    DEFAULT (datetime('now')),
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
    saved_at   TEXT    DEFAULT (datetime('now')),
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

-- ============================================================
-- SPRINT 3 TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS salons (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    address       TEXT,
    category      TEXT    DEFAULT 'women',
    price_range   TEXT    DEFAULT 'mid',
    rating        REAL    DEFAULT 0.0,
    review_count  INTEGER DEFAULT 0,
    working_hours TEXT    DEFAULT '9:00 AM - 8:00 PM',
    phone         TEXT,
    description   TEXT,
    latitude      REAL    DEFAULT 0.0,    -- GPS latitude for distance calculation
    longitude     REAL    DEFAULT 0.0,    -- GPS longitude for distance calculation
    created_at    TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS salon_services (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    salon_id     INTEGER NOT NULL,
    service_name TEXT    NOT NULL,
    service_type TEXT,                    -- 'makeup' | 'hair' | 'nails' | 'skincare' | 'bridal'
    price_min    INTEGER DEFAULT 0,
    price_max    INTEGER DEFAULT 0,
    duration_min INTEGER DEFAULT 60,
    FOREIGN KEY (salon_id) REFERENCES salons(id)
);

CREATE TABLE IF NOT EXISTS bookings (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    salon_id   INTEGER NOT NULL,
    service_id INTEGER,
    datetime   TEXT    NOT NULL,
    status     TEXT    DEFAULT 'pending', -- 'pending'|'confirmed'|'rejected'|'alternate'|'completed'|'cancelled'
    note       TEXT,
    alt_time   TEXT,                      -- alternate time proposed by salon
    created_at TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (salon_id)   REFERENCES salons(id),
    FOREIGN KEY (service_id) REFERENCES salon_services(id)
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id  INTEGER NOT NULL,
    sender_type TEXT    NOT NULL,         -- 'user' | 'salon'
    message     TEXT    NOT NULL,
    sent_at     TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    salon_id    INTEGER NOT NULL,
    booking_id  INTEGER,
    rating      INTEGER NOT NULL,         -- 1 to 5
    review_text TEXT,
    created_at  TEXT    DEFAULT (datetime('now')),
    UNIQUE(user_id, booking_id),          -- one review per appointment
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (salon_id)   REFERENCES salons(id),
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- ============================================================
-- BOOKING STATUS FLOW
-- ============================================================
-- pending → confirmed → completed  (auto when datetime passes)
--         → rejected
--         → alternate → confirmed → completed
-- pending/confirmed → cancelled    (only if 2+ hours before appointment)
-- ============================================================