# 💄 GlamMatch — Personalized Styling & Salon Connector App

> *Your personal glam stylist, always on.*

GlamMatch is an AI-powered web application that provides personalized colour palette recommendations, styling tips, wardrobe outfit suggestions, makeup product recommendations, and face shape analysis — all based on a user's skin undertone, body type, and facial structure. It also connects users with nearby beauty parlours for appointment booking.

---

## 👩‍💻 Team Members

| Name | Roll Number | Role |
|------|------------|------|
| Ayza Ahmed | 24L-2577 | Project Lead & Requirements Engineer |
| Eman Adil | 24L-2589 | Backend & Database Developer |
| Anoushay Fatima | 24L-2585 | Frontend Developer, UI/UX & QA Tester |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.8+, Flask (REST API) |
| **Frontend** | HTML5, CSS3, JavaScript (Single Page App) |
| **Database** | SQLite (auto-created on first run) |
| **Auth** | JWT (JSON Web Tokens, 24-hour expiry) |
| **AI / Analysis** | face-api.js (TinyFaceDetector + FaceLandmark68Net) |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
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
```

---

## ✅ Sprint 1 Features

| User Story | Feature | Status |
|-----------|---------|--------|
| US-01 | User Registration & Secure Login | ✅ Complete |
| US-02 | Undertone Quiz (6 questions with colour swatches) | ✅ Complete |
| US-03 | Personalized Colour Palette (clothing + makeup) | ✅ Complete |
| US-04 | Styling Tips + Bookmarks | ✅ Complete |
| US-05 | Body Type Quiz & Recommendations | ✅ Complete |


---

## ✅ Sprint 2 Features

| User Story | Feature | Status |
|-----------|---------|--------|
| US-06 | Upload selfie and get skin tone / undertone estimate| ✅ Complete |
| US-07 | Detect face shape from uploaded photo	| ✅ Complete |
| US-08 | Receive makeup and clothing product recommendations | ✅ Complete |
| US-09 | Upload wardrobe items and get outfit suggestions	| ✅ Complete |
| US-10 | Get face shape–based style suggestions (hairstyle, hijab & earrings) | ✅ Complete |





---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- The `models/` folder must be inside `backend/` (copy the four model files there — see Project Structure above)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

You should see:

```
✅ GlamMatch — http://localhost:5000
```

### Frontend

The Flask server serves the frontend automatically. Open your browser and go to:

```
http://localhost:5000
```

> **Note on face-api.js models:** Place the four model files in `backend/models/`. Flask serves them at `/models/`. If the local models are unavailable, the app automatically falls back to the vladmandic CDN, so face detection still works without local files.

---

## 🌐 Application Screens

| Screen | Description | Sprint |
|--------|-------------|--------|
| **Login** | Secure login with email & password | 1 |
| **Register** | Create new account with field validation | 1 |
| **Home** | Landing page with feature overview and season palette preview | 1 |
| **Style Analysis — Skin Tone** | Upload photo or take quiz → undertone detection + colour palette | 1–2 |
| **Style Analysis — Face Shape** | Upload selfie or take manual quiz → face shape + style suggestions | 2 |
| **Style Analysis — Body Type** | 5-question quiz → body type classification with styling tips | 1 |
| **Wardrobe** | Add clothing items with colour, category & style tag; generate event-based outfits | 1–3 |
| **Products** | Makeup & clothing recommendations by undertone; wishlist | 2 |
| **Parlour** | Parlour Finder & Booking *(Sprint 3 — In Progress)* | 3 |

---

## 🔌 API Endpoints

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/register` | ❌ | Register new user |
| POST | `/api/login` | ❌ | Login, returns JWT token |
| GET | `/api/profile` | ✅ | Get user profile |
| POST | `/api/forgot-password` | ❌ | Request password reset |
| POST | `/api/reset-password` | ❌ | Reset password with token |

### Undertone Quiz & Palette

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/quiz/undertone/questions` | ✅ | Get undertone quiz questions |
| POST | `/api/quiz/undertone/submit` | ✅ | Submit answers, returns undertone result |
| GET | `/api/palette` | ✅ | Get personalized colour palette |
| GET | `/api/tips` | ✅ | Get styling tips for undertone |
| POST | `/api/bookmarks` | ✅ | Toggle tip bookmark |

### Body Type Quiz

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/quiz/bodytype/questions` | ✅ | Get body type quiz questions |
| POST | `/api/quiz/bodytype/submit` | ✅ | Submit answers, returns body type result |

### Photo Analysis & Face Shape

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/photo/save-result` | ✅ | Save skin tone + face shape from frontend analysis |
| GET | `/api/face-shape` | ✅ | Get saved face shape for user |
| GET | `/api/face-shape/quiz/questions` | ✅ | Get manual face shape quiz questions |
| POST | `/api/face-shape/quiz/submit` | ✅ | Submit manual quiz, returns face shape |

### Style Suggestions

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/style-suggestions` | ✅ | Get hairstyle/hijab/earring suggestions for face shape |
| POST | `/api/bookmarks/style` | ✅ | Toggle style suggestion bookmark |

### Wardrobe & Outfits

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/wardrobe` | ✅ | Get all wardrobe items for user |
| POST | `/api/wardrobe` | ✅ | Add wardrobe item (category, style_tag, color) |
| DELETE | `/api/wardrobe/<id>` | ✅ | Delete wardrobe item |
| POST | `/api/wardrobe/outfit` | ✅ | Generate event-based outfit combinations |
| POST | `/api/wardrobe/favourite` | ✅ | Save a favourite outfit |

### Products & Wishlist

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/products` | ✅ | Get makeup/clothing recommendations by undertone |
| GET | `/api/wishlist` | ✅ | Get user's saved wishlist products |
| POST | `/api/wishlist` | ✅ | Toggle product in wishlist |

---

## 🗄️ Database Tables

| Table | Description | Sprint |
|-------|-------------|--------|
| `users` | User accounts — name, email, password hash, undertone, body type, face shape | 1 |
| `quiz_log` | Records of all quiz submissions with answers and results | 1 |
| `wardrobe` | Clothing items per user — category, style tag, colour | 1–3 |
| `bookmarks` | Saved styling tip IDs per user | 1 |
| `photo_analysis` | Skin tone and face shape results from photo uploads | 2 |
| `product_recommendations` | Makeup and clothing products seeded by undertone | 2 |
| `wishlist` | User-saved products from product recommendations | 2 |
| `style_suggestions` | Hairstyle, hijab, and earring suggestions per face shape | 2 |
| `style_bookmarks` | User-saved style suggestions | 2 |

---

## 🔒 Security Notes

- Passwords are hashed using SHA-256 before storing
- Authentication uses JWT tokens with a 24-hour expiry
- Never commit the `.env` file — use `.env.example` as a template
- Privacy option available when uploading photos (keep or delete after analysis)
- Existing databases automatically migrate to add new columns (e.g., `color` on wardrobe) without data loss

---

## 📋 Submission Checklist

- [x] Repository set to Public
- [x] All team members have commits
- [x] README.md complete and up to date
- [x] Backend with `requirements.txt`
- [x] Frontend source code (`index.html`)
- [x] Database `schema.sql` and `seed.sql`
- [x] `.gitignore` configured
- [x] `.env.example` (no real secrets committed)
- [x] `docs/` folder with all iteration documents (Iteration 0–3)
- [x] `models/` folder with face-api.js model files
- [x] ERD diagram (`erd.png`)
