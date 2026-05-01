# 💄 GlamMatch — Personalized Styling & Salon Connector App

> *Your personal glam stylist, always on.*

GlamMatch is a web application that provides personalized colour palette recommendations, styling tips, wardrobe outfit suggestions, makeup product recommendations, and face shape analysis — all based on a user's skin undertone, body type, and facial structure. It also connects users with nearby beauty parlours for appointment booking, chat, and reviews.

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
├── Backend/
│   ├── app.py                  ← Flask REST API (all routes, all sprints)
│   ├── glammatch.db            ← SQLite database (auto-created on first run)
│   ├── requirements.txt        ← Python dependencies
│   └── env.example             ← Environment variables template
├── Frontend/
│   └── index.html              ← Full Single Page Application
│   └── models/                 ← face-api.js model files (served at /models/)
│       ├── tiny_face_detector_model-shard1
│       ├── tiny_face_detector_model-weights_manifest.json
│       ├── face_landmark_68_model-shard1
│       └── face_landmark_68_model-weights_manifest.json
│   └── images/                 ← Hairstyle, hijab, earring reference images
├── database/
│   ├── schema.sql              ← Database tables DDL (all sprints)
│   └── seed.sql                ← Sample test data (all sprints)
├── docs/
│   ├── api-docs.md             ← Full API documentation
│   ├── report.docs/
│   │   ├── Iteration 0.docx    ← Project proposal
│   │   ├── Iteration 1.docx    ← Sprint 1 report
│   │   ├── Iteration 2.docx    ← Sprint 2 report
│   │   └── Iteration 3.docx    ← Sprint 3 report
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
| US-06 | Upload selfie and get skin tone / undertone estimate | ✅ Complete |
| US-07 | Detect face shape from uploaded photo or manual quiz | ✅ Complete |
| US-08 | Makeup and clothing product recommendations + wishlist | ✅ Complete |
| US-09 | Upload wardrobe items and get event-based outfit suggestions | ✅ Complete |
| US-10 | Face shape–based style suggestions (hairstyle, hijab & earrings) | ✅ Complete |

---

## ✅ Sprint 3 Features

| User Story | Feature | Status |
|-----------|---------|--------|
| US-11 | Find nearby salons with search bar and filters (service, price, category) | ✅ Complete |
| US-12 | View full salon profile with services catalog and reviews | ✅ Complete |
| US-13 | Request appointment booking and track status (Pending / Confirmed / Rejected / Alternate / Completed / Cancelled) | ✅ Complete |
| US-14 | Chat between client and salon (accessible from bookings list and salon profile) | ✅ Complete |
| US-15 | Rate and review salon after appointment is marked completed | ✅ Complete |

---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup

```bash
cd Backend
pip install -r requirements.txt
python app.py
```

You should see:

```
GlamMatch Sprint 3 — http://localhost:5000
```

### Frontend

The Flask server serves the frontend automatically. Open your browser and go to:

```
http://localhost:5000
```

> **Note on face-api.js models:** The four model files are inside `Frontend/models/`. Flask serves them at `/models/`. If the local models are unavailable, the app automatically falls back to the vladmandic CDN, so face detection still works.

> **Note on database:** The SQLite database (`glammatch.db`) is auto-created and seeded with salons, services, and sample data on first run. If you want a fresh database, simply delete `glammatch.db` and restart the app.

---

## 🌐 Application Screens

| Screen | Description | Sprint |
|--------|-------------|--------|
| **Login** | Secure login with email & password | 1 |
| **Register** | Create new account with field validation | 1 |
| **Forgot / Reset Password** | Email-based password reset with expiring token | 1 |
| **Home** | Landing page with feature overview | 1 |
| **Style Analysis — Skin Tone** | Upload photo or take quiz → undertone + colour palette | 1–2 |
| **Style Analysis — Face Shape** | Upload selfie or take manual quiz → face shape + style suggestions | 2 |
| **Style Analysis — Body Type** | 5-question quiz → body type with styling tips | 1 |
| **Wardrobe** | Add clothing items; generate event-based outfit combinations | 2 |
| **Products** | Makeup & clothing recommendations by undertone; wishlist | 2 |
| **Salon Finder** | Search + filter salons by service, price, category; distance badges | 3 |
| **Salon Profile** | Full profile with services catalog, reviews, and chat option | 3 |
| **Book Appointment** | Select service, date/time, add note, submit booking request | 3 |
| **My Bookings** | Track all bookings with status tracker; cancel, accept alternate, mark completed | 3 |
| **Chat** | WhatsApp-style message thread per booking (auto-refreshes every 5s) | 3 |
| **Leave a Review** | 5-star rating + text review after appointment is completed | 3 |

---

## 🔌 API Endpoints

