"""
GlamMatch — Sprint 1 Backend
Flask REST API: Auth, Undertone/Body Quiz, Color Palette, Wardrobe, Styling Tips
"""
from flask import Flask, request, jsonify, send_from_directory
import sqlite3, hashlib, os, json, functools

try:
    import jwt, datetime
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

# ── Setup ────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
DB  = os.path.join(os.path.dirname(__file__), "glammatch.db")
SECRET = "glammatch_sprint1_secret"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "glammatch0@gmail.com"
SMTP_PASS = "sszdwpcrntfbmhhf"
FROM_EMAIL = "glammatch0@gmail.com"
try:
    from flask_cors import CORS
    CORS(app)
except ImportError:
    @app.after_request
    def add_cors(r):
        r.headers["Access-Control-Allow-Origin"]  = "*"
        r.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        r.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        return r

@app.route("/api/<path:p>", methods=["OPTIONS"])
def options(p): return "", 200

# ── DB ───────────────────────────────────────────────────────────
def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = db()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            email      TEXT UNIQUE NOT NULL,
            password   TEXT NOT NULL,
            undertone  TEXT,
            body_type  TEXT,
            face_shape TEXT,
            created    TEXT DEFAULT(datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS wardrobe(
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id   INTEGER NOT NULL,
            filename  TEXT NOT NULL,
            category  TEXT,
            style_tag TEXT,
            color     TEXT,
            added     TEXT DEFAULT(datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS quiz_log(
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type    TEXT NOT NULL,
            answers TEXT NOT NULL,
            result  TEXT NOT NULL,
            taken   TEXT DEFAULT(datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS bookmarks(
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tip_id  TEXT NOT NULL,
            UNIQUE(user_id,tip_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS photo_analysis(
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            skin_tone   TEXT,
            undertone   TEXT,
            face_shape  TEXT,
            photo_saved INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT(datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS product_recommendations(
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
        CREATE TABLE IF NOT EXISTS wishlist(
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            saved_at   TEXT DEFAULT(datetime('now')),
            UNIQUE(user_id,product_id),
            FOREIGN KEY(user_id)    REFERENCES users(id),
            FOREIGN KEY(product_id) REFERENCES product_recommendations(id)
        );
        CREATE TABLE IF NOT EXISTS style_suggestions(
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            face_shape      TEXT NOT NULL,
            category        TEXT NOT NULL,
            suggestion_name TEXT NOT NULL,
            description     TEXT
        );
        CREATE TABLE IF NOT EXISTS style_bookmarks(
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            suggestion_id INTEGER NOT NULL,
            UNIQUE(user_id,suggestion_id),
            FOREIGN KEY(user_id)       REFERENCES users(id),
            FOREIGN KEY(suggestion_id) REFERENCES style_suggestions(id)
        );
        CREATE TABLE IF NOT EXISTS password_reset_tokens(
            token      TEXT PRIMARY KEY,
            user_id    INTEGER NOT NULL,
            expires    TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );            
    """)
    c.commit()

    # ── Seed style_suggestions if empty ──────────────────────────
    if not c.execute("SELECT 1 FROM style_suggestions LIMIT 1").fetchone():
        suggestions = [
            # oval
            ("oval","hairstyle","Any Length Works","Oval faces suit virtually all hairstyles — long, short, curly, or straight."),
            ("oval","hairstyle","Side-Swept Bangs","Asymmetric side bangs add drama and complement your balanced proportions beautifully."),
            ("oval","hairstyle","Voluminous Waves","Loose waves add romance and highlight your naturally symmetrical features."),
            ("oval","hijab","Wrap Style Hijab","A simple wrap or Turkish style flatters your oval shape perfectly — minimal fuss, maximum elegance."),
            ("oval","hijab","Draped Shawl","A draped shawl with soft folds adds sophistication and works beautifully with your balanced features."),
            ("oval","hijab","Turban Style","A neat turban or pin-free wrap draws attention to your symmetrical face with chic simplicity."),
            ("oval","earring","Statement Drops","Long drop earrings or chandeliers look stunning — your balanced shape carries bold styles effortlessly."),
            ("oval","earring","Hoops — Any Size","Small, medium, or oversized hoops all work. Oval faces are the most versatile shape for earrings."),
            ("oval","earring","Geometric Shapes","Angular geometric earrings add modern edge and contrast beautifully with soft oval lines."),
            # round
            ("round","hairstyle","Long Layers","Long layered hair creates length and slims a round face — great for adding visual height."),
            ("round","hairstyle","High Top Knot","A high bun or top knot draws the eye upward, elongating your face shape beautifully."),
            ("round","hairstyle","Avoid Full Blunt Bobs","Blunt jaw-length cuts add width. Opt for longer styles or asymmetric cuts instead."),
            ("round","hijab","Tall Volume on Top","Styles with height at the crown — like a high-pinned turban — balance and elongate a round face."),
            ("round","hijab","V-Shape Front","Hijab styles that form a V or point at the forehead add length and slim the face visually."),
            ("round","hijab","Avoid Wide Side Volume","Avoid styles that flare wide at the sides — this adds width to an already full face shape."),
            ("round","earring","Long Drop Earrings","Elongated dangles draw the eye down and add visual length to round faces."),
            ("round","earring","Angular Studs","Square or rectangular studs add sharp contrast that slims and defines a rounder face."),
            ("round","earring","Avoid Large Round Hoops","Round earrings echo the face's circular shape — opt for ovals or geometric drops instead."),
            # square
            ("square","hairstyle","Soft Waves & Curls","Wavy or curly texture softens angular jawlines and adds feminine contrast to square faces."),
            ("square","hairstyle","Side Part with Length","A deep side part with hair past the chin balances a strong jaw with asymmetric softness."),
            ("square","hairstyle","Avoid Blunt Straight Cuts","Straight one-length cuts accentuate squareness — add layers or waves for a softening effect."),
            ("square","hijab","Rounded Draping","Softly draped hijab styles with rounded edges contrast with angular jaw and soften the overall look."),
            ("square","hijab","Side Volume","Styles with more volume on one side create pleasing asymmetry that flatters square shapes."),
            ("square","hijab","Avoid Tight Angular Wraps","Sharp geometric wraps repeat the angular lines of a square face — choose softer draping."),
            ("square","earring","Oval & Teardrop Earrings","Curved oval or teardrop shapes contrast the angles of a square jaw for a softening effect."),
            ("square","earring","Hoop Earrings","Medium circular hoops add curves that balance strong angular jawlines beautifully."),
            ("square","earring","Avoid Sharp Rectangle Earrings","Rectangular bar earrings repeat the angular jaw — choose rounds or soft drops instead."),
            # heart
            ("heart","hairstyle","Chin-Length Bob","A bob at jaw level adds width at the chin, balancing a wider forehead beautifully."),
            ("heart","hairstyle","Side-Swept Fringe","Side bangs minimize a wider forehead and draw attention to your cheekbones instead."),
            ("heart","hairstyle","Avoid High Volume on Top","Extra volume at the crown emphasizes the widest part — keep fullness lower on heart faces."),
            ("heart","hijab","Fuller at the Chin","Hijab styles with volume near the jaw balance a pointed chin with a wide forehead."),
            ("heart","hijab","Avoid Height at Crown","Styles that add height to the top of the head accentuate an already wider forehead."),
            ("heart","hijab","Layered Draping at Jaw","Layering fabric near the jaw adds width where heart-shaped faces are naturally narrower."),
            ("heart","earring","Teardrop & Wide-Bottom Earrings","Earrings wider at the bottom draw attention to the jaw, balancing a narrower chin."),
            ("heart","earring","Chandelier Earrings","Wide chandelier styles flare at the bottom to complement the natural taper of a heart face."),
            ("heart","earring","Avoid Pointed-Top Studs","Sharp pointed studs emphasize the pointed chin — opt for designs that widen at the bottom."),
            # oblong
            ("oblong","hairstyle","Soft Waves with Volume","Waves and curls add width to an oblong face, making it appear shorter and fuller."),
            ("oblong","hairstyle","Blunt Fringe","A straight-across fringe reduces the vertical length of an oblong face — very flattering."),
            ("oblong","hairstyle","Avoid Sleek Length","Long sleek straight hair emphasizes the length — add waves or volume for an oblong face."),
            ("oblong","hijab","Wide Side Volume","Styles with volume on the sides add width, balancing the length of an oblong face shape."),
            ("oblong","hijab","Horizontal Draping","Hijab wrapped with horizontal layers across the forehead shortens and balances an oblong face."),
            ("oblong","hijab","Avoid Tall Crown Styles","Height at the top adds more length — choose styles that widen rather than heighten."),
            ("oblong","earring","Stud or Button Earrings","Short studs and button earrings don't add length, keeping the face's vertical line balanced."),
            ("oblong","earring","Wide Hoops","Wide circular hoops add horizontal emphasis, making an oblong face appear shorter and rounder."),
            ("oblong","earring","Avoid Long Dangles","Long earrings elongate an already-long face — keep earrings short and wide instead."),
        ]
        c.executemany(
            "INSERT INTO style_suggestions(face_shape,category,suggestion_name,description) VALUES(?,?,?,?)",
            suggestions
        )
        c.commit()

    # ── Seed product_recommendations if empty ─────────────────────
    if not c.execute("SELECT 1 FROM product_recommendations LIMIT 1").fetchone():
        products = [
            # WARM makeup
            ("makeup","foundation","warm","L'Oreal","True Match Foundation","W3 Golden Beige","#C8906A","https://www.loreal-paris.com"),
            ("makeup","blush","warm","NARS","Blush","Orgasm — Warm Peach","#E8956A","https://www.narscosmetics.com"),
            ("makeup","lipstick","warm","MAC","Matte Lipstick","Mull It Over — Terracotta","#B7604A","https://www.maccosmetics.com"),
            ("makeup","lipstick","warm","Charlotte Tilbury","Matte Revolution","So It Glows — Coral","#CC6040","https://www.charlottetilbury.com"),
            ("makeup","highlight","warm","Fenty Beauty","Killawatt Highlighter","Trophy Wife — Gold","#D4A030","https://www.fentybeauty.com"),
            ("makeup","eyeshadow","warm","Urban Decay","Naked Heat Palette","Warm Amber Tones","#C08040","https://www.urbandecay.com"),
            # WARM clothing
            ("clothing","top","warm","Zara","Linen Blend Top","Terracotta","#C45C3A","https://www.zara.com"),
            ("clothing","dress","warm","H&M","Wrap Midi Dress","Camel","#C19A6B","https://www.hm.com"),
            ("clothing","outerwear","warm","Mango","Tailored Blazer","Warm Brown","#8B5030","https://www.mango.com"),
            ("clothing","bottom","warm","Uniqlo","Wide Leg Trousers","Mustard","#E1AD01","https://www.uniqlo.com"),
            # COOL makeup
            ("makeup","foundation","cool","Maybelline","Fit Me Foundation","C30 Cool Porcelain","#F0D0C0","https://www.maybelline.com"),
            ("makeup","blush","cool","NARS","Blush","Dolce Vita — Mauve Pink","#C8788A","https://www.narscosmetics.com"),
            ("makeup","lipstick","cool","MAC","Lipstick","Rebel — Berry","#8E2D56","https://www.maccosmetics.com"),
            ("makeup","lipstick","cool","Charlotte Tilbury","Hot Lips","Walk of No Shame — Cool Red","#C01840","https://www.charlottetilbury.com"),
            ("makeup","highlight","cool","Fenty Beauty","Diamond Bomb","How Many Carats — Silver","#E0E0E8","https://www.fentybeauty.com"),
            ("makeup","eyeshadow","cool","Urban Decay","Naked Palette","Cool Blues & Purples","#6060B0","https://www.urbandecay.com"),
            # COOL clothing
            ("clothing","top","cool","Zara","Satin Blouse","Sapphire Blue","#0F52BA","https://www.zara.com"),
            ("clothing","dress","cool","H&M","Midi Dress","Lavender","#967BB6","https://www.hm.com"),
            ("clothing","outerwear","cool","Mango","Blazer","Emerald Green","#50C878","https://www.mango.com"),
            ("clothing","bottom","cool","Uniqlo","Slim Trousers","Slate Grey","#708090","https://www.uniqlo.com"),
            # NEUTRAL makeup
            ("makeup","foundation","neutral","Fenty Beauty","Pro Filt'r Foundation","240N Neutral","#C8906A","https://www.fentybeauty.com"),
            ("makeup","blush","neutral","NARS","Blush","Desire — Dusty Rose","#DCAE96","https://www.narscosmetics.com"),
            ("makeup","lipstick","neutral","Charlotte Tilbury","Pillow Talk","Original — Nude Pink","#C8847A","https://www.charlottetilbury.com"),
            ("makeup","lipstick","neutral","MAC","Lipstick","Twig — Mauve","#C0909A","https://www.maccosmetics.com"),
            ("makeup","highlight","neutral","Fenty Beauty","Killawatt Highlighter","Rose Gold","#B76E79","https://www.fentybeauty.com"),
            ("makeup","eyeshadow","neutral","Urban Decay","Naked3 Palette","Rosy Neutral Tones","#C09090","https://www.urbandecay.com"),
            # NEUTRAL clothing
            ("clothing","top","neutral","Zara","Relaxed Blouse","Dusty Rose","#DCAE96","https://www.zara.com"),
            ("clothing","dress","neutral","H&M","Wrap Dress","Sage Green","#8CA67B","https://www.hm.com"),
            ("clothing","outerwear","neutral","Mango","Trench Coat","Taupe","#BDB09F","https://www.mango.com"),
            ("clothing","bottom","neutral","Uniqlo","Wide Leg Pants","Mauve","#C0909A","https://www.uniqlo.com"),
        ]
        c.executemany(
            "INSERT INTO product_recommendations(category,sub_category,undertone,brand,product_name,shade_name,swatch_color,product_link) VALUES(?,?,?,?,?,?,?,?)",
            products
        )
        c.commit()

    c.close()

# ── Auth helpers ─────────────────────────────────────────────────
def hp(pw): return hashlib.sha256(pw.encode()).hexdigest()

def make_token(uid):
    if JWT_AVAILABLE:
        return jwt.encode(
            {"user_id": uid, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
            SECRET, algorithm="HS256"
        )
    import base64
    return base64.b64encode(f"{uid}:{SECRET}".encode()).decode()

def decode_token(token):
    if JWT_AVAILABLE:
        try:
            return jwt.decode(token, SECRET, algorithms=["HS256"])["user_id"]
        except: return None
    import base64
    try:
        uid, _ = base64.b64decode(token).decode().split(":", 1)
        return int(uid)
    except: return None

def auth(f):
    @functools.wraps(f)
    def w(*a, **kw):
        t = request.headers.get("Authorization","").replace("Bearer ","")
        uid = decode_token(t)
        if not uid: return jsonify({"error":"Unauthorized"}), 401
        request.uid = uid
        return f(*a, **kw)
    return w

# ════════════════════════════════════════════════════════════════
#  DATA
# ════════════════════════════════════════════════════════════════

# ── Undertone quiz ───────────────────────────────────────────────
UT_QUESTIONS = [
    {"id":1,"q":"Look at the inner side of your wrist in natural light — what tone does your skin appear?",
     "opts":[{"id":"a","t":"Pinkish or reddish","score":{"cool":2}},
             {"id":"b","t":"Yellowish or golden","score":{"warm":2}},
             {"id":"c","t":"A mix of both pink and yellow","score":{"neutral":2}}]},
    {"id":2,"q":"When you hold a pure white fabric near your face, how does your face look?",
     "opts":[{"id":"a","t":"Fresh and bright — pure white suits me well","score":{"cool":2}},
             {"id":"b","t":"Off-white or cream looks better — pure white feels too harsh","score":{"warm":2}},
             {"id":"c","t":"Both look fine, I can't notice much difference","score":{"neutral":2}}]},
    {"id":3,"q":"Which jewellery makes your face look more glowing?",
     "opts":[{"id":"a","t":"Silver — my face looks brighter","score":{"cool":2}},
             {"id":"b","t":"Gold — my skin looks warm and vibrant","score":{"warm":2}},
             {"id":"c","t":"Both look equally good on me","score":{"neutral":2}}]},
    {"id":4,"q":"Which group of colours gets you the most compliments when you wear them?",
     "opts":[{"id":"a","t":"Royal blue, deep purple, hot pink, burgundy","score":{"cool":2}},
             {"id":"b","t":"Orange, terracotta, olive green, camel, mustard","score":{"warm":2}},
             {"id":"c","t":"Dusty rose, teal, mauve, soft grey","score":{"neutral":2}}]},
    {"id":5,"q":"After spending 2–3 hours in the sun, what usually happens to your skin?",
     "opts":[{"id":"a","t":"It turns red or I notice redness on my face","score":{"cool":2}},
             {"id":"b","t":"It looks a little golden or bronzed","score":{"warm":2}},
             {"id":"c","t":"Sometimes red, sometimes tan — it varies","score":{"neutral":2}}]},
    {"id":6,"q":"Which lipstick shades look most natural and flattering on you?",
     "opts":[{"id":"a","t":"Berry, mauve, cool pink or plum shades","score":{"cool":2}},
             {"id":"b","t":"Coral, peach, warm red or terracotta shades","score":{"warm":2}},
             {"id":"c","t":"Nude pink or rose gold — middle-ground shades","score":{"neutral":2}}]},
]

def classify_ut(answers):
    s = {"warm": 0, "cool": 0, "neutral": 0}
    for qid, oid in answers.items():
        q = next((x for x in UT_QUESTIONS if str(x["id"]) == str(qid)), None)
        if q:
            o = next((x for x in q["opts"] if x["id"] == oid), None)
            if o:
                for k, v in o["score"].items():
                    s[k] += v
    sorted_scores = sorted(s.values(), reverse=True)
    if sorted_scores[0] == sorted_scores[1]:
        return "neutral"
    return max(s, key=s.get)

# ── Body type quiz ───────────────────────────────────────────────
BT_QUESTIONS = [
    {"id":1,
     "q":"Stand in front of a mirror. How do your shoulders compare to your hips?",
     "opts":[{"id":"a","t":"Shoulders are clearly broader — hips are narrower","score":{"inverted_triangle":3}},
             {"id":"b","t":"Hips are clearly wider — shoulders are narrower","score":{"pear":3}},
             {"id":"c","t":"Both shoulders and hips look roughly the same width","score":{"rectangle":2,"hourglass":2}}]},
    {"id":2,
     "q":"Look at your waist — how defined is it compared to your hips and shoulders?",
     "opts":[{"id":"a","t":"Clearly defined — noticeably smaller, curves inward","score":{"hourglass":3}},
             {"id":"b","t":"Slightly defined — a little curve but not dramatic","score":{"pear":1,"inverted_triangle":1}},
             {"id":"c","t":"Not defined — sides are fairly straight up and down","score":{"rectangle":3}},
             {"id":"d","t":"The waist area is the widest part — pushes outward","score":{"apple":3}}]},
    {"id":3,
     "q":"Where does most of your body fullness sit?",
     "opts":[{"id":"a","t":"Shoulders and bust — I have a fuller upper body","score":{"inverted_triangle":3}},
             {"id":"b","t":"Stomach and tummy area — my middle is the most prominent","score":{"apple":3}},
             {"id":"c","t":"Hips, thighs and bottom — lower body is fuller","score":{"pear":3}},
             {"id":"d","t":"Evenly — hips and bust are similar, waist is smaller","score":{"hourglass":3}},
             {"id":"e","t":"Evenly all over — no single area is noticeably fuller","score":{"rectangle":3}}]},
    {"id":4,
     "q":"When you look at photos of yourself from the front, what stands out most?",
     "opts":[{"id":"a","t":"My shoulders and upper body look strong and broad","score":{"inverted_triangle":2}},
             {"id":"b","t":"My hips and lower body look fuller than my top","score":{"pear":2}},
             {"id":"c","t":"My waist is clearly smaller between my hips and shoulders","score":{"hourglass":2}},
             {"id":"d","t":"My tummy or midsection looks fuller than hips and shoulders","score":{"apple":2}},
             {"id":"e","t":"My body looks straight — similar width from top to bottom","score":{"rectangle":2}}]},
    {"id":5,
     "q":"If you traced your body outline from shoulders down to hips, which shape does it look most like?",
     "opts":[{"id":"a","t":"▽  Wide at top, narrows toward the hips","score":{"inverted_triangle":3}},
             {"id":"b","t":"△  Narrow at top, widens toward the hips","score":{"pear":3}},
             {"id":"c","t":"( )  Widest in the middle — oval or round shape","score":{"apple":3}},
             {"id":"d","t":"⬡  Wide at shoulders, narrow waist, wide at hips","score":{"hourglass":3}},
             {"id":"e","t":"▭  Same width all the way — straight rectangle","score":{"rectangle":3}}]},
]

def classify_bt(answers):
    s = {k: 0 for k in BT_INFO}
    for qid, oid in answers.items():
        q = next((x for x in BT_QUESTIONS if str(x["id"]) == str(qid)), None)
        if q:
            o = next((x for x in q["opts"] if x["id"] == oid), None)
            if o:
                weight = 2 if int(qid) in (1, 2) else 1
                for k, v in o["score"].items():
                    s[k] += v * weight
    top_score = max(s.values())
    top_types = [k for k, v in s.items() if v == top_score]
    if len(top_types) == 1:
        return top_types[0]
    tie_set = set(top_types)
    if tie_set == {"apple", "inverted_triangle"}:
        return "apple"
    if tie_set == {"rectangle", "hourglass"}:
        return "hourglass"
    return sorted(top_types)[0]

BT_INFO = {
    "hourglass":         {"name":"Hourglass","emoji":"⏳","desc":"Balanced shoulders and hips with a well-defined waist.",
                          "tips":["Wrap dresses highlight your curves","High-waisted bottoms","Fitted silhouettes","Belted coats"],
                          "avoid":["Shapeless boxy cuts","Drop-waist styles"]},
    "pear":              {"name":"Pear","emoji":"🍐","desc":"Hips wider than shoulders — create balance up top.",
                          "tips":["A-line skirts","Boat necks & off-shoulder tops","Structured jackets","Dark bottoms + bright tops"],
                          "avoid":["Skinny jeans with no top volume","Low-rise bottoms"]},
    "apple":             {"name":"Apple","emoji":"🍎","desc":"Fullness around the midsection — elongate the torso.",
                          "tips":["V-necks and wrap tops","Empire waist dresses","Monochromatic outfits","Flowy fabrics"],
                          "avoid":["Cropped tops","Belts at the waist"]},
    "rectangle":         {"name":"Rectangle","emoji":"▬","desc":"Shoulders, waist and hips roughly the same width — create curves.",
                          "tips":["Peplum tops","Ruffles and embellishments","Wrap styles","Layering"],
                          "avoid":["Boxy minimalist silhouettes","Straight-cut tunics"]},
    "inverted_triangle": {"name":"Inverted Triangle","emoji":"🔻","desc":"Broader shoulders than hips — add volume below.",
                          "tips":["Wide-leg trousers","A-line & full skirts","Minimal shoulder detail","Bright/detailed bottoms"],
                          "avoid":["Puff sleeves","Wide lapels","Boat necks"]},
}

# ── Palettes ─────────────────────────────────────────────────────
PALETTES = {
    "warm":{
        "desc":"Your warm undertone glows with earthy, golden tones.",
        "clothing":{
            "rec":[{"n":"Terracotta","h":"#C45C3A"},{"n":"Camel","h":"#C19A6B"},{"n":"Olive Green","h":"#808000"},
                   {"n":"Coral","h":"#FF6B6B"},{"n":"Burnt Orange","h":"#CC5500"},{"n":"Golden Yellow","h":"#FFD700"},
                   {"n":"Mustard","h":"#E1AD01"},{"n":"Warm Brown","h":"#8B4513"}],
            "avoid":[{"n":"Icy Blue","h":"#A5C8E1","r":"Washes out warm skin"},
                     {"n":"Fuchsia","h":"#FF00FF","r":"Clashes with golden tones"},
                     {"n":"Silver Grey","h":"#C0C0C0","r":"Makes warm skin look dull"}]},
        "makeup":{
            "rec":[{"n":"Peachy Blush","h":"#FFAE87"},{"n":"Bronze Highlight","h":"#CD7F32"},
                   {"n":"Rust Lip","h":"#B7410E"},{"n":"Copper Eye","h":"#B87333"},
                   {"n":"Golden Lip","h":"#D4A017"},{"n":"Warm Nude","h":"#C68642"}],
            "avoid":[{"n":"Cool Pink Lip","h":"#FF69B4","r":"Creates ashy effect"},
                     {"n":"Silver Eye","h":"#C0C0C0","r":"Dulls warm skin"}]}
    },
    "cool":{
        "desc":"Your cool undertone radiates with jewel tones and icy hues.",
        "clothing":{
            "rec":[{"n":"Sapphire Blue","h":"#0F52BA"},{"n":"Emerald","h":"#50C878"},
                   {"n":"Rose Pink","h":"#FF66CC"},{"n":"Lavender","h":"#967BB6"},
                   {"n":"Icy White","h":"#F0F8FF"},{"n":"Burgundy","h":"#800020"},
                   {"n":"Slate Grey","h":"#708090"},{"n":"Royal Purple","h":"#7851A9"}],
            "avoid":[{"n":"Warm Olive","h":"#808000","r":"Clashes with cool skin"},
                     {"n":"Camel","h":"#C19A6B","r":"Makes cool tones sallow"},
                     {"n":"Orange","h":"#FFA500","r":"Too warm for cool tones"}]},
        "makeup":{
            "rec":[{"n":"Rosy Pink","h":"#FF69B4"},{"n":"Silver Highlight","h":"#E8E8E8"},
                   {"n":"Berry Lip","h":"#8E2D56"},{"n":"Mauve Blush","h":"#C0909A"},
                   {"n":"Navy Liner","h":"#000080"},{"n":"Cool Red","h":"#DC143C"}],
            "avoid":[{"n":"Bronze/Copper","h":"#B87333","r":"Too warm, creates mismatch"},
                     {"n":"Coral Lip","h":"#FF6B6B","r":"Warm coral fights cool skin"}]}
    },
    "neutral":{
        "desc":"Lucky you — neutral undertones work beautifully with most palettes!",
        "clothing":{
            "rec":[{"n":"Dusty Rose","h":"#DCAE96"},{"n":"Sage Green","h":"#8CA67B"},
                   {"n":"Mauve","h":"#C0909A"},{"n":"Teal","h":"#008080"},
                   {"n":"Blush Pink","h":"#F4C2C2"},{"n":"Warm White","h":"#FAF0E6"},
                   {"n":"Slate Blue","h":"#6A7F9E"},{"n":"Taupe","h":"#BDB09F"}],
            "avoid":[{"n":"Neon Yellow","h":"#FFFF00","r":"Overpowers neutral skin"},
                     {"n":"Hot Pink","h":"#FF69B4","r":"Can be too harsh"}]},
        "makeup":{
            "rec":[{"n":"Warm Nude","h":"#C68642"},{"n":"Peachy Blush","h":"#FFAE87"},
                   {"n":"Rose Gold","h":"#B76E79"},{"n":"Mauve Lip","h":"#C0909A"},
                   {"n":"Champagne","h":"#F7E7CE"},{"n":"Brown Smoky","h":"#7B3F00"}],
            "avoid":[{"n":"Very Cool Red","h":"#C41E3A","r":"Skews too far cool"},
                     {"n":"Deep Orange","h":"#FF5700","r":"Too extreme for neutral"}]}
    }
}

TIPS = {
    "warm":[
        {"id":"w1","cat":"Clothing","emoji":"👗","tip":"Opt for earth tones — terracotta, rust, camel and olive always enhance warm undertones."},
        {"id":"w2","cat":"Clothing","emoji":"🧥","tip":"Natural fabrics in golden or warm tones like linen and cotton work beautifully."},
        {"id":"w3","cat":"Makeup","emoji":"💄","tip":"Warm-toned foundations with yellow or peach undertones blend seamlessly. Avoid pink-based formulas."},
        {"id":"w4","cat":"Makeup","emoji":"✨","tip":"Bronze and copper highlighters give the most natural sun-kissed glow."},
        {"id":"w5","cat":"Accessories","emoji":"💛","tip":"Gold jewellery is your metal — it harmonises with your golden undertone naturally."},
        {"id":"w6","cat":"Accessories","emoji":"👜","tip":"Tan, cognac or warm brown bags anchor any warm-toned outfit beautifully."},
    ],
    "cool":[
        {"id":"c1","cat":"Clothing","emoji":"👗","tip":"Jewel tones like sapphire, amethyst and emerald make your cool undertone radiate."},
        {"id":"c2","cat":"Clothing","emoji":"🧥","tip":"Crisp whites and icy pastels enhance your natural luminosity. Try powder blue or soft lilac."},
        {"id":"c3","cat":"Makeup","emoji":"💄","tip":"Choose foundations with pink or rosy undertones. Berry and plum lip colours are your signature."},
        {"id":"c4","cat":"Makeup","emoji":"✨","tip":"Silver and pearl highlighters create a cool, ethereal glow perfect for your undertone."},
        {"id":"c5","cat":"Accessories","emoji":"🩶","tip":"Silver jewellery complements your cool undertone. White gold is also ideal."},
        {"id":"c6","cat":"Accessories","emoji":"👜","tip":"Navy, black and charcoal bags are your neutrals — they anchor cool outfits effortlessly."},
    ],
    "neutral":[
        {"id":"n1","cat":"Clothing","emoji":"👗","tip":"Both warm and cool tones work. Dusty rose, mauve and teal are especially harmonious."},
        {"id":"n2","cat":"Clothing","emoji":"🧥","tip":"Muted complex tones like sage, blush and taupe are especially flattering."},
        {"id":"n3","cat":"Makeup","emoji":"💄","tip":"Rose-gold and nude-pink lip shades hit the sweet spot between warm and cool."},
        {"id":"n4","cat":"Makeup","emoji":"✨","tip":"Rose-gold or champagne highlighters bridge both undertone families beautifully."},
        {"id":"n5","cat":"Accessories","emoji":"🌸","tip":"Both gold and silver work on neutral undertones — mix metals freely!"},
        {"id":"n6","cat":"Accessories","emoji":"👜","tip":"Warm beige, taupe and dusty mauve bags complement your balanced undertone."},
    ]
}

# ════════════════════════════════════════════════════════════════
#  ROUTES — Auth (US-01)
# ════════════════════════════════════════════════════════════════
@app.route("/api/register", methods=["POST"])
def register():
    d = request.get_json() or {}
    name  = (d.get("name") or "").strip()
    email = (d.get("email") or "").strip().lower()
    pw    = d.get("password") or ""
    if not name or not email or not pw:
        return jsonify({"error":"All fields are required"}), 400
    if "@" not in email:
        return jsonify({"error":"Enter a valid email address"}), 400
    if len(pw) < 8 or not any(c.isdigit() for c in pw):
        return jsonify({"error":"Password must be 8+ characters with at least one number"}), 400
    c = db()
    try:
        c.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)", (name,email,hp(pw)))
        c.commit()
        uid = c.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()["id"]
        return jsonify({"token":make_token(uid),"name":name}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error":"Email already registered — please sign in"}), 409
    finally: c.close()

@app.route("/api/login", methods=["POST"])
def login():
    d = request.get_json() or {}
    email = (d.get("email") or "").strip().lower()
    pw    = d.get("password") or ""
    c = db()
    u = c.execute("SELECT * FROM users WHERE email=? AND password=?", (email,hp(pw))).fetchone()
    c.close()
    if not u: return jsonify({"error":"Incorrect email or password"}), 401
    return jsonify({"token":make_token(u["id"]),"name":u["name"],
                    "undertone":u["undertone"],"body_type":u["body_type"],
                    "face_shape":u["face_shape"]})

@app.route("/api/profile", methods=["GET"])
@auth
def profile():
    c = db()
    u = c.execute("SELECT id,name,email,undertone,body_type,face_shape,created FROM users WHERE id=?",
                  (request.uid,)).fetchone()
    bm = [r["tip_id"] for r in c.execute("SELECT tip_id FROM bookmarks WHERE user_id=?",
                                          (request.uid,)).fetchall()]
    c.close()
    if not u: return jsonify({"error":"Not found"}), 404
    return jsonify({"id":u["id"],"name":u["name"],"email":u["email"],
                    "undertone":u["undertone"],"body_type":u["body_type"],
                    "face_shape":u["face_shape"],
                    "created":u["created"],"bookmarks":bm})

# ════════════════════════════════════════════════════════════════
#  ROUTES — Undertone Quiz (US-02)
# ════════════════════════════════════════════════════════════════
@app.route("/api/quiz/undertone/questions", methods=["GET"])
@auth
def ut_questions():
    return jsonify({"questions":UT_QUESTIONS,"total":len(UT_QUESTIONS)})

@app.route("/api/quiz/undertone/submit", methods=["POST"])
@auth
def ut_submit():
    answers = (request.get_json() or {}).get("answers",{})
    if len(answers) < len(UT_QUESTIONS):
        return jsonify({"error":"Please answer all questions"}), 400
    result = classify_ut(answers)
    c = db()
    c.execute("INSERT INTO quiz_log(user_id,type,answers,result) VALUES(?,?,?,?)",
              (request.uid,"undertone",json.dumps(answers),result))
    c.execute("UPDATE users SET undertone=? WHERE id=?", (result,request.uid))
    c.commit(); c.close()
    return jsonify({"undertone":result,"description":PALETTES[result]["desc"],
                    "tips":TIPS[result]})

# ════════════════════════════════════════════════════════════════
#  ROUTES — Color Palette (US-03)
# ════════════════════════════════════════════════════════════════
@app.route("/api/palette", methods=["GET"])
@auth
def palette():
    c = db()
    u = c.execute("SELECT undertone FROM users WHERE id=?", (request.uid,)).fetchone()
    c.close()
    if not u or not u["undertone"]:
        return jsonify({"error":"Complete the undertone quiz first"}), 400
    ut = u["undertone"]
    return jsonify({"undertone":ut,"palette":PALETTES[ut]})

# ════════════════════════════════════════════════════════════════
#  ROUTES — Styling Tips + Bookmarks (US-04)
# ════════════════════════════════════════════════════════════════
@app.route("/api/tips", methods=["GET"])
@auth
def tips():
    c = db()
    u = c.execute("SELECT undertone FROM users WHERE id=?", (request.uid,)).fetchone()
    c.close()
    if not u or not u["undertone"]:
        return jsonify({"error":"Complete the undertone quiz first"}), 400
    return jsonify({"tips":TIPS[u["undertone"]]})

@app.route("/api/bookmarks", methods=["POST"])
@auth
def toggle_bookmark():
    tip_id = (request.get_json() or {}).get("tip_id")
    if not tip_id: return jsonify({"error":"tip_id required"}), 400
    c = db()
    ex = c.execute("SELECT id FROM bookmarks WHERE user_id=? AND tip_id=?",
                   (request.uid,tip_id)).fetchone()
    if ex:
        c.execute("DELETE FROM bookmarks WHERE user_id=? AND tip_id=?", (request.uid,tip_id))
        c.commit(); c.close()
        return jsonify({"bookmarked":False})
    c.execute("INSERT INTO bookmarks(user_id,tip_id) VALUES(?,?)", (request.uid,tip_id))
    c.commit(); c.close()
    return jsonify({"bookmarked":True})

# ════════════════════════════════════════════════════════════════
#  ROUTES — Body Type Quiz (US-05)
# ════════════════════════════════════════════════════════════════
@app.route("/api/quiz/bodytype/questions", methods=["GET"])
@auth
def bt_questions():
    return jsonify({"questions":BT_QUESTIONS,"total":len(BT_QUESTIONS)})

@app.route("/api/quiz/bodytype/submit", methods=["POST"])
@auth
def bt_submit():
    answers = (request.get_json() or {}).get("answers",{})
    if len(answers) < len(BT_QUESTIONS):
        return jsonify({"error":"Please answer all questions"}), 400
    result = classify_bt(answers)
    c = db()
    c.execute("INSERT INTO quiz_log(user_id,type,answers,result) VALUES(?,?,?,?)",
              (request.uid,"bodytype",json.dumps(answers),result))
    c.execute("UPDATE users SET body_type=? WHERE id=?", (result,request.uid))
    c.commit(); c.close()
    return jsonify({"body_type":result,"info":BT_INFO[result]})

# ════════════════════════════════════════════════════════════════
#  ROUTES — Wardrobe (US-08 partial / Sprint 1 basic)
# ════════════════════════════════════════════════════════════════
@app.route("/api/wardrobe", methods=["GET"])
@auth
def get_wardrobe():
    c = db()
    items = c.execute("SELECT * FROM wardrobe WHERE user_id=? ORDER BY added DESC",
                      (request.uid,)).fetchall()
    c.close()
    return jsonify({"items":[dict(i) for i in items]})

@app.route("/api/wardrobe", methods=["POST"])
@auth
def add_wardrobe():
    d = request.get_json() or {}
    filename  = d.get("filename","item.jpg")
    category  = d.get("category","Top")
    style_tag = d.get("style_tag","Casual")
    color     = d.get("color","")
    c = db()
    try:
        c.execute("ALTER TABLE wardrobe ADD COLUMN color TEXT")
        c.commit()
    except Exception:
        pass
    c.execute("INSERT INTO wardrobe(user_id,filename,category,style_tag,color) VALUES(?,?,?,?,?)",
              (request.uid,filename,category,style_tag,color))
    c.commit()
    item_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.close()
    return jsonify({"id":item_id,"filename":filename,"category":category,"style_tag":style_tag,"color":color}), 201

@app.route("/api/wardrobe/<int:item_id>", methods=["DELETE"])
@auth
def del_wardrobe(item_id):
    c = db()
    c.execute("DELETE FROM wardrobe WHERE id=? AND user_id=?", (item_id,request.uid))
    c.commit(); c.close()
    return jsonify({"deleted":True})

@app.route("/api/wardrobe/outfit", methods=["POST"])
@auth
def gen_outfit():
    c     = db()
    items = list(c.execute("SELECT * FROM wardrobe WHERE user_id=?",
                           (request.uid,)).fetchall())[:20]
    ut    = c.execute("SELECT undertone FROM users WHERE id=?",
                      (request.uid,)).fetchone()
    c.close()

    if len(items) < 2:
        return jsonify({"error":"Add at least 2 wardrobe items to generate an outfit"}), 400

    d     = request.get_json() or {}
    event = d.get("event_type","casual")

    hijab_map   = {"warm":"#C9956C","cool":"#A8C5DA","neutral":"#D4C5B0"}
    undertone   = ut["undertone"] if ut and ut["undertone"] else "neutral"
    hijab_color = hijab_map.get(undertone,"#D4C5B0")

    tips_map = {"warm":"Pair with gold accessories",
                "cool":"Pair with silver accessories",
                "neutral":"Mix metals freely"}

    badge_map = {
        "casual":      "Casual Chic ✦",
        "formal":      "Office Ready ✦",
        "party":       "Party Perfect ✦",
        "traditional": "Elegant Traditional ✦",
        "sports":      "Active Fit ✦"
    }

    def match_event(item):
        tag = (item["style_tag"] or "").lower()
        if event == "sports":      return tag in ("sports","casual")
        if event == "formal":      return tag in ("formal","party")
        if event == "party":       return tag in ("party","formal")
        if event == "traditional": return tag in ("traditional","casual")
        return True

    event_items = [i for i in items if match_event(i)]
    if len(event_items) < 2:
        event_items = items

    tops = [i for i in event_items if i["category"] in ("Top","Shirt","Blouse","Jacket","Kurta","Sweater","Coat","Abaya")]
    bots = [i for i in event_items if i["category"] in ("Bottom","Skirt","Trousers","Jeans","Pants","Leggings","Dress","Shalwar")]
    accs = [i for i in event_items if i["category"] in ("Hijab","Dupatta","Bag","Shoes","Belt","Scarf")]

    combo = []
    if tops: combo.append(dict(tops[0]))
    if bots: combo.append(dict(bots[0]))
    if not combo: combo = [dict(event_items[0]),dict(event_items[1])]

    import random
    top_pool = tops if tops else event_items
    bot_pool = bots if bots else event_items
    outfits = []
    used = set()
    for _ in range(min(3, max(1, len(event_items)-1))):
        for attempt in range(10):
            t = dict(random.choice(top_pool))
            b = dict(random.choice(bot_pool))
            key = (t["id"], b["id"])
            if key not in used or attempt > 5:
                used.add(key); break
        outfit_items = [t, b]
        if accs: outfit_items.append(dict(random.choice(accs)))
        outfits.append({"items": outfit_items, "event": event,
                        "badge": badge_map.get(event, "Perfect Match ✦"),
                        "hijab_color": hijab_color})

    return jsonify({"outfit":combo,"outfits":outfits,
                    "accessory_tip":tips_map.get(undertone,""),
                    "hijab_color":hijab_color,"badge":badge_map.get(event,"Perfect Match ✦")})

# ── Serve models for face-api.js ──────────────────────────────────
@app.route("/models/<path:filename>")
def serve_models(filename):
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    if os.path.exists(os.path.join(models_dir, filename)):
        return send_from_directory(models_dir, filename)
    return jsonify({"error": "Model not found"}), 404

# ── Serve frontend ────────────────────────────────────────────────
@app.route("/", defaults={"p":""})
@app.route("/<path:p>")
def serve(p):
    fp = os.path.join(app.static_folder, p)
    if p and os.path.exists(fp):
        return send_from_directory(app.static_folder, p)
    return send_from_directory(app.template_folder, "index.html")

# ══════════════════════════════════════════
# SPRINT 2 ROUTES
# ══════════════════════════════════════════

# ── US-06 & US-07: Save photo analysis result (from face-api.js frontend)
@app.route("/api/photo/save-result", methods=["POST"])
@auth
def save_photo_result():
    d          = request.get_json() or {}
    undertone  = d.get("undertone","neutral")
    skin_tone  = d.get("skin_tone","medium")
    face_shape = d.get("face_shape")
    save_photo = d.get("save_photo", False)
    swatch     = d.get("swatch_color","#C8A882")

    c = db()
    c.execute(
        "INSERT INTO photo_analysis(user_id,skin_tone,undertone,face_shape,photo_saved) VALUES(?,?,?,?,?)",
        (request.uid, skin_tone, undertone, face_shape, 1 if save_photo else 0)
    )
    c.execute("UPDATE users SET undertone=? WHERE id=?",  (undertone,  request.uid))
    if face_shape:
        c.execute("UPDATE users SET face_shape=? WHERE id=?", (face_shape, request.uid))
    c.commit(); c.close()
    return jsonify({"saved":True,"undertone":undertone,"face_shape":face_shape})

# ── US-07: Get saved face shape
@app.route("/api/face-shape", methods=["GET"])
@auth
def get_face_shape():
    c  = db()
    u  = c.execute("SELECT face_shape FROM users WHERE id=?", (request.uid,)).fetchone()
    c.close()
    fs = u["face_shape"] if u and u["face_shape"] else None
    descriptions = {
        "oval":   "Slightly wider at cheekbones — the most versatile shape.",
        "round":  "Equal width and length with soft, curved edges.",
        "square": "Strong angular jaw with roughly equal width and length.",
        "heart":  "Wider at forehead, narrows to a pointed chin.",
        "oblong": "Longer than wide with a straight cheek line."
    }
    return jsonify({"face_shape":fs,"description":descriptions.get(fs,"")})

# ── US-07: Manual face shape quiz
FACE_QUIZ = [
    {"id":1,"q":"Is your forehead wider than your jaw?",
     "opts":[{"id":"a","t":"Yes, noticeably wider"},{"id":"b","t":"About the same"},{"id":"c","t":"Jaw is wider"}]},
    {"id":2,"q":"Is your face longer than it is wide?",
     "opts":[{"id":"a","t":"Yes, quite long"},{"id":"b","t":"Roughly equal"},{"id":"c","t":"Very round"}]},
    {"id":3,"q":"Do you have a strong angular jawline?",
     "opts":[{"id":"a","t":"Yes, very angular"},{"id":"b","t":"Somewhat defined"},{"id":"c","t":"Soft and rounded"}]},
    {"id":4,"q":"Are your cheekbones the widest part of your face?",
     "opts":[{"id":"a","t":"Yes, prominent"},{"id":"b","t":"Somewhat"},{"id":"c","t":"No, jaw or forehead is wider"}]},
]

def classify_face(ans):
    if ans.get("1")=="a" and ans.get("3")=="c": return "heart"
    if ans.get("2")=="a" and ans.get("3")=="b": return "oblong"
    if ans.get("3")=="a":                        return "square"
    if ans.get("2")=="c" or ans.get("3")=="c":  return "round"
    return "oval"

@app.route("/api/face-shape/quiz/questions", methods=["GET"])
@auth
def face_quiz_q(): return jsonify({"questions":FACE_QUIZ})

@app.route("/api/face-shape/quiz/submit", methods=["POST"])
@auth
def face_quiz_submit():
    answers    = (request.get_json() or {}).get("answers",{})
    face_shape = classify_face(answers)
    c = db()
    c.execute("UPDATE users SET face_shape=? WHERE id=?", (face_shape, request.uid))
    c.execute("INSERT INTO photo_analysis(user_id,face_shape,photo_saved) VALUES(?,?,0)",
              (request.uid, face_shape))
    c.commit(); c.close()
    return jsonify({"face_shape":face_shape})

# ── US-08: Products
@app.route("/api/products", methods=["GET"])
@auth
def get_products():
    c         = db()
    u         = c.execute("SELECT undertone FROM users WHERE id=?", (request.uid,)).fetchone()
    undertone = u["undertone"] if u and u["undertone"] else None

    if not undertone:
        c.close()
        return jsonify({"products": [], "undertone": None, "quiz_required": True})

    category  = request.args.get("category")
    q, p      = "SELECT * FROM product_recommendations WHERE undertone=?", [undertone]
    if category: q += " AND category=?"; p.append(category)
    products  = c.execute(q, p).fetchall()
    c.close()
    return jsonify({"products":[dict(x) for x in products],"undertone":undertone})

# ── US-08: Wishlist
@app.route("/api/wishlist", methods=["GET","POST"])
@auth
def wishlist():
    c = db()
    if request.method=="GET":
        rows = c.execute(
            "SELECT w.id as wishlist_id, p.* FROM wishlist w "
            "JOIN product_recommendations p ON w.product_id=p.id WHERE w.user_id=?",
            (request.uid,)).fetchall()
        c.close()
        return jsonify({"wishlist":[dict(r) for r in rows]})
    pid = (request.get_json() or {}).get("product_id")
    ex  = c.execute("SELECT id FROM wishlist WHERE user_id=? AND product_id=?",
                    (request.uid,pid)).fetchone()
    if ex:
        c.execute("DELETE FROM wishlist WHERE id=?", (ex["id"],))
        c.commit(); c.close(); return jsonify({"saved":False})
    c.execute("INSERT INTO wishlist(user_id,product_id) VALUES(?,?)", (request.uid,pid))
    c.commit(); c.close(); return jsonify({"saved":True})

# ── US-09: Save favourite outfit
@app.route("/api/wardrobe/favourite", methods=["POST"])
@auth
def save_fav():
    d = request.get_json() or {}
    c = db()
    c.execute("INSERT INTO quiz_log(user_id,type,answers,result) VALUES(?,?,?,?)",
              (request.uid,"outfit_fav",
               json.dumps(d.get("item_ids",[])),"saved"))
    c.commit(); c.close()
    return jsonify({"message":"Outfit saved ⭐"})

# ── US-10: Style suggestions
@app.route("/api/style-suggestions", methods=["GET"])
@auth
def style_suggestions():
    c  = db()
    u  = c.execute("SELECT face_shape FROM users WHERE id=?", (request.uid,)).fetchone()
    fs = u["face_shape"] if u and u["face_shape"] else None
    if not fs:
        c.close()
        return jsonify({"face_shape": None, "suggestions": []})
    cat= request.args.get("category")
    q, p = "SELECT * FROM style_suggestions WHERE face_shape=?", [fs]
    if cat: q += " AND category=?"; p.append(cat)
    rows = c.execute(q,p).fetchall()
    c.close()
    return jsonify({"face_shape":fs,"suggestions":[dict(r) for r in rows]})

# ── US-10: Style bookmarks
@app.route("/api/bookmarks/style", methods=["POST"])
@auth
def style_bookmark():
    sid = (request.get_json() or {}).get("suggestion_id")
    c   = db()
    ex  = c.execute("SELECT id FROM style_bookmarks WHERE user_id=? AND suggestion_id=?",
                    (request.uid,sid)).fetchone()
    if ex:
        c.execute("DELETE FROM style_bookmarks WHERE id=?", (ex["id"],))
        c.commit(); c.close(); return jsonify({"bookmarked":False})
    c.execute("INSERT INTO style_bookmarks(user_id,suggestion_id) VALUES(?,?)",
              (request.uid,sid))
    c.commit(); c.close(); return jsonify({"bookmarked":True})


# ── Forgot / Reset Password ───────────────────────────────────────
import secrets, datetime as dt

PASSWORD_RESET_TOKENS = {}   # token -> {user_id, expires}

@app.route("/api/forgot-password", methods=["POST"])


def forgot_password():
    email = ((request.get_json() or {}).get("email") or "").strip().lower()
    if not email or "@" not in email:
        return jsonify({"error": "Enter a valid email address"}), 400
    c = db()
    u = c.execute("SELECT id, name FROM users WHERE email=?", (email,)).fetchone()
    if u:
        token = secrets.token_urlsafe(32)
        expires = (dt.datetime.utcnow() + dt.timedelta(hours=1)).isoformat()
        c.execute("DELETE FROM password_reset_tokens WHERE user_id=?", (u["id"],))
        c.execute("INSERT INTO password_reset_tokens(token,user_id,expires) VALUES(?,?,?)",
                  (token, u["id"], expires))
        c.commit()
        reset_link = f"http://localhost:5000/?reset_token={token}"
        print(f"\n PASSWORD RESET LINK for {email}:\n   {reset_link}\n")
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            html_body = f"""
            <div style="font-family:Arial,sans-serif;max-width:500px;margin:0 auto;padding:20px;">
              <h2 style="color:#C0546A;font-family:Georgia,serif;">Glam<em>Match</em></h2>
              <p>Hi {u['name']},</p>
              <p>We received a request to reset your GlamMatch password.</p>
              <p>Click the button below to set a new password:</p>
              <div style="text-align:center;margin:30px 0;">
                <a href="{reset_link}"
                   style="background:#C0546A;color:#fff;padding:12px 30px;border-radius:50px;
                          text-decoration:none;font-weight:bold;font-size:15px;">
                  Reset My Password
                </a>
              </div>
              <p style="color:#999;font-size:13px;">This link expires in 1 hour.</p>
              <p style="color:#999;font-size:13px;">If you didn't request this, ignore this email.</p>
              <hr style="border:none;border-top:1px solid #eee;margin:20px 0;"/>
              <p style="color:#ccc;font-size:12px;">— The GlamMatch Team 💄</p>
            </div>
            """
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "GlamMatch — Reset Your Password 🔑"
            msg["From"]    = f"GlamMatch <{FROM_EMAIL}>"
            msg["To"]      = email
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
                s.starttls()
                s.login(SMTP_USER, SMTP_PASS)
                s.sendmail(FROM_EMAIL, [email], msg.as_string())
            print(f"✉️  Reset email sent to {email}")
        except Exception as e:
            print(f" Email failed: {e}")
    c.close()
    return jsonify({"message": "If that email is registered, a reset link has been sent."})
@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    d        = request.get_json() or {}
    token    = (d.get("token") or "").strip()
    password = d.get("password") or ""
    if not token or not password:
        return jsonify({"error": "Token and password are required"}), 400
    if len(password) < 8 or not any(c.isdigit() for c in password):
        return jsonify({"error": "Password must be 8+ characters with at least one number"}), 400
    conn = db()
    entry = conn.execute("SELECT * FROM password_reset_tokens WHERE token=?", (token,)).fetchone()
    if not entry:
        conn.close()
        return jsonify({"error": "Invalid or expired reset link"}), 400
    if dt.datetime.utcnow() > dt.datetime.fromisoformat(entry["expires"]):
        conn.execute("DELETE FROM password_reset_tokens WHERE token=?", (token,))
        conn.commit(); conn.close()
        return jsonify({"error": "Reset link has expired. Please request a new one."}), 400
    conn.execute("UPDATE users SET password=? WHERE id=?", (hp(password), entry["user_id"]))
    conn.execute("DELETE FROM password_reset_tokens WHERE token=?", (token,))
    conn.commit(); conn.close()
    return jsonify({"message": "Password reset successfully"})

# ══════════════════════════════════════════════════════════════════
#  SPRINT 3 — SALON CONNECTOR PLATFORM
#  US-11: Salon Discovery | US-12: Salon Profile | US-13: Booking
#  US-14: Chat           | US-15: Reviews
# ══════════════════════════════════════════════════════════════════

def init_salon_db():
    c = db()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS salons(
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            address       TEXT,
            category      TEXT DEFAULT 'women',
            price_range   TEXT DEFAULT 'mid',
            rating        REAL DEFAULT 0.0,
            review_count  INTEGER DEFAULT 0,
            working_hours TEXT DEFAULT '9:00 AM – 8:00 PM',
            phone         TEXT,
            description   TEXT,
            created_at    TEXT DEFAULT(datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS salon_services(
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            salon_id     INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            service_type TEXT,
            price_min    INTEGER DEFAULT 0,
            price_max    INTEGER DEFAULT 0,
            duration_min INTEGER DEFAULT 60,
            FOREIGN KEY(salon_id) REFERENCES salons(id)
        );
        CREATE TABLE IF NOT EXISTS bookings(
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            salon_id   INTEGER NOT NULL,
            service_id INTEGER,
            datetime   TEXT NOT NULL,
            status     TEXT DEFAULT 'pending',
            note       TEXT,
            alt_time   TEXT,
            created_at TEXT DEFAULT(datetime('now')),
            FOREIGN KEY(user_id)    REFERENCES users(id),
            FOREIGN KEY(salon_id)   REFERENCES salons(id),
            FOREIGN KEY(service_id) REFERENCES salon_services(id)
        );
        CREATE TABLE IF NOT EXISTS chat_messages(
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id  INTEGER NOT NULL,
            sender_type TEXT NOT NULL,
            message     TEXT NOT NULL,
            sent_at     TEXT DEFAULT(datetime('now')),
            FOREIGN KEY(booking_id) REFERENCES bookings(id)
        );
        CREATE TABLE IF NOT EXISTS reviews(
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            salon_id    INTEGER NOT NULL,
            booking_id  INTEGER,
            rating      INTEGER NOT NULL,
            review_text TEXT,
            created_at  TEXT DEFAULT(datetime('now')),
            UNIQUE(user_id, booking_id),
            FOREIGN KEY(user_id)   REFERENCES users(id),
            FOREIGN KEY(salon_id)  REFERENCES salons(id),
            FOREIGN KEY(booking_id) REFERENCES bookings(id)
        );
    """)
    c.commit()

    # Seed salons if empty
    if not c.execute("SELECT 1 FROM salons LIMIT 1").fetchone():
        salons = [
            ("Glamour Studio",    "12 Mall Road, Lahore",       "women",  "mid",      4.7, 38, "10:00 AM – 9:00 PM",  "+92-300-1234567", "Premium beauty studio specializing in bridal and editorial makeup."),
            ("The Beauty Lounge", "45 DHA Phase 5, Lahore",     "women",  "premium",  4.5, 22, "9:00 AM – 8:00 PM",   "+92-321-9876543", "Relaxing lounge offering hair, skin, and nail treatments."),
            ("Zara Salon",        "88 Johar Town, Lahore",      "unisex", "budget",   4.2, 55, "8:30 AM – 9:30 PM",   "+92-333-5551234", "Affordable salon for everyday cuts, color, and grooming."),
            ("Bridal Affairs",    "3 Gulberg III, Lahore",      "women",  "premium",  4.9, 14, "10:00 AM – 7:00 PM",  "+92-311-7778888", "Exclusive bridal studio with full event packages."),
            ("SnipMaster",        "22 Model Town, Lahore",      "men",    "budget",   4.3, 41, "9:00 AM – 10:00 PM",  "+92-345-4440000", "Classic barbershop with modern grooming services."),
            ("Nails & Beyond",    "67 Bahria Town, Lahore",     "women",  "mid",      4.6, 29, "10:00 AM – 8:00 PM",  "+92-300-9990001", "Nail art, gel extensions, and pedicure specialist."),
            ("Style Hub",         "11 Faisal Town, Lahore",     "unisex", "mid",      4.1, 63, "9:00 AM – 9:00 PM",   "+92-322-1231231", "Full-service salon covering all hair and beauty needs."),
            ("Elite Spa & Salon", "5 Cantt, Lahore",            "women",  "premium",  4.8, 18, "10:00 AM – 7:30 PM",  "+92-301-5556789", "Luxury spa and salon experience with trained therapists."),
        ]
        c.executemany(
            "INSERT INTO salons(name,address,category,price_range,rating,review_count,working_hours,phone,description) VALUES(?,?,?,?,?,?,?,?,?)",
            salons
        )
        c.commit()

        # Seed services
        services = [
            # Glamour Studio (id=1)
            (1,"Bridal Makeup",       "makeup",  8000,15000, 180),
            (1,"Party Makeup",         "makeup",  3000, 6000,  90),
            (1,"Hair Styling",         "hair",    1500, 3000,  60),
            (1,"Facial",              "skincare",1500, 3500,  60),
            # The Beauty Lounge (id=2)
            (2,"Hair Cut & Blow Dry",  "hair",    1200, 2500,  60),
            (2,"Hair Color",           "hair",    3000, 8000, 120),
            (2,"Manicure",             "nails",    800, 1500,  45),
            (2,"Pedicure",             "nails",    900, 1800,  45),
            # Zara Salon (id=3)
            (3,"Basic Haircut",        "hair",     500,  800,  30),
            (3,"Threading",            "skincare", 150,  250,  15),
            (3,"Waxing (Full)",        "skincare", 800, 1200,  60),
            (3,"Simple Makeup",        "makeup",  1500, 2500,  60),
            # Bridal Affairs (id=4)
            (4,"Full Bridal Package",  "makeup", 20000,50000, 360),
            (4,"Mehndi Makeup",        "makeup",  5000,10000, 120),
            (4,"Trial Makeup",         "makeup",  3000, 5000,  90),
            (4,"Hair Treatment",       "hair",    2000, 5000,  90),
            # SnipMaster (id=5)
            (5,"Haircut",              "hair",     400,  700,  30),
            (5,"Shave",                "hair",     300,  500,  20),
            (5,"Beard Trim",           "hair",     250,  400,  15),
            (5,"Hair Color",           "hair",    1500, 3000,  60),
            # Nails & Beyond (id=6)
            (6,"Gel Nails",            "nails",   1500, 2500,  60),
            (6,"Nail Art",             "nails",    500, 1500,  45),
            (6,"Pedicure Deluxe",      "nails",   1200, 2000,  60),
            (6,"Acrylic Extensions",   "nails",   2000, 3500,  90),
            # Style Hub (id=7)
            (7,"Haircut (Women)",      "hair",     800, 1500,  45),
            (7,"Haircut (Men)",        "hair",     400,  700,  30),
            (7,"Highlights",           "hair",    3000, 7000, 120),
            (7,"Facial Basic",         "skincare",1000, 2000,  60),
            # Elite Spa & Salon (id=8)
            (8,"Luxury Facial",        "skincare",3500, 6000,  90),
            (8,"Body Massage",         "skincare",4000, 7000,  90),
            (8,"Hair Spa",             "hair",    2000, 4000,  60),
            (8,"Full Glam Makeup",     "makeup",  5000, 9000, 120),
        ]
        c.executemany(
            "INSERT INTO salon_services(salon_id,service_name,service_type,price_min,price_max,duration_min) VALUES(?,?,?,?,?,?)",
            services
        )
        c.commit()
    c.close()

# ── US-11: Salon Discovery ────────────────────────────────────────
@app.route("/api/salons", methods=["GET"])
@auth
def get_salons():
    c = db()
    q = "SELECT * FROM salons WHERE 1=1"
    p = []
    st = request.args.get("service_type")
    pr = request.args.get("price_range")
    ct = request.args.get("category")
    if pr:  q += " AND price_range=?";  p.append(pr)
    if ct and ct != "all": q += " AND (category=? OR category='unisex')"; p.append(ct)
    q += " ORDER BY rating DESC"
    salons = c.execute(q, p).fetchall()

    result = []
    for s in salons:
        sd = dict(s)
        if st:
            svc_match = c.execute(
                "SELECT id FROM salon_services WHERE salon_id=? AND service_type=? LIMIT 1",
                (s["id"], st)
            ).fetchone()
            if not svc_match:
                continue
        result.append(sd)
    c.close()
    return jsonify({"salons": result, "count": len(result)})

# ── US-12: Salon Profile ──────────────────────────────────────────
@app.route("/api/salons/<int:salon_id>", methods=["GET"])
@auth
def get_salon(salon_id):
    c = db()
    s = c.execute("SELECT * FROM salons WHERE id=?", (salon_id,)).fetchone()
    if not s:
        c.close()
        return jsonify({"error": "Salon not found"}), 404
    services = c.execute(
        "SELECT * FROM salon_services WHERE salon_id=? ORDER BY service_type, service_name",
        (salon_id,)
    ).fetchall()
    reviews = c.execute(
        """SELECT r.*, u.name as user_name FROM reviews r
           JOIN users u ON r.user_id = u.id
           WHERE r.salon_id=? ORDER BY r.created_at DESC LIMIT 10""",
        (salon_id,)
    ).fetchall()
    c.close()
    return jsonify({
        "salon":    dict(s),
        "services": [dict(sv) for sv in services],
        "reviews":  [dict(rv) for rv in reviews],
    })

# ── US-13: Booking ────────────────────────────────────────────────
@app.route("/api/bookings", methods=["GET"])
@auth
def get_bookings():
    c = db()
    rows = c.execute(
        """SELECT b.*, s.name as salon_name, sv.service_name
           FROM bookings b
           JOIN salons s ON b.salon_id = s.id
           LEFT JOIN salon_services sv ON b.service_id = sv.id
           WHERE b.user_id=? ORDER BY b.created_at DESC""",
        (request.uid,)
    ).fetchall()
    c.close()
    return jsonify({"bookings": [dict(r) for r in rows]})

@app.route("/api/bookings", methods=["POST"])
@auth
def create_booking():
    d = request.get_json() or {}
    salon_id   = d.get("salon_id")
    service_id = d.get("service_id")
    datetime_  = d.get("datetime", "").strip()
    note       = d.get("note", "")
    if not salon_id or not datetime_:
        return jsonify({"error": "salon_id and datetime are required"}), 400
    c = db()
    s = c.execute("SELECT id FROM salons WHERE id=?", (salon_id,)).fetchone()
    if not s:
        c.close()
        return jsonify({"error": "Salon not found"}), 404
    c.execute(
        "INSERT INTO bookings(user_id,salon_id,service_id,datetime,note) VALUES(?,?,?,?,?)",
        (request.uid, salon_id, service_id, datetime_, note)
    )
    c.commit()
    bid = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.close()
    return jsonify({"booking_id": bid, "status": "pending"}), 201

@app.route("/api/bookings/<int:bid>", methods=["PUT"])
@auth
def update_booking(bid):
    d      = request.get_json() or {}
    status = d.get("status")
    alt    = d.get("alt_time", "")
    allowed = ("confirmed", "rejected", "alternate", "completed")
    if status not in allowed:
        return jsonify({"error": f"status must be one of {allowed}"}), 400
    c = db()
    c.execute("UPDATE bookings SET status=?, alt_time=? WHERE id=?", (status, alt, bid))
    c.commit(); c.close()
    return jsonify({"booking_id": bid, "status": status})

# ── US-14: Chat ───────────────────────────────────────────────────
@app.route("/api/chat/<int:bid>", methods=["GET"])
@auth
def get_chat(bid):
    c    = db()
    msgs = c.execute(
        "SELECT * FROM chat_messages WHERE booking_id=? ORDER BY sent_at ASC",
        (bid,)
    ).fetchall()
    c.close()
    return jsonify({"messages": [dict(m) for m in msgs]})

@app.route("/api/chat/<int:bid>", methods=["POST"])
@auth
def send_chat(bid):
    d    = request.get_json() or {}
    msg  = (d.get("message") or "").strip()
    sender = d.get("sender_type", "user")
    if not msg:
        return jsonify({"error": "message is required"}), 400
    if sender not in ("user", "salon"):
        sender = "user"
    c = db()
    c.execute(
        "INSERT INTO chat_messages(booking_id,sender_type,message) VALUES(?,?,?)",
        (bid, sender, msg)
    )
    c.commit()
    mid = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.close()
    return jsonify({"message_id": mid, "sent": True}), 201

# ── US-15: Reviews ────────────────────────────────────────────────
@app.route("/api/reviews", methods=["POST"])
@auth
def post_review():
    d          = request.get_json() or {}
    salon_id   = d.get("salon_id")
    booking_id = d.get("booking_id")
    rating     = d.get("rating")
    text       = (d.get("review_text") or "").strip()
    if not salon_id or not rating or not (1 <= int(rating) <= 5):
        return jsonify({"error": "salon_id and rating (1–5) are required"}), 400
    c = db()
    try:
        c.execute(
            "INSERT INTO reviews(user_id,salon_id,booking_id,rating,review_text) VALUES(?,?,?,?,?)",
            (request.uid, salon_id, booking_id, int(rating), text)
        )
        c.commit()
        # Update salon average rating
        avg = c.execute(
            "SELECT AVG(rating) as avg, COUNT(*) as cnt FROM reviews WHERE salon_id=?",
            (salon_id,)
        ).fetchone()
        c.execute(
            "UPDATE salons SET rating=?, review_count=? WHERE id=?",
            (round(avg["avg"], 1), avg["cnt"], salon_id)
        )
        c.commit()
        c.close()
        return jsonify({"saved": True, "rating": int(rating)}), 201
    except Exception as e:
        c.close()
        if "UNIQUE" in str(e):
            return jsonify({"error": "You have already reviewed this appointment"}), 409
        return jsonify({"error": str(e)}), 500

@app.route("/api/salons/<int:salon_id>/reviews", methods=["GET"])
@auth
def salon_reviews(salon_id):
    c    = db()
    rows = c.execute(
        """SELECT r.*, u.name as user_name FROM reviews r
           JOIN users u ON r.user_id = u.id
           WHERE r.salon_id=? ORDER BY r.created_at DESC""",
        (salon_id,)
    ).fetchall()
    c.close()
    return jsonify({"reviews": [dict(r) for r in rows]})


# ══════════════════════════════════════════════════════════════════
#  PARLOUR REGISTRATION — US (new) — Salon owner onboarding
# ══════════════════════════════════════════════════════════════════

def init_parlour_applications_db():
    c = db()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS parlour_applications(
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            submitted_by    INTEGER,
            name            TEXT NOT NULL,
            owner_name      TEXT NOT NULL,
            cnic            TEXT NOT NULL,
            phone           TEXT NOT NULL,
            email           TEXT NOT NULL,
            category        TEXT,
            description     TEXT,
            address         TEXT,
            city            TEXT,
            area            TEXT,
            maps_link       TEXT,
            price_range     TEXT,
            working_hours   TEXT,
            services_json   TEXT,
            photo_count     INTEGER DEFAULT 0,
            cnic_doc_count  INTEGER DEFAULT 0,
            has_cert        INTEGER DEFAULT 0,
            has_health      INTEGER DEFAULT 0,
            status          TEXT DEFAULT 'pending',
            submitted_at    TEXT DEFAULT(datetime('now')),
            reviewed_at     TEXT,
            review_note     TEXT,
            FOREIGN KEY(submitted_by) REFERENCES users(id)
        );
    """)
    c.commit()
    c.close()

@app.route("/api/parlour/register", methods=["POST"])
@auth
def register_parlour():
    d = request.get_json() or {}
    required = ["name","owner_name","cnic","phone","email","category",
                "address","city","price_range"]
    missing = [k for k in required if not (d.get(k) or "").strip()]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    import re
    if not re.match(r"^\d{5}-\d{7}-\d$", d.get("cnic","").strip()):
        return jsonify({"error": "Invalid CNIC format. Use: 12345-1234567-1"}), 400
    if "@" not in d.get("email",""):
        return jsonify({"error": "Invalid email address"}), 400
    if d.get("photo_count",0) < 3:
        return jsonify({"error": "At least 3 parlour photos are required"}), 400
    if d.get("cnic_doc_count",0) < 1:
        return jsonify({"error": "CNIC document upload is required"}), 400

    c = db()
    # Check for duplicate application from same user for same salon name
    existing = c.execute(
        "SELECT id FROM parlour_applications WHERE submitted_by=? AND name=? AND status='pending'",
        (request.uid, d["name"].strip())
    ).fetchone()
    if existing:
        c.close()
        return jsonify({"error": "You already have a pending application for this salon name."}), 409

    c.execute("""
        INSERT INTO parlour_applications(
            submitted_by, name, owner_name, cnic, phone, email,
            category, description, address, city, area, maps_link,
            price_range, working_hours, services_json,
            photo_count, cnic_doc_count, has_cert, has_health
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            request.uid,
            d.get("name","").strip(),
            d.get("owner_name","").strip(),
            d.get("cnic","").strip(),
            d.get("phone","").strip(),
            d.get("email","").strip(),
            d.get("category",""),
            d.get("description","").strip(),
            d.get("address","").strip(),
            d.get("city","").strip(),
            d.get("area","").strip(),
            d.get("maps_link","").strip(),
            d.get("price_range",""),
            d.get("working_hours",""),
            json.dumps(d.get("services",[])),
            int(d.get("photo_count",0)),
            int(d.get("cnic_doc_count",0)),
            1 if d.get("has_cert") else 0,
            1 if d.get("has_health") else 0,
        )
    )
    c.commit()
    app_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.close()
    return jsonify({
        "submitted": True,
        "application_id": app_id,
        "message": "Your parlour application has been received and is under review.",
        "email": d.get("email","").strip()
    }), 201

@app.route("/api/parlour/my-applications", methods=["GET"])
@auth
def my_parlour_applications():
    c = db()
    rows = c.execute(
        "SELECT id,name,status,submitted_at,review_note FROM parlour_applications WHERE submitted_by=? ORDER BY submitted_at DESC",
        (request.uid,)
    ).fetchall()
    c.close()
    return jsonify({"applications": [dict(r) for r in rows]})


if __name__ == "__main__":
    init_db()
    init_salon_db()
    init_parlour_applications_db()
    print("GlamMatch Sprint 3 — http://localhost:5000")
    app.run(debug=True, port=5000)
