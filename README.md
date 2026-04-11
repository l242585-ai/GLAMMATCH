💄 GlamMatch — Personalized Styling & Salon Connector App

Your personal glam stylist, always on.

GlamMatch is an AI-powered web application that provides personalized colour palette recommendations, styling tips, wardrobe outfit suggestions, makeup product recommendations, and face shape analysis — all based on a user's skin undertone, body type, and facial structure. It also connects users with nearby beauty parlours for appointment booking.

👩‍💻 Team Members
NameRoll NumberRoleAyza Ahmed24L-2577Project Lead & Requirements EngineerEman Adil24L-2589Backend & Database DeveloperAnoushay Fatima24L-2585Frontend Developer, UI/UX & QA Tester

🛠️ Tech Stack
LayerTechnologyBackendPython 3.8+, Flask (REST API)FrontendHTML5, CSS3, JavaScript (Single Page App)DatabaseSQLite (auto-created on first run)AuthJWT (JSON Web Tokens, 24-hour expiry)AI / Analysisface-api.js (TinyFaceDetector + FaceLandmark68Net)Version ControlGit & GitHub

📁 Project Structure
GlamMatch/
├── backend/
│   ├── app.py                  ← Flask REST API (all routes, all sprints)
│   ├── models/                 ← face-api.js model files (served at /models/)
│   │   ├── tiny_face_detector_model-shard1
│   │   ├── tiny_face_detector_model-weights_manifest.json
│   │   ├── face_landmark_68_model-shard1
│   │   └── face_landmark_68_model-weights_manifest.json
│   ├── requirements.txt        ← Python dependencies
│   └── .env.example            ← Environment variables template
├── frontend/
│   └── src/
│       └── index.html          ← Full Single Page Application
├── database/
│   ├── schema.sql              ← Database tables (DDL)
│   └── seed.sql                ← Sample test data
├── docs/
│   ├── Iteration_0.docx        ← Project proposal
│   ├── Iteration_1.docx        ← Sprint 1 report
│   ├── Iteration_2.docx        ← Sprint 2 report
│   └── Iteration_3.docx        ← Sprint 3 report
├── erd.png                     ← Entity Relationship Diagram
├── .gitignore
└── README.md

✅ Sprint 1 Features
User StoryFeatureStatusUS-01User Registration & Secure Login✅ CompleteUS-02Undertone Quiz (6 questions with colour swatches)✅ CompleteUS-03Personalized Colour Palette (clothing + makeup)✅ CompleteUS-04Styling Tips + Bookmarks✅ CompleteUS-05Body Type Quiz & Recommendations✅ CompleteUS-06Basic Wardrobe Management✅ Complete

✅ Sprint 2 Features
User StoryFeatureStatusUS-07Photo Upload → Skin Tone Detection (pixel RGB analysis)✅ CompleteUS-08Face Shape Detection via Photo (face-api.js landmarks)✅ CompleteUS-09Manual Face Shape Quiz✅ CompleteUS-10Face Shape Style Suggestions (hairstyle, hijab, earrings)✅ CompleteUS-11Makeup & Clothing Product Recommendations by Undertone✅ CompleteUS-12Product Wishlist✅ CompleteUS-13Event-Based Outfit Generation from Wardrobe✅ CompleteUS-14Style Suggestion Bookmarks✅ Complete

🔧 Sprint 3 — Bug Fixes
The following bugs from Sprint 2 were identified and resolved in Sprint 3:
BugFixWardrobe had no colour fieldAdded colour picker + name input to all wardrobe sections; backend stores color columnOutfit generation returned the same combination for every event typeAdded event-type filtering and randomised selection with deduplicationFace shape photo detection always failedFixed model serving route (/models/) in Flask + added CDN fallback for face-api.js models

🚀 How to Run
Prerequisites

Python 3.8 or higher
pip (Python package manager)
The models/ folder must be inside backend/ (copy the four model files there — see Project Structure above)

Backend Setup
bashcd backend
pip install -r requirements.txt
python app.py
You should see:
✅ GlamMatch — http://localhost:5000
Frontend
The Flask server serves the frontend automatically. Open your browser and go to:
http://localhost:5000

