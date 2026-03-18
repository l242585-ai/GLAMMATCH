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
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            email     TEXT UNIQUE NOT NULL,
            password  TEXT NOT NULL,
            undertone TEXT,
            body_type TEXT,
            created   TEXT DEFAULT(datetime('now'))
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
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER NOT NULL,
            type     TEXT NOT NULL,
            answers  TEXT NOT NULL,
            result   TEXT NOT NULL,
            taken    TEXT DEFAULT(datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS bookmarks(
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tip_id  TEXT NOT NULL,
            UNIQUE(user_id,tip_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
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
    {"id":1,"q":"What colour are the veins on your inner wrist?",
     "opts":[{"id":"a","t":"Bluish / purple","score":{"cool":2}},
             {"id":"b","t":"Greenish","score":{"warm":2}},
             {"id":"c","t":"Blue-green mix","score":{"neutral":2}}]},
    {"id":2,"q":"How does your skin react to sun exposure?",
     "opts":[{"id":"a","t":"I burn easily, rarely tan","score":{"cool":2}},
             {"id":"b","t":"I tan easily, rarely burn","score":{"warm":2}},
             {"id":"c","t":"Sometimes burn then tan","score":{"neutral":2}}]},
    {"id":3,"q":"Which jewellery flatters you most?",
     "opts":[{"id":"a","t":"Silver looks best","score":{"cool":2}},
             {"id":"b","t":"Gold looks best","score":{"warm":2}},
             {"id":"c","t":"Both look equally good","score":{"neutral":2}}]},
    {"id":4,"q":"Which neutral shades do you prefer wearing?",
     "opts":[{"id":"a","t":"Bright white, navy, grey, black","score":{"cool":2}},
             {"id":"b","t":"Off-white, camel, brown, olive","score":{"warm":2}},
             {"id":"c","t":"Ivory, beige, taupe","score":{"neutral":2}}]},
    {"id":5,"q":"What overall tone do you notice in your skin?",
     "opts":[{"id":"a","t":"Pink, rosy or bluish","score":{"cool":2}},
             {"id":"b","t":"Yellow, peachy or golden","score":{"warm":2}},
             {"id":"c","t":"Mix of pink and yellow","score":{"neutral":2}}]},
    {"id":6,"q":"Which colours make you look most vibrant?",
     "opts":[{"id":"a","t":"Jewel tones: sapphire, emerald, ruby","score":{"cool":2}},
             {"id":"b","t":"Earth tones: terracotta, coral, rust","score":{"warm":2}},
             {"id":"c","t":"Muted tones: dusty rose, sage, mauve","score":{"neutral":2}}]},
]

def classify_ut(answers):
    s={"warm":0,"cool":0,"neutral":0}
    for qid,oid in answers.items():
        q=next((x for x in UT_QUESTIONS if str(x["id"])==str(qid)),None)
        if q:
            o=next((x for x in q["opts"] if x["id"]==oid),None)
            if o:
                for k,v in o["score"].items(): s[k]+=v
    return max(s,key=s.get)

# ── Body type quiz ───────────────────────────────────────────────
BT_QUESTIONS = [
    {"id":1,"q":"How do your shoulders compare to your hips?",
     "opts":[{"id":"a","t":"Shoulders wider than hips","score":{"inverted_triangle":3,"hourglass":1}},
             {"id":"b","t":"Roughly equal","score":{"rectangle":2,"hourglass":1}},
             {"id":"c","t":"Hips wider than shoulders","score":{"pear":3,"hourglass":1}}]},
    {"id":2,"q":"How defined is your waist?",
     "opts":[{"id":"a","t":"Very defined — clearly smaller","score":{"hourglass":3}},
             {"id":"b","t":"Slightly defined","score":{"pear":1,"inverted_triangle":1}},
             {"id":"c","t":"Not very defined — straight","score":{"rectangle":3}},
             {"id":"d","t":"Wider midsection","score":{"apple":3}}]},
    {"id":3,"q":"Where do you gain weight first?",
     "opts":[{"id":"a","t":"Hips, thighs and bottom","score":{"pear":3}},
             {"id":"b","t":"Stomach and midsection","score":{"apple":3}},
             {"id":"c","t":"Evenly all over","score":{"rectangle":2,"hourglass":1}},
             {"id":"d","t":"Upper body and bust","score":{"inverted_triangle":3}}]},
    {"id":4,"q":"Which area is the widest on your body?",
     "opts":[{"id":"a","t":"Shoulders / bust","score":{"inverted_triangle":3}},
             {"id":"b","t":"Hips / thighs","score":{"pear":3}},
             {"id":"c","t":"Midsection / waist","score":{"apple":3}},
             {"id":"d","t":"All roughly similar","score":{"rectangle":2,"hourglass":1}}]},
    {"id":5,"q":"Describe your hips / bottom shape:",
     "opts":[{"id":"a","t":"Full and rounded","score":{"pear":2,"hourglass":2}},
             {"id":"b","t":"Fairly flat","score":{"rectangle":2,"inverted_triangle":2}},
             {"id":"c","t":"Weight in tummy, not hips","score":{"apple":3}}]},
]

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
    scores = {k:0 for k in BT_INFO}
    for qid,oid in answers.items():
        q = next((x for x in BT_QUESTIONS if str(x["id"])==str(qid)),None)
        if q:
            o = next((x for x in q["opts"] if x["id"]==oid),None)
            if o:
                for k,v in o["score"].items(): scores[k]+=v
    result = max(scores,key=scores.get)
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
    """Generate a simple outfit combination from wardrobe items."""
    c = db()
    items = c.execute("SELECT * FROM wardrobe WHERE user_id=?", (request.uid,)).fetchall()
    ut = c.execute("SELECT undertone FROM users WHERE id=?", (request.uid,)).fetchone()
    c.close()
    if len(items) < 2:
        return jsonify({"error":"Add at least 2 wardrobe items to generate an outfit"}), 400
    tops  = [i for i in items if i["category"] in ("Top","Shirt","Blouse","Jacket")]
    bots  = [i for i in items if i["category"] in ("Bottom","Skirt","Trousers","Jeans")]
    combo = []
    if tops:  combo.append(dict(tops[0]))
    if bots:  combo.append(dict(bots[0]))
    if not combo: combo = [dict(items[0]), dict(items[1])]
    tip = ""
    if ut and ut["undertone"]:
        tips_map = {"warm":"Pair with gold accessories","cool":"Pair with silver accessories","neutral":"Mix metals freely"}
        tip = tips_map.get(ut["undertone"],"")
    return jsonify({"outfit":combo,"accessory_tip":tip})

# ── Serve frontend ────────────────────────────────────────────────
@app.route("/", defaults={"p":""})
@app.route("/<path:p>")
def serve(p):
    fp = os.path.join(app.static_folder, p)
    if p and os.path.exists(fp):
        return send_from_directory(app.static_folder, p)
    return send_from_directory(app.template_folder, "index.html")

if __name__ == "__main__":
    init_db()
    print("✅ GlamMatch Sprint 1 — http://localhost:5000")
    app.run(debug=True, port=5000)
