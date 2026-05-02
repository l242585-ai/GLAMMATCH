-- GlamMatch Database Schema
-- Updated for current Flask app and parlour portal workflow
-- SQLite

PRAGMA foreign_keys = ON;

-- ============================================================
-- USER / AUTH TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    password   TEXT NOT NULL,
    undertone  TEXT,
    body_type  TEXT,
    face_shape TEXT,
    created    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    token   TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    expires TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================================
-- QUIZ / STYLE ANALYSIS TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS quiz_log (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type    TEXT NOT NULL,
    answers TEXT NOT NULL,
    result  TEXT NOT NULL,
    taken   TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS bookmarks (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tip_id  TEXT NOT NULL,
    UNIQUE(user_id, tip_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

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
-- WARDROBE / PRODUCT TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS wardrobe (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    filename  TEXT NOT NULL,
    category  TEXT,
    style_tag TEXT,
    color     TEXT,
    added     TEXT DEFAULT (datetime('now')),
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

-- ============================================================
-- PARLOUR PORTAL TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS parlours (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER,
    name          TEXT NOT NULL,
    owner         TEXT NOT NULL,
    phone         TEXT NOT NULL,
    email         TEXT,
    address       TEXT NOT NULL,
    city          TEXT NOT NULL,
    area          TEXT,
    services      TEXT,                      -- JSON array of service names
    open_time     TEXT DEFAULT '09:00',       -- 24-hour HH:MM
    close_time    TEXT DEFAULT '21:00',       -- 24-hour HH:MM
    days          TEXT DEFAULT 'Mon – Sat',   -- e.g. Mon – Sat, Daily, or comma-separated days
    cnic          TEXT,
    cnic_front_file TEXT,                     -- base64/data URL for prototype document storage
    cnic_back_file  TEXT,                     -- base64/data URL for prototype document storage
    cnic_verification_note TEXT,
    business_type TEXT,
    price_min     INTEGER DEFAULT 0,
    price_max     INTEGER DEFAULT 0,
    description   TEXT,
    rating        REAL DEFAULT 0.0,
    review_count  INTEGER DEFAULT 0,
    status        TEXT DEFAULT 'pending',     -- pending | approved | rejected
    created_at    TEXT DEFAULT (datetime('now')),
    updated_at    TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS parlour_bookings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER,
    parlour_id    INTEGER NOT NULL,
    parlour_name  TEXT NOT NULL,
    service       TEXT NOT NULL,
    datetime      TEXT NOT NULL,              -- ISO local datetime from frontend
    client_name   TEXT NOT NULL,
    client_phone  TEXT NOT NULL,
    note          TEXT,
    status        TEXT DEFAULT 'pending',     -- pending | confirmed | rejected | cancelled | completed
    created_at    TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (parlour_id) REFERENCES parlours(id)
);

CREATE TABLE IF NOT EXISTS parlour_chat_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    booking_id  INTEGER,
    sender_type TEXT DEFAULT 'user',          -- client | parlour | user
    message     TEXT NOT NULL,
    reply       TEXT DEFAULT '',
    sent_at     TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (booking_id) REFERENCES parlour_bookings(id)
);

CREATE TABLE IF NOT EXISTS parlour_notifications (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    booking_id      INTEGER,
    kind            TEXT DEFAULT 'booking',   -- booking_cancelled | booking_rejected | etc.
    recipient_role  TEXT DEFAULT 'general',   -- client | owner | general
    title           TEXT NOT NULL,
    message         TEXT NOT NULL,
    is_read         INTEGER DEFAULT 0,
    created_at      TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (booking_id) REFERENCES parlour_bookings(id)
);

-- ============================================================
-- IMPORTANT BUSINESS RULES IMPLEMENTED IN BACKEND
-- ============================================================
-- 1. Only approved parlours appear in Find Parlours.
-- 2. Pending/rejected parlours cannot receive bookings.
-- 3. Bookings cannot be made in the past.
-- 4. Bookings cannot be made more than 90 days ahead.
-- 5. Bookings cannot be made on closed days or outside opening hours.
-- 6. Duplicate active bookings for the same parlour/date-time are blocked.
-- 7. Client cannot cancel within 2 hours of appointment time.
-- 8. Owner cannot reject within 2 hours of appointment time.
-- 9. Owner cannot manually complete a booking.
-- 10. Active bookings become completed automatically after appointment time passes.
-- 11. Chat closes after booking is cancelled, rejected, completed, or time passes.
