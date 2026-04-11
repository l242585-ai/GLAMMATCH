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
    """)
    c.commit(); c.close()

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
                    "undertone":u["undertone"],"body_type":u["body_type"]})

@app.route("/api/profile", methods=["GET"])
@auth
def profile():
    c = db()
    u = c.execute("SELECT id,name,email,undertone,body_type,created FROM users WHERE id=?",
                  (request.uid,)).fetchone()
    bm = [r["tip_id"] for r in c.execute("SELECT tip_id FROM bookmarks WHERE user_id=?",
                                          (request.uid,)).fetchall()]
    c.close()
    if not u: return jsonify({"error":"Not found"}), 404
    return jsonify({"id":u["id"],"name":u["name"],"email":u["email"],
                    "undertone":u["undertone"],"body_type":u["body_type"],
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
    c = db()
    c.execute("INSERT INTO wardrobe(user_id,filename,category,style_tag) VALUES(?,?,?,?)",
              (request.uid,filename,category,style_tag))
    c.commit()
    item_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.close()
    return jsonify({"id":item_id,"filename":filename,"category":category,"style_tag":style_tag}), 201

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

    tops  = [i for i in items if i["category"] in ("Top","Shirt","Blouse","Jacket")]
    bots  = [i for i in items if i["category"] in ("Bottom","Skirt","Trousers","Jeans","Dress")]
    combo = []
    if tops: combo.append(dict(tops[0]))
    if bots: combo.append(dict(bots[0]))
    if not combo: combo = [dict(items[0]),dict(items[1])]

    outfits = []
    for i in range(min(3, len(items)-1)):
        t = dict(tops[i % len(tops)]) if tops else dict(items[i])
        b = dict(bots[i % len(bots)]) if bots else dict(items[(i+1)%len(items)])
        outfits.append({"items":[t,b],"event":event,
                        "badge":"Perfect Match ✦","hijab_color":hijab_color})

    return jsonify({"outfit":combo,"outfits":outfits,
                    "accessory_tip":tips_map.get(undertone,""),
                    "hijab_color":hijab_color,"badge":"Perfect Match ✦"})

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
    undertone = u["undertone"] if u and u["undertone"] else "neutral"
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
    fs = u["face_shape"] if u and u["face_shape"] else "oval"
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

if __name__ == "__main__":
    init_db()
    print("✅ GlamMatch Sprint 1 — http://localhost:5000")
    app.run(debug=True, port=5000)