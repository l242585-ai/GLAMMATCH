# 💄 GlamMatch — Personalized Styling & Salon Connector App

> *Your personal glam stylist, always on.*

GlamMatch is an AI-powered web application that provides personalized colour palette recommendations, styling tips, and wardrobe outfit suggestions based on a user's skin undertone and body type. It also connects users with nearby beauty parlours for appointment booking.

---

## 👩‍💻 Team Members

| Name | Roll Number | Role |
|------|------------|------|
| Ayza Ahmed | 24L-2577 | Project Lead & Requirements Engineer |
| Eman Adil | 24L-2589 | Backend & Database Developer |
| Anoushay Fatima | 24L-2585 | Frontend Developer & UI/UX & QA Tester |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask (REST API) |
| **Frontend** | HTML, CSS, JavaScript (Single Page App) |
| **Database** | SQLite (auto-created on first run) |
| **Auth** | JWT (JSON Web Tokens) |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
GlamMatch/
├── backend/
│   ├── app.py              ← Flask REST API (all routes)
│   ├── requirements.txt    ← Python dependencies
│   └── .env.example        ← Environment variables template
├── frontend/
│   └── src/
│       └── index.html      ← Full Single Page Application
├── database/
│   ├── schema.sql          ← Database tables (DDL)
│   ├── seed.sql            ← Sample test data
│   └── erd.png             ← Entity Relationship Diagram
├── docs/
│   ├── Iteration_1.docx    ← Sprint 1 report
│   └── api-docs.md         ← API documentation
├── .gitignore
└── README.md
```

---

## ✅ Sprint 1 Features

| User Story | Feature | Status |
|-----------|---------|--------|
| US-01 | User Registration & Secure Login | ✅ Complete |
| US-02 | Undertone Quiz (6 questions) | ✅ Complete |
| US-03 | Personalized Colour Palette | ✅ Complete |
| US-04 | Styling Tips + Bookmarks | ✅ Complete |
| US-05 | Body Type Quiz & Recommendations | ✅ Complete |
| US-08 | Basic Wardrobe Management | ✅ Complete |

---

# How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

You should see:
```
✅ GlamMatch Sprint 1 — http://localhost:5000
```

### Frontend
The Flask server serves the frontend automatically.
Open your browser and go to:
```
http://localhost:5000
```

---

## 🌐 Application Screens (Sprint 1)

| Screen | Description |
|--------|-------------|
| **Login** | Secure login with email & password |
| **Register** | Create new account with validation |
| **Home** | Landing page with features overview |
| **Style Analysis** | Skin tone detection & undertone quiz |
| **Wardrobe** | Upload & manage clothing items |

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/register` | ❌ | Register new user |
| POST | `/api/login` | ❌ | Login, returns JWT token |
| GET | `/api/profile` | ✅ | Get user profile |
| GET | `/api/quiz/undertone/questions` | ✅ | Get undertone quiz questions |
| POST | `/api/quiz/undertone/submit` | ✅ | Submit undertone quiz |
| GET | `/api/palette` | ✅ | Get personalized colour palette |
| GET | `/api/tips` | ✅ | Get styling tips |
| POST | `/api/bookmarks` | ✅ | Toggle tip bookmark |
| GET | `/api/quiz/bodytype/questions` | ✅ | Get body type quiz questions |
| POST | `/api/quiz/bodytype/submit` | ✅ | Submit body type quiz |
| GET | `/api/wardrobe` | ✅ | Get wardrobe items |
| POST | `/api/wardrobe` | ✅ | Add wardrobe item |
| DELETE | `/api/wardrobe/<id>` | ✅ | Delete wardrobe item |
| POST | `/api/wardrobe/outfit` | ✅ | Generate outfit suggestion |

---

## 🗄️ Database Tables

| Table | Description |
|-------|-------------|
| `users` | Stores user accounts, undertone & body type |
| `quiz_log` | Records quiz answers and results |
| `wardrobe` | Stores clothing items per user |
| `bookmarks` | Stores saved styling tips per user |

---

## 🔒 Security Notes

- Passwords are hashed using SHA-256 before storing
- Authentication uses JWT tokens (24-hour expiry)
- Never commit `.env` file — use `.env.example` as template
- Privacy option available for uploaded photos (keep/delete)

---

## 📋 Submission Checklist

- [x] Repository set to Public
- [x] All team members have commits
- [x] README.md complete
- [x] Backend with requirements.txt
- [x] Frontend source code
- [x] Database schema.sql and seed.sql
- [x] .gitignore configured
- [x] .env.example (no real secrets committed)
- [x] docs/ folder with iteration document
