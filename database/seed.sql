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

-- ============= SPRINT 2 SEED DATA =============

-- MAKEUP PRODUCTS (warm)
INSERT OR IGNORE INTO product_recommendations
  (category,sub_category,undertone,brand,product_name,shade_name,swatch_color,product_link)
VALUES
('makeup','foundation','warm','Maybelline','Fit Me Foundation','Golden Beige 220','#D4A574','https://www.maybelline.com'),
('makeup','blush','warm','NARS','Blush','Orgasm','#E8956D','https://www.narscosmetics.com'),
('makeup','lipstick','warm','NYX','Butter Lipstick','Praline','#B5714A','https://www.nyxcosmetics.com'),
('makeup','eyeshadow','warm','Urban Decay','Naked Palette','Warm Neutrals','#C49A6C','https://www.urbandecay.com'),
('makeup','foundation','warm','L''Oreal','True Match Foundation','W3 Golden Beige','#C8956C','https://www.loreal.com'),
('makeup','lipstick','warm','MAC','Lipstick','Velvet Teddy','#C4956A','https://www.maccosmetics.com'),
-- CLOTHING (warm)
('clothing',NULL,'warm',NULL,'Mustard Wrap Dress',NULL,'#D4A017','https://www.uniqlo.com'),
('clothing',NULL,'warm',NULL,'Rust Blazer',NULL,'#B7410E','https://www.hm.com'),
('clothing',NULL,'warm',NULL,'Olive Wide-Leg Trousers',NULL,'#6B7C41','https://www.zara.com'),
('clothing',NULL,'warm',NULL,'Camel Trench Coat',NULL,'#C19A6B','https://www.mango.com'),
-- MAKEUP (cool)
('makeup','foundation','cool','Fenty Beauty','Pro Filt''r Foundation','150N Cool','#F0D5C8','https://www.fentybeauty.com'),
('makeup','blush','cool','e.l.f.','Blush','Pinktastic','#E8A0B4','https://www.elfcosmetics.com'),
('makeup','lipstick','cool','MAC','Lipstick','Brave','#C0748A','https://www.maccosmetics.com'),
('makeup','eyeshadow','cool','Morphe','35B Palette','Cool Tones','#9DB8D2','https://www.morphe.com'),
('makeup','foundation','cool','L''Oreal','True Match Foundation','C1 Rose Ivory','#F5E0D8','https://www.loreal.com'),
('makeup','blush','cool','Milani','Baked Blush','Berry Amore','#C87090','https://www.milanicosmetics.com'),
-- CLOTHING (cool)
('clothing',NULL,'cool',NULL,'Dusty Rose Midi Dress',NULL,'#DCAE96','https://www.hm.com'),
('clothing',NULL,'cool',NULL,'Lavender Blazer',NULL,'#B57EDC','https://www.zara.com'),
('clothing',NULL,'cool',NULL,'Navy Wide-Leg Pants',NULL,'#1C2951','https://www.uniqlo.com'),
('clothing',NULL,'cool',NULL,'Powder Blue Shirt',NULL,'#B0C4DE','https://www.mango.com'),
-- MAKEUP (neutral)
('makeup','foundation','neutral','Fenty Beauty','Pro Filt''r Foundation','235N','#C8956C','https://www.fentybeauty.com'),
('makeup','lipstick','neutral','MAC','Lipstick','Velvet Teddy','#C4956A','https://www.maccosmetics.com'),
('makeup','blush','neutral','NARS','Blush','Luster','#E8956D','https://www.narscosmetics.com'),
('makeup','eyeshadow','neutral','Urban Decay','Basics Palette','Neutrals','#C49A6C','https://www.urbandecay.com'),
('makeup','foundation','neutral','Maybelline','Fit Me Foundation','220 Natural Beige','#D4A574','https://www.maybelline.com'),
('makeup','lipstick','neutral','NYX','Butter Lipstick','Creme Brulee','#D4956A','https://www.nyxcosmetics.com'),
-- CLOTHING (neutral)
('clothing',NULL,'neutral',NULL,'Sage Green Co-ord Set',NULL,'#8CA67B','https://www.zara.com'),
('clothing',NULL,'neutral',NULL,'Dusty Mauve Blazer',NULL,'#C0909A','https://www.hm.com'),
('clothing',NULL,'neutral',NULL,'Teal Midi Skirt',NULL,'#008080','https://www.uniqlo.com'),
('clothing',NULL,'neutral',NULL,'Warm White Linen Shirt',NULL,'#FAF0E6','https://www.mango.com');

