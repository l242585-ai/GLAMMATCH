-- GlamMatch Sample Data
-- Sprint 1 — SQLite seed file

-- Sample users (passwords are SHA256 of 'test1234')
INSERT OR IGNORE INTO users (name, email, password, undertone, body_type) VALUES
('Anoushay Fatima', 'anoushay@test.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'warm', 'hourglass'),
('Eman Adil',       'eman@test.com',     '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'cool',  'pear'),
('Ayza Ahmed',      'ayza@test.com',     '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'neutral','rectangle');

-- Sample wardrobe items
INSERT OR IGNORE INTO wardrobe (user_id, filename, category, style_tag) VALUES
(1, 'top1.jpg',    'Top',    'Casual'),
(1, 'skirt1.jpg',  'Skirt',  'Formal'),
(2, 'blouse1.jpg', 'Blouse', 'Party'),
(3, 'jeans1.jpg',  'Jeans',  'Casual');

-- Sample bookmarks
INSERT OR IGNORE INTO bookmarks (user_id, tip_id) VALUES
(1, 'w1'),
(1, 'w3'),
(2, 'c2');