Full documentation is in `docs/api-docs.md`. Summary below:

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/register` | ❌ | Register new user |
| POST | `/api/login` | ❌ | Login, returns JWT token |
| GET | `/api/profile` | ✅ | Get user profile |
| POST | `/api/forgot-password` | ❌ | Request password reset email |
| POST | `/api/reset-password` | ❌ | Reset password with token |

### Undertone Quiz & Palette

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/quiz/undertone/questions` | ✅ | Get undertone quiz questions |
| POST | `/api/quiz/undertone/submit` | ✅ | Submit answers, get undertone result |
| GET | `/api/palette` | ✅ | Get personalized colour palette |
| GET | `/api/tips` | ✅ | Get styling tips for undertone |
| POST | `/api/bookmarks` | ✅ | Toggle tip bookmark |

### Body Type Quiz

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/quiz/bodytype/questions` | ✅ | Get body type quiz questions |
| POST | `/api/quiz/bodytype/submit` | ✅ | Submit answers, get body type result |

### Photo Analysis & Face Shape

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/photo/save-result` | ✅ | Save skin tone + face shape from photo analysis |
| GET | `/api/face-shape` | ✅ | Get saved face shape |
| GET | `/api/face-shape/quiz/questions` | ✅ | Get manual face shape quiz questions |
| POST | `/api/face-shape/quiz/submit` | ✅ | Submit manual quiz, get face shape |

### Style Suggestions

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/style-suggestions` | ✅ | Get hairstyle/hijab/earring suggestions |
| POST | `/api/bookmarks/style` | ✅ | Toggle style suggestion bookmark |

### Wardrobe & Outfits

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/wardrobe` | ✅ | Get all wardrobe items |
| POST | `/api/wardrobe` | ✅ | Add wardrobe item |
| DELETE | `/api/wardrobe/<id>` | ✅ | Delete wardrobe item |
| POST | `/api/wardrobe/outfit` | ✅ | Generate event-based outfit combinations |
| POST | `/api/wardrobe/favourite` | ✅ | Save a favourite outfit |

### Products & Wishlist

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/products` | ✅ | Get makeup/clothing recommendations by undertone |
| GET | `/api/wishlist` | ✅ | Get user's saved wishlist |
| POST | `/api/wishlist` | ✅ | Toggle product in wishlist |

### Salon Connector — Sprint 3

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/salons` | ✅ | List salons with filters (category, price_range, service_type) |
| GET | `/api/salons/<id>` | ✅ | Full salon profile with services and reviews |
| GET | `/api/salons/<id>/reviews` | ✅ | Get all reviews for a salon |
| GET | `/api/bookings` | ✅ | Get all bookings for current user |
| POST | `/api/bookings` | ✅ | Create new booking request |
| GET | `/api/bookings/<id>` | ✅ | Get a single booking |
| PUT | `/api/bookings/<id>` | ✅ | Update booking status |
| GET | `/api/chat/<booking_id>` | ✅ | Get chat messages for a booking |
| POST | `/api/chat/<booking_id>` | ✅ | Send a chat message |
| POST | `/api/reviews` | ✅ | Submit a salon review |

---

## 🗄️ Database Tables

| Table | Description | Sprint |
|-------|-------------|--------|
| `users` | User accounts — name, email, password hash, undertone, body type, face shape | 1 |
| `quiz_log` | All quiz submissions with answers and results | 1 |
| `wardrobe` | Clothing items per user — category, style tag, colour | 1 |
| `bookmarks` | Saved styling tip IDs per user | 1 |
| `password_reset_tokens` | Active password reset tokens with expiry | 1 |
| `photo_analysis` | Skin tone and face shape results from photo uploads | 2 |
| `product_recommendations` | Makeup and clothing products seeded by undertone | 2 |
| `wishlist` | User-saved products from recommendations | 2 |
| `style_suggestions` | Hairstyle, hijab, earring suggestions per face shape | 2 |
| `style_bookmarks` | User-saved style suggestions | 2 |
| `salons` | Salon profiles — name, address, category, price range, rating | 3 |
| `salon_services` | Services per salon — type, price range, duration | 3 |
| `bookings` | Appointment requests with status tracking | 3 |
| `chat_messages` | Chat thread messages per booking | 3 |
| `reviews` | Post-appointment ratings and reviews | 3 |

---

## 🔒 Security Notes

- Passwords are hashed using SHA-256 before storing
- Authentication uses JWT tokens with a 24-hour expiry
- Never commit the `.env` file — use `env.example` as a template
- Privacy option available when uploading photos (keep or delete after analysis)
- Existing databases automatically migrate to add new columns without data loss

---

## 📋 Submission Checklist

- [x] Repository set to Public
- [x] All team members have commits
- [x] README.md complete and up to date
- [x] Backend with `requirements.txt`
- [x] Frontend source code (`index.html`)
- [x] Database `schema.sql` and `seed.sql`
- [x] API documentation (`docs/api-docs.md`)
- [x] `.gitignore` configured
- [x] `env.example` (no real secrets committed)
- [x] `docs/` folder with all iteration documents (Iteration 0–3)
- [x] `Frontend/models/` folder with face-api.js model files