-- STYLE SUGGESTIONS
INSERT OR IGNORE INTO style_suggestions (face_shape,category,suggestion_name,description) VALUES
-- OVAL
('oval','hairstyle','Beachy Waves','Loose waves enhance your balanced proportions beautifully.'),
('oval','hairstyle','Sleek Straight','Straight hair showcases your even face shape.'),
('oval','hairstyle','High Ponytail','Pulls hair up to highlight your well-proportioned face.'),
('oval','hijab','Classic Wrap','Simple wrap that frames your face evenly.'),
('oval','hijab','Pinned Side Style','One-sided pin complements your natural symmetry.'),
('oval','hijab','Layered Front Style','Soft layers at front add dimension.'),
('oval','earring','Hoop Earrings','Any size hoop works beautifully with oval faces.'),
('oval','earring','Drop Earrings','Elongated drops enhance your natural balance.'),
('oval','earring','Stud Earrings','Simple studs highlight your symmetrical features.'),
-- ROUND
('round','hairstyle','Long Layers','Layers add length and visually slim the face.'),
('round','hairstyle','Side Part','Creates asymmetry to elongate a round face.'),
('round','hairstyle','High Bun','Adds height to balance round proportions.'),
('round','hijab','Layered Volume Top','Extra volume on top adds height and elongates.'),
('round','hijab','V-Shape Front','Creates a slimming V at the forehead.'),
('round','hijab','Draped Side Style','Side draping creates a lengthening diagonal line.'),
('round','earring','Long Drop Earrings','Elongate the face to balance round features.'),
('round','earring','Angular Earrings','Square shapes add definition to soft features.'),
('round','earring','Chandelier Earrings','Draw the eye downward to elongate the face.'),
-- SQUARE
('square','hairstyle','Soft Curls','Curls soften the angular jawline beautifully.'),
('square','hairstyle','Side-Swept Fringe','Diagonal fringe softens forehead corners.'),
('square','hairstyle','Layered Bob','Layers around jaw level soften square edges.'),
('square','hijab','Soft Gathered Style','Loose gathering creates soft curves against a square jaw.'),
('square','hijab','Round-Front Drape','Soft rounded draping against angular features.'),
('square','hijab','Loose Wrap','Relaxed voluminous wrap softens strong angles.'),
('square','earring','Round Hoops','Circles soften square facial angles.'),
('square','earring','Oval Drop Earrings','Oval shapes balance strong jawlines.'),
('square','earring','Pearl Drops','Soft rounded pearls complement angular shapes.'),
-- HEART
('heart','hairstyle','Chin-Length Bob','Adds width at jaw to balance a wider forehead.'),
('heart','hairstyle','Side Part Waves','Soft waves add fullness around the chin area.'),
('heart','hairstyle','Low Bun','Keeps volume low to balance a wider forehead.'),
('heart','hijab','Volume-at-Chin Style','Extra fabric at chin balances the forehead.'),
('heart','hijab','Wide Wrap','Wider fabric frames the lower face.'),
('heart','hijab','Side-Pinned Style','Pin to side to draw attention from forehead width.'),
('heart','earring','Teardrop Earrings','Wider at bottom to balance a pointed chin.'),
('heart','earring','Chandelier Earrings','Wide base adds fullness at jaw level.'),
('heart','earring','Drop Earrings','Adds width at jaw to complement heart shapes.'),
-- OBLONG
('oblong','hairstyle','Blunt Bob','Adds width to shorten an elongated face.'),
('oblong','hairstyle','Curtain Bangs','Fringe reduces apparent face length.'),
('oblong','hairstyle','Voluminous Waves','Width on sides balances a long face.'),
('oblong','hijab','Side Volume Style','Fabric on sides adds width.'),
('oblong','hijab','Turban Style','Adds width at forehead to shorten long face.'),
('oblong','hijab','Flat Top Style','Keeps height minimal while adding width.'),
('oblong','earring','Stud Earrings','Simple studs do not add more length.'),
('oblong','earring','Wide Hoop Earrings','Horizontal width balances facial length.'),
('oblong','earring','Cluster Earrings','Wide shapes add horizontal interest.');
