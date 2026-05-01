-- GlamMatch Sample Data
-- Sprint 1, 2 & 3 — SQLite seed file

-- ============================================================
-- SPRINT 1 SEED DATA
-- ============================================================

-- Sample users (passwords are SHA256 of 'test1234')
INSERT OR IGNORE INTO users (name, email, password, undertone, body_type, face_shape) VALUES
('Anoushay Fatima', 'anoushay@test.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'warm',    'hourglass', 'oval'),
('Eman Adil',       'eman@test.com',     '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'cool',    'pear',      'round'),
('Ayza Ahmed',      'ayza@test.com',     '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'neutral', 'rectangle', 'heart');

-- Sample wardrobe items
INSERT OR IGNORE INTO wardrobe (user_id, filename, category, style_tag, color) VALUES
(1, 'top1.jpg',    'Top',    'Casual',   'terracotta'),
(1, 'skirt1.jpg',  'Skirt',  'Formal',   'camel'),
(2, 'blouse1.jpg', 'Blouse', 'Party',    'sapphire'),
(3, 'jeans1.jpg',  'Jeans',  'Casual',   'navy');

-- Sample bookmarks
INSERT OR IGNORE INTO bookmarks (user_id, tip_id) VALUES
(1, 'w1'),
(1, 'w3'),
(2, 'c2');

-- ============================================================
-- SPRINT 2 SEED DATA
-- ============================================================

-- MAKEUP PRODUCTS — warm
INSERT OR IGNORE INTO product_recommendations
  (category, sub_category, undertone, brand, product_name, shade_name, swatch_color, product_link)
VALUES
('makeup', 'foundation', 'warm', 'L''Oreal',         'True Match Foundation',   'W3 Golden Beige',      '#C8906A', 'https://www.loreal-paris.com'),
('makeup', 'blush',      'warm', 'NARS',             'Blush',                   'Orgasm — Warm Peach',  '#E8956A', 'https://www.narscosmetics.com'),
('makeup', 'lipstick',   'warm', 'MAC',              'Matte Lipstick',          'Mull It Over',         '#B7604A', 'https://www.maccosmetics.com'),
('makeup', 'lipstick',   'warm', 'Charlotte Tilbury','Matte Revolution',        'So It Glows — Coral',  '#CC6040', 'https://www.charlottetilbury.com'),
('makeup', 'highlight',  'warm', 'Fenty Beauty',     'Killawatt Highlighter',   'Trophy Wife — Gold',   '#D4A030', 'https://www.fentybeauty.com'),
('makeup', 'eyeshadow',  'warm', 'Urban Decay',      'Naked Heat Palette',      'Warm Amber Tones',     '#C08040', 'https://www.urbandecay.com');

-- CLOTHING — warm
INSERT OR IGNORE INTO product_recommendations
  (category, sub_category, undertone, brand, product_name, shade_name, swatch_color, product_link)
VALUES
('clothing', 'top',       'warm', 'Zara',   'Linen Blend Top',     'Terracotta', '#C45C3A', 'https://www.zara.com'),
('clothing', 'dress',     'warm', 'H&M',    'Wrap Midi Dress',     'Camel',      '#C19A6B', 'https://www.hm.com'),
('clothing', 'outerwear', 'warm', 'Mango',  'Tailored Blazer',     'Warm Brown', '#8B5030', 'https://www.mango.com'),
('clothing', 'bottom',    'warm', 'Uniqlo', 'Wide Leg Trousers',   'Mustard',    '#E1AD01', 'https://www.uniqlo.com');

-- MAKEUP PRODUCTS — cool
INSERT OR IGNORE INTO product_recommendations
  (category, sub_category, undertone, brand, product_name, shade_name, swatch_color, product_link)
VALUES
('makeup', 'foundation', 'cool', 'Maybelline',       'Fit Me Foundation',       'C30 Cool Porcelain',   '#F0D0C0', 'https://www.maybelline.com'),
('makeup', 'blush',      'cool', 'NARS',             'Blush',                   'Dolce Vita — Mauve',   '#C8788A', 'https://www.narscosmetics.com'),
('makeup', 'lipstick',   'cool', 'MAC',              'Lipstick',                'Rebel — Berry',        '#8E2D56', 'https://www.maccosmetics.com'),
('makeup', 'lipstick',   'cool', 'Charlotte Tilbury','Hot Lips',                'Walk of No Shame',     '#C01840', 'https://www.charlottetilbury.com'),
('makeup', 'highlight',  'cool', 'Fenty Beauty',     'Diamond Bomb',            'How Many Carats',      '#E0E0E8', 'https://www.fentybeauty.com'),
('makeup', 'eyeshadow',  'cool', 'Urban Decay',      'Naked Palette',           'Cool Blues & Purples', '#6060B0', 'https://www.urbandecay.com');

-- CLOTHING — cool
INSERT OR IGNORE INTO product_recommendations
  (category, sub_category, undertone, brand, product_name, shade_name, swatch_color, product_link)
VALUES
('clothing', 'top',       'cool', 'Zara',   'Satin Blouse',        'Sapphire Blue',  '#0F52BA', 'https://www.zara.com'),
('clothing', 'dress',     'cool', 'H&M',    'Midi Dress',          'Lavender',       '#967BB6', 'https://www.hm.com'),
('clothing', 'outerwear', 'cool', 'Mango',  'Blazer',              'Emerald Green',  '#50C878', 'https://www.mango.com'),
('clothing', 'bottom',    'cool', 'Uniqlo', 'Slim Trousers',       'Slate Grey',     '#708090', 'https://www.uniqlo.com');

-- MAKEUP PRODUCTS — neutral
INSERT OR IGNORE INTO product_recommendations
  (category, sub_category, undertone, brand, product_name, shade_name, swatch_color, product_link)
VALUES
('makeup', 'foundation', 'neutral', 'Fenty Beauty',     'Pro Filt''r Foundation', '240N Neutral',      '#C8906A', 'https://www.fentybeauty.com'),
('makeup', 'blush',      'neutral', 'NARS',             'Blush',                  'Desire — Dusty Rose','#DCAE96', 'https://www.narscosmetics.com'),
('makeup', 'lipstick',   'neutral', 'Charlotte Tilbury','Pillow Talk',            'Original — Nude Pink','#C8847A', 'https://www.charlottetilbury.com'),
('makeup', 'lipstick',   'neutral', 'MAC',              'Lipstick',               'Twig — Mauve',      '#C0909A', 'https://www.maccosmetics.com'),
('makeup', 'highlight',  'neutral', 'Fenty Beauty',     'Killawatt Highlighter',  'Rose Gold',         '#B76E79', 'https://www.fentybeauty.com'),
('makeup', 'eyeshadow',  'neutral', 'Urban Decay',      'Naked3 Palette',         'Rosy Neutral Tones','#C09090', 'https://www.urbandecay.com');

-- CLOTHING — neutral
INSERT OR IGNORE INTO product_recommendations
  (category, sub_category, undertone, brand, product_name, shade_name, swatch_color, product_link)
VALUES
('clothing', 'top',       'neutral', 'Zara',   'Relaxed Blouse',     'Dusty Rose',  '#DCAE96', 'https://www.zara.com'),
('clothing', 'dress',     'neutral', 'H&M',    'Wrap Dress',         'Sage Green',  '#8CA67B', 'https://www.hm.com'),
('clothing', 'outerwear', 'neutral', 'Mango',  'Trench Coat',        'Taupe',       '#BDB09F', 'https://www.mango.com'),
('clothing', 'bottom',    'neutral', 'Uniqlo', 'Wide Leg Pants',     'Mauve',       '#C0909A', 'https://www.uniqlo.com');

-- STYLE SUGGESTIONS
INSERT OR IGNORE INTO style_suggestions (face_shape, category, suggestion_name, description) VALUES
-- OVAL
('oval', 'hairstyle', 'Any Length Works',      'Oval faces suit virtually all hairstyles — long, short, curly, or straight.'),
('oval', 'hairstyle', 'Side-Swept Bangs',      'Asymmetric side bangs add drama and complement your balanced proportions.'),
('oval', 'hairstyle', 'Voluminous Waves',      'Loose waves add romance and highlight your naturally symmetrical features.'),
('oval', 'hijab',     'Wrap Style Hijab',      'A simple wrap or Turkish style flatters your oval shape perfectly.'),
('oval', 'hijab',     'Draped Shawl',          'A draped shawl with soft folds adds sophistication.'),
('oval', 'hijab',     'Turban Style',          'A neat turban draws attention to your symmetrical face.'),
('oval', 'earring',   'Statement Drops',       'Long drop earrings or chandeliers look stunning on oval faces.'),
('oval', 'earring',   'Hoops — Any Size',      'Small, medium, or oversized hoops all work on oval faces.'),
('oval', 'earring',   'Geometric Shapes',      'Angular geometric earrings add modern edge.'),
-- ROUND
('round', 'hairstyle', 'Long Layers',          'Long layered hair creates length and slims a round face.'),
('round', 'hairstyle', 'High Top Knot',        'A high bun draws the eye upward, elongating your face shape.'),
('round', 'hairstyle', 'Avoid Full Blunt Bobs','Blunt jaw-length cuts add width — opt for longer styles instead.'),
('round', 'hijab',    'Tall Volume on Top',    'Styles with height at the crown balance and elongate a round face.'),
('round', 'hijab',    'V-Shape Front',         'A V or point at the forehead adds length and slims the face.'),
('round', 'hijab',    'Avoid Wide Side Volume','Avoid styles that flare wide at the sides.'),
('round', 'earring',  'Long Drop Earrings',    'Elongated dangles draw the eye down and add visual length.'),
('round', 'earring',  'Angular Studs',         'Square or rectangular studs add sharp contrast.'),
('round', 'earring',  'Avoid Large Round Hoops','Round earrings echo the circular shape — opt for ovals instead.'),
-- SQUARE
('square', 'hairstyle', 'Soft Waves & Curls',  'Wavy or curly texture softens angular jawlines.'),
('square', 'hairstyle', 'Side Part with Length','A deep side part with hair past the chin balances a strong jaw.'),
('square', 'hairstyle', 'Avoid Blunt Cuts',    'Straight one-length cuts accentuate squareness — add layers.'),
('square', 'hijab',    'Rounded Draping',       'Softly draped styles with rounded edges contrast the angular jaw.'),
('square', 'hijab',    'Side Volume',           'More volume on one side creates pleasing asymmetry.'),
('square', 'hijab',    'Avoid Tight Angular Wraps','Sharp geometric wraps repeat the angular lines.'),
('square', 'earring',  'Oval & Teardrop',       'Curved oval or teardrop shapes soften a square jaw.'),
('square', 'earring',  'Hoop Earrings',         'Medium circular hoops add curves to balance strong jawlines.'),
('square', 'earring',  'Avoid Sharp Rectangles','Rectangular bar earrings repeat the angular jaw — choose rounds.'),
-- HEART
('heart', 'hairstyle', 'Chin-Length Bob',      'A bob at jaw level adds width at the chin, balancing a wider forehead.'),
('heart', 'hairstyle', 'Side-Swept Fringe',    'Side bangs minimize a wider forehead.'),
('heart', 'hairstyle', 'Avoid High Volume Top','Extra volume at the crown emphasizes the widest part.'),
('heart', 'hijab',     'Fuller at the Chin',   'Hijab styles with volume near the jaw balance a pointed chin.'),
('heart', 'hijab',     'Avoid Height at Crown','Styles that add height accentuate an already wider forehead.'),
('heart', 'hijab',     'Layered Draping at Jaw','Layering fabric near the jaw adds width where heart faces are narrower.'),
('heart', 'earring',   'Teardrop & Wide-Bottom','Earrings wider at the bottom draw attention to the jaw.'),
('heart', 'earring',   'Chandelier Earrings',  'Wide chandelier styles flare at the bottom to complement heart faces.'),
('heart', 'earring',   'Avoid Pointed-Top Studs','Sharp pointed studs emphasize the pointed chin.'),
-- OBLONG
('oblong', 'hairstyle', 'Soft Waves with Volume','Waves and curls add width to an oblong face.'),
('oblong', 'hairstyle', 'Blunt Fringe',         'A straight-across fringe reduces the vertical length.'),
('oblong', 'hairstyle', 'Avoid Sleek Length',   'Long sleek straight hair emphasizes length — add waves instead.'),
('oblong', 'hijab',    'Wide Side Volume',       'Styles with volume on the sides add width.'),
('oblong', 'hijab',    'Horizontal Draping',     'Horizontal layers across the forehead shorten an oblong face.'),
('oblong', 'hijab',    'Avoid Tall Crown Styles','Height at the top adds more length.'),
('oblong', 'earring',  'Stud or Button Earrings','Short studs don''t add length, keeping vertical line balanced.'),
('oblong', 'earring',  'Wide Hoops',             'Wide circular hoops add horizontal emphasis.'),
('oblong', 'earring',  'Avoid Long Dangles',     'Long earrings elongate an already-long face.');

-- ============================================================
-- SPRINT 3 SEED DATA
-- ============================================================

-- SALONS
INSERT OR IGNORE INTO salons (name, address, category, price_range, rating, review_count, working_hours, phone, description) VALUES
('Glamour Studio',    '12 Mall Road, Lahore',       'women',  'mid',     4.7, 38, '10:00 AM – 9:00 PM',  '+92-300-1234567', 'Premium beauty studio specializing in bridal and editorial makeup.'),
('The Beauty Lounge', '45 DHA Phase 5, Lahore',     'women',  'premium', 4.5, 22, '9:00 AM – 8:00 PM',   '+92-321-9876543', 'Relaxing lounge offering hair, skin, and nail treatments.'),
('Zara Salon',        '88 Johar Town, Lahore',      'unisex', 'budget',  4.2, 55, '8:30 AM – 9:30 PM',   '+92-333-5551234', 'Affordable salon for everyday cuts, color, and grooming.'),
('Bridal Affairs',    '3 Gulberg III, Lahore',      'women',  'premium', 4.9, 14, '10:00 AM – 7:00 PM',  '+92-311-7778888', 'Exclusive bridal studio with full event packages.'),
('SnipMaster',        '22 Model Town, Lahore',      'men',    'budget',  4.3, 41, '9:00 AM – 10:00 PM',  '+92-345-4440000', 'Classic barbershop with modern grooming services.'),
('Nails & Beyond',    '67 Bahria Town, Lahore',     'women',  'mid',     4.6, 29, '10:00 AM – 8:00 PM',  '+92-300-9990001', 'Nail art, gel extensions, and pedicure specialist.'),
('Style Hub',         '11 Faisal Town, Lahore',     'unisex', 'mid',     4.1, 63, '9:00 AM – 9:00 PM',   '+92-322-1231231', 'Full-service salon covering all hair and beauty needs.'),
('Elite Spa & Salon', '5 Cantt, Lahore',            'women',  'premium', 4.8, 18, '10:00 AM – 7:30 PM',  '+92-301-5556789', 'Luxury spa and salon experience with trained therapists.');

-- SALON SERVICES
INSERT OR IGNORE INTO salon_services (salon_id, service_name, service_type, price_min, price_max, duration_min) VALUES
-- Glamour Studio (id=1)
(1, 'Bridal Makeup',      'bridal',   8000,  15000, 180),
(1, 'Party Makeup',       'makeup',   3000,   6000,  90),
(1, 'Hair Styling',       'hair',     1500,   3000,  60),
(1, 'Facial',             'skincare', 1500,   3500,  60),
-- The Beauty Lounge (id=2)
(2, 'Hair Cut & Blow Dry','hair',     1200,   2500,  60),
(2, 'Hair Color',         'hair',     3000,   8000, 120),
(2, 'Manicure',           'nails',     800,   1500,  45),
(2, 'Pedicure',           'nails',     900,   1800,  45),
-- Zara Salon (id=3)
(3, 'Basic Haircut',      'hair',      500,    800,  30),
(3, 'Threading',          'skincare',  150,    250,  15),
(3, 'Waxing (Full)',      'skincare',  800,   1200,  60),
(3, 'Simple Makeup',      'makeup',   1500,   2500,  60),
-- Bridal Affairs (id=4)
(4, 'Full Bridal Package','bridal',  20000,  50000, 360),
(4, 'Mehndi Makeup',      'bridal',   5000,  10000, 120),
(4, 'Trial Makeup',       'makeup',   3000,   5000,  90),
(4, 'Hair Treatment',     'hair',     2000,   5000,  90),
-- SnipMaster (id=5)
(5, 'Haircut',            'hair',      400,    700,  30),
(5, 'Shave',              'hair',      300,    500,  20),
(5, 'Beard Trim',         'hair',      250,    400,  15),
(5, 'Hair Color',         'hair',     1500,   3000,  60),
-- Nails & Beyond (id=6)
(6, 'Gel Nails',          'nails',    1500,   2500,  60),
(6, 'Nail Art',           'nails',     500,   1500,  45),
(6, 'Pedicure Deluxe',    'nails',    1200,   2000,  60),
(6, 'Acrylic Extensions', 'nails',    2000,   3500,  90),
-- Style Hub (id=7)
(7, 'Haircut (Women)',    'hair',      800,   1500,  45),
(7, 'Haircut (Men)',      'hair',      400,    700,  30),
(7, 'Highlights',         'hair',     3000,   7000, 120),
(7, 'Facial Basic',       'skincare', 1000,   2000,  60),
-- Elite Spa & Salon (id=8)
(8, 'Luxury Facial',      'skincare', 3500,   6000,  90),
(8, 'Body Massage',       'skincare', 4000,   7000,  90),
(8, 'Hair Spa',           'hair',     2000,   4000,  60),
(8, 'Full Glam Makeup',   'makeup',   5000,   9000, 120);

-- SAMPLE BOOKINGS (for testing status flow)
INSERT OR IGNORE INTO bookings (user_id, salon_id, service_id, datetime, status, note) VALUES
(1, 1, 1, '2024-05-15T14:00', 'confirmed',  'Please use halal cosmetics'),
(2, 2, 5, '2024-05-18T11:00', 'pending',    'First time visit'),
(3, 4, 13,'2024-05-20T10:00', 'completed',  'Bridal shoot prep');

-- SAMPLE REVIEWS (only on completed bookings)
INSERT OR IGNORE INTO reviews (user_id, salon_id, booking_id, rating, review_text) VALUES
(3, 4, 3, 5, 'Absolutely stunning work! The bridal package was worth every rupee. Highly recommended.');

-- Update Bridal Affairs rating to reflect the seeded review
UPDATE salons SET rating = 5.0, review_count = 1 WHERE id = 4;