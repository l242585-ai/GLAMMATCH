# 💄 GlamMatch — Personalized Styling & Parlour Connector

> *Your personal AI beauty stylist — discover your palette, style your wardrobe, and book verified parlours near you.*

GlamMatch is a Flask + JavaScript single-page web application for personalized beauty and styling recommendations. It includes undertone analysis, body type and face shape suggestions, wardrobe outfit generation, product recommendations, and a complete parlour booking workflow with admin verification, CNIC document review, client-parlour chat, booking rules, and role-based notifications.

---

## 👩‍💻 Team Members

| Name | Roll Number | Role |
|------|-------------|------|
| Ayza Ahmed | 24L-2577 | Project Lead & Requirements Engineer |
| Eman Adil | 24L-2589 | Backend & Database Developer |
| Anoushay Fatima | 24L-2585 | Frontend Developer, UI/UX & QA Tester |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.8+, Flask REST API |
| Frontend | HTML5, CSS3, JavaScript single-page app |
| Database | SQLite |
| Authentication | JWT bearer tokens |
| AI / Analysis | face-api.js local model files |
| Storage | SQLite text/BLOB-style base64 document storage for prototype CNIC uploads |

---

## 📁 Project Structure

```text
GLAMMATCH/
├── Backend/
│   ├── app.py              # Flask backend and API routes
│   ├── glammatch.db        # SQLite database; generated/updated locally
│   ├── requirements.txt    # Python dependencies
│   └── env.example         # Optional environment variables
├── Frontend/
│   ├── index.html          # Complete SPA frontend
│   └── models/             # face-api.js model files
├── database/
│   ├── schema.sql          # Updated database schema reference
│   └── seed.sql            # Optional sample data notes/seeds
├── docs/
│   └── api-docs.md         # Updated API documentation
├── .gitignore
└── README.md
```

---

## ✅ Main Functional Modules

### 1. User Authentication

- User registration and login.
- JWT token-based protected routes.
- Forgot/reset password flow.
- Localhost now opens the welcome/login screen first instead of automatically opening a saved session home page.

### 2. Style Analysis

- Undertone quiz and personalized color palette.
- Skin tone and face shape result saving from photo analysis.
- Manual face shape quiz.
- Body type quiz and style recommendations.
- Hairstyle, hijab, and earring suggestions based on face shape.

### 3. Wardrobe and Products

- Add wardrobe items.
- Generate event-based outfit suggestions.
- Save favorite outfits.
- View makeup/clothing product recommendations.
- Add/remove products from wishlist.

### 4. Parlour Portal

The parlour portal now has only two main cards:

1. **Register Your Parlour**
2. **Find Parlours**

The old top-navbar **My Bookings** entry was removed. Client bookings are accessed from the Find Parlours / booking flow.

---

## 🏪 Parlour Registration and Owner Dashboard

### Parlour Registration

A parlour owner can register a parlour with:

- Parlour name
- Owner name
- Phone and email
- Address, city, area
- Services
- Opening time and closing time
- Working days
- Price range
- Description
- CNIC number
- CNIC front upload
- CNIC back upload

### CNIC Verification Flow

- CNIC must contain exactly 13 digits.
- CNIC front/back documents are uploaded during registration.
- New parlours start with `pending` status.
- Admin reviews CNIC documents and approves/rejects the parlour.
- Only `approved` parlours are visible in Find Parlours.

### Owner Dashboard

If the user has already registered a parlour, **Register Your Parlour** opens the owner dashboard instead of showing the registration form again.

Owner dashboard includes:

- Parlour details
- Verification status
- Edit details option
- Bookings received for that parlour
- Owner-side role-based notifications
- Client-parlour chat for active bookings

---

## 🔐 Admin Portal

Admin portal is protected by an admin code.

Default admin code:

```text
12345678
```

Optional environment variable:

```bash
GLAMMATCH_ADMIN_CODE=your_admin_code_here
```

Admin portal capabilities:

- Password/code required every time admin portal is opened.
- View pending, approved, rejected parlours.
- Open CNIC front/back documents in the in-page viewer.
- Approve, reject, or mark parlour pending.
- View all bookings.

---

## 📅 Booking Rules

Clients can book only approved parlours.

Validation checks include:

- Past date/time is blocked.
- Booking more than 90 days in advance is blocked.
- Closed days are blocked.
- Times outside parlour opening/closing hours are blocked.
- Duplicate active booking for the same parlour and exact time slot is blocked.
- Selected service must be offered by that parlour.
- Client name and phone are validated.
- Booking note is limited to 500 characters.

### Cancellation / Rejection Rules

- Client can cancel only pending/confirmed bookings.
- Client cannot cancel within 2 hours of appointment time.
- Parlour can reject only pending/confirmed bookings.
- Parlour cannot reject within 2 hours of appointment time.

### Completion Rule

- Parlour owner cannot manually complete a booking.
- Booking becomes `completed` automatically only after the appointment time passes.
- Once completed/cancelled/rejected, chat and actions close.

---

## 💬 Chat System

- Chat is linked to a specific booking.
- Client and parlour owner can message each other only while the booking is active.
- Chat hides after booking is cancelled, rejected, completed, or appointment time passes.
- Chat uses WhatsApp/Instagram-style message distinction:
  - Current user's messages appear on the right.
  - Other side's messages appear on the left.
  - Labels show `You: Client`, `You: Parlour`, `Client: Name`, or `Parlour`.

---

## 🔔 Notifications

In-app notifications are role-based:

- If the **client cancels**, the **parlour owner** receives a notification.
- If the **parlour rejects**, the **client** receives a notification.
- Client notifications show in My Bookings.
- Owner notifications show in Owner Dashboard.
- Notifications can be marked as read.

---

## 🚀 How to Run

### 1. Install requirements

```bash
cd Backend
pip install -r requirements.txt
```

### 2. Run Flask backend

```bash
python app.py
```

### 3. Open in browser

```text
http://localhost:5000
```

The backend serves the frontend automatically.

---

## 🗄️ Database Notes

- SQLite database is stored as `Backend/glammatch.db`.
- The backend creates missing tables automatically.
- Existing databases are migrated with missing columns where needed.
- Do not commit `glammatch.db` to GitHub because `.gitignore` excludes database files.
- For a clean test, delete `Backend/glammatch.db` and restart the backend.

---

## 🔌 API Documentation

Full updated API documentation is available in:

```text
docs/api-docs.md
```

---

## Suggested Commit Message

```text
Update GlamMatch parlour workflow docs and implement verified booking system
```