Note on face-api.js models: Place the four model files in backend/models/. Flask serves them at /models/. If the local models are unavailable, the app automatically falls back to the vladmandic CDN, so face detection still works without local files.


🌐 Application Screens
ScreenDescriptionSprintLoginSecure login with email & password1RegisterCreate new account with field validation1HomeLanding page with feature overview and season palette preview1Style Analysis — Skin ToneUpload photo or take quiz → undertone detection + colour palette1–2Style Analysis — Face ShapeUpload selfie or take manual quiz → face shape + style suggestions2Style Analysis — Body Type5-question quiz → body type classification with styling tips1WardrobeAdd clothing items with colour, category & style tag; generate event-based outfits1–3ProductsMakeup & clothing recommendations by undertone; wishlist2ParlourParlour Finder & Booking (Sprint 3 — In Progress)3

🔌 API Endpoints
Auth
MethodEndpointAuthDescriptionPOST/api/register❌Register new userPOST/api/login❌Login, returns JWT tokenGET/api/profile✅Get user profilePOST/api/forgot-password❌Request password resetPOST/api/reset-password❌Reset password with token
Undertone Quiz & Palette
MethodEndpointAuthDescriptionGET/api/quiz/undertone/questions✅Get undertone quiz questionsPOST/api/quiz/undertone/submit✅Submit answers, returns undertone resultGET/api/palette✅Get personalized colour paletteGET/api/tips✅Get styling tips for undertonePOST/api/bookmarks✅Toggle tip bookmark
Body Type Quiz
MethodEndpointAuthDescriptionGET/api/quiz/bodytype/questions✅Get body type quiz questionsPOST/api/quiz/bodytype/submit✅Submit answers, returns body type result
Photo Analysis & Face Shape
MethodEndpointAuthDescriptionPOST/api/photo/save-result✅Save skin tone + face shape from frontend analysisGET/api/face-shape✅Get saved face shape for userGET/api/face-shape/quiz/questions✅Get manual face shape quiz questionsPOST/api/face-shape/quiz/submit✅Submit manual quiz, returns face shape
Style Suggestions
MethodEndpointAuthDescriptionGET/api/style-suggestions✅Get hairstyle/hijab/earring suggestions for face shapePOST/api/bookmarks/style✅Toggle style suggestion bookmark
Wardrobe & Outfits
MethodEndpointAuthDescriptionGET/api/wardrobe✅Get all wardrobe items for userPOST/api/wardrobe✅Add wardrobe item (category, style_tag, color)DELETE/api/wardrobe/<id>✅Delete wardrobe itemPOST/api/wardrobe/outfit✅Generate event-based outfit combinationsPOST/api/wardrobe/favourite✅Save a favourite outfit
Products & Wishlist
MethodEndpointAuthDescriptionGET/api/products✅Get makeup/clothing recommendations by undertoneGET/api/wishlist✅Get user's saved wishlist productsPOST/api/wishlist✅Toggle product in wishlist

🗄️ Database Tables
TableDescriptionSprintusersUser accounts — name, email, password hash, undertone, body type, face shape1quiz_logRecords of all quiz submissions with answers and results1wardrobeClothing items per user — category, style tag, colour1–3bookmarksSaved styling tip IDs per user1photo_analysisSkin tone and face shape results from photo uploads2product_recommendationsMakeup and clothing products seeded by undertone2wishlistUser-saved products from product recommendations2style_suggestionsHairstyle, hijab, and earring suggestions per face shape2style_bookmarksUser-saved style suggestions2

🔒 Security Notes

Passwords are hashed using SHA-256 before storing
Authentication uses JWT tokens with a 24-hour expiry
Never commit the .env file — use .env.example as a template
Privacy option available when uploading photos (keep or delete after analysis)
Existing databases automatically migrate to add new columns (e.g., color on wardrobe) without data loss


📋 Submission Checklist

 Repository set to Public
 All team members have commits
 README.md complete and up to date
 Backend with requirements.txt
 Frontend source code (index.html)
 Database schema.sql and seed.sql
 .gitignore configured
 .env.example (no real secrets committed)
 docs/ folder with all iteration documents (Iteration 0–3)
 models/ folder with face-api.js model files
 ERD diagram (erd.png)
