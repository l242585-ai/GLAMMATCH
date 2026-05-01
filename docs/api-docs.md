# GlamMatch API Documentation
## Sprint 1, 2 & 3 — REST API Endpoints

**Base URL:** `http://localhost:5000/api`
**Auth:** Bearer token in `Authorization` header (except register, login, forgot-password, reset-password)

---

## Auth Endpoints

### POST /register
Register a new user.
**Body:**
```json
{ "name": "Anoushay", "email": "a@test.com", "password": "test1234" }
```
**Response:**
```json
{ "token": "...", "name": "Anoushay" }
```
**Validation:**
- Name, email and password are all required
- Email must contain @
- Password must be 8+ characters with at least one number

---

### POST /login
Login existing user.
**Body:**
```json
{ "email": "a@test.com", "password": "test1234" }
```
**Response:**
```json
{ "token": "...", "name": "Anoushay", "undertone": "warm", "body_type": "hourglass", "face_shape": "oval" }
```

---

### GET /profile
Get current user profile. **Requires auth.**
**Response:**
```json
{
  "id": 1, "name": "Anoushay", "email": "a@test.com",
  "undertone": "warm", "body_type": "hourglass", "face_shape": "oval",
  "created": "2024-01-01 12:00:00", "bookmarks": ["w1", "w3"]
}
```

---

## Forgot / Reset Password

### POST /forgot-password
Request a password reset link. Does NOT require auth.
**Body:** `{ "email": "a@test.com" }`
**Response:** `{ "message": "If that email is registered, a reset link has been sent." }`
**Notes:**
- Always returns success to prevent email enumeration
- Token expires after 1 hour

---

### POST /reset-password
Set a new password using a reset token. Does NOT require auth.
**Body:** `{ "token": "abc123...", "password": "newpass1" }`
**Response:** `{ "message": "Password reset successfully" }`

---

## Undertone Quiz (US-02)

### GET /quiz/undertone/questions
Get all 6 undertone quiz questions. **Requires auth.**

### POST /quiz/undertone/submit
Submit quiz answers. **Requires auth.**
**Body:** `{ "answers": { "1": "a", "2": "b", "3": "a", "4": "b", "5": "a", "6": "b" } }`
**Response:** `{ "undertone": "cool", "description": "...", "tips": [...] }`
**Result values:** `warm` | `cool` | `neutral`

---

## Colour Palette (US-03)

### GET /palette
Get personalised colour palette based on saved undertone. **Requires auth.**
**Error (no undertone):** `400 { "error": "Complete the undertone quiz first" }`

---

## Styling Tips (US-04)

### GET /tips
Get styling tips for user's undertone. **Requires auth.**

### POST /bookmarks
Toggle bookmark on a styling tip. **Requires auth.**
**Body:** `{ "tip_id": "w1" }`
**Response:** `{ "bookmarked": true }` or `{ "bookmarked": false }`

---

## Body Type Quiz (US-05)

### GET /quiz/bodytype/questions
Get all 5 body type quiz questions. **Requires auth.**

### POST /quiz/bodytype/submit
Submit body type answers. **Requires auth.**
**Body:** `{ "answers": { "1": "a", "2": "a", "3": "c", "4": "d", "5": "a" } }`
**Result values:** `hourglass` | `pear` | `apple` | `rectangle` | `inverted_triangle`

---

## Photo Analysis (US-06 & US-07)

### POST /photo/save-result
Save skin tone and face shape from photo analysis. **Requires auth.**
**Body:**
```json
{
  "undertone": "warm", "skin_tone": "medium",
  "face_shape": "oval", "swatch_color": "#C8906A", "save_photo": true
}
```
**Notes:** `save_photo: false` = privacy mode — analyze then discard

### GET /face-shape
Get saved face shape. **Requires auth.**
**Face shape values:** `oval` | `round` | `square` | `heart` | `oblong`

### GET /face-shape/quiz/questions
Get 4 manual face shape quiz questions. **Requires auth.**

### POST /face-shape/quiz/submit
Submit face shape quiz. **Requires auth.**
**Body:** `{ "answers": { "1": "b", "2": "b", "3": "b", "4": "a" } }`

---

## Style Suggestions (US-10)

### GET /style-suggestions
Get hairstyle/hijab/earring suggestions for face shape. **Requires auth.**
Optional: `?category=hairstyle` | `hijab` | `earring`

### POST /bookmarks/style
Toggle style suggestion bookmark. **Requires auth.**
**Body:** `{ "suggestion_id": 1 }`

---

## Products & Wishlist (US-08)

### GET /products
Get recommendations by undertone. **Requires auth.**
Optional: `?category=makeup` | `clothing`

### GET /wishlist
Get user's wishlist. **Requires auth.**

### POST /wishlist
Toggle product in wishlist. **Requires auth.**
**Body:** `{ "product_id": 3 }`

---

## Wardrobe & Outfits (US-09)

### GET /wardrobe
Get all wardrobe items. **Requires auth.**

### POST /wardrobe
Add wardrobe item. **Requires auth.**
**Body:** `{ "filename": "top.jpg", "category": "Top", "style_tag": "Casual", "color": "red" }`

### DELETE /wardrobe/\<id\>
Delete wardrobe item. **Requires auth.**

### POST /wardrobe/outfit
Generate event-based outfit combinations. **Requires auth.**
**Body:** `{ "event_type": "casual" }`
**Event types:** `casual` | `formal` | `party` | `traditional` | `sports`

### POST /wardrobe/favourite
Save a favourite outfit. **Requires auth.**
**Body:** `{ "item_ids": [1, 2, 3] }`

---

---

# Sprint 3 — Salon Connector Platform

## Salon Discovery (US-11)

### GET /salons
Get list of salons with optional filters. **Requires auth.**

**Query Parameters (all optional):**

| Param | Values | Description |
|---|---|---|
| `category` | `women` \| `men` \| `unisex` \| `all` | Filter by salon category |
| `price_range` | `budget` \| `mid` \| `premium` | Filter by price range |
| `service_type` | `makeup` \| `hair` \| `nails` \| `skincare` \| `bridal` | Filter by service type |

**Response:**
```json
{
  "salons": [
    {
      "id": 1,
      "name": "Glamour Studio",
      "address": "12 Mall Road, Lahore",
      "category": "women",
      "price_range": "mid",
      "rating": 4.7,
      "review_count": 38,
      "working_hours": "10:00 AM - 9:00 PM",
      "phone": "+92-300-1234567",
      "description": "Premium beauty studio...",
      "latitude": 31.5620,
      "longitude": 74.3578
    }
  ],
  "count": 1
}
```

**Notes:**
- `latitude` and `longitude` are returned so the frontend can calculate real distance using the Haversine formula
- Frontend sorts salons nearest-first when user grants location permission
- Results ordered by rating when location is not available

---

## Salon Profile (US-12)

### GET /salons/\<salon_id\>
Full salon profile with services and reviews. **Requires auth.**

**Response:**
```json
{
  "salon": { "id": 1, "name": "Glamour Studio", "latitude": 31.5620, "longitude": 74.3578, "..." : "..." },
  "services": [
    { "id": 1, "service_name": "Bridal Makeup", "service_type": "bridal", "price_min": 8000, "price_max": 15000, "duration_min": 180 }
  ],
  "reviews": [
    { "id": 1, "user_name": "Eman", "rating": 5, "review_text": "Amazing!", "created_at": "2024-05-01 14:30:00" }
  ]
}
```

---

## Appointment Booking (US-13)

### GET /bookings
Get all bookings for current user. **Requires auth.**

**Note — Auto-Complete Logic:**
Every time this endpoint is called, the backend checks if any `confirmed` booking's `datetime` has already passed. If so, it automatically updates the status to `completed`. This means the user does not need to manually mark an appointment as done — it completes itself once the time passes.

**Response:**
```json
{
  "bookings": [
    {
      "id": 1,
      "salon_name": "The Beauty Lounge",
      "service_name": "Hair Cut & Blow Dry",
      "datetime": "2024-05-10T14:00",
      "status": "confirmed",
      "note": "I prefer a female stylist",
      "alt_time": null
    }
  ]
}
```

---

### POST /bookings
Create a new booking request. **Requires auth.**
**Body:**
```json
{ "salon_id": 2, "service_id": 5, "datetime": "2024-05-10T14:00", "note": "Optional note" }
```
**Response:** `{ "booking_id": 1, "status": "pending" }`

---

### GET /bookings/\<booking_id\>
Get a single booking. **Requires auth.**

---

### PUT /bookings/\<booking_id\>
Update booking status. **Requires auth.**
**Body:** `{ "status": "confirmed" }` or `{ "status": "alternate", "alt_time": "2024-05-11T10:00" }`

**Status values:**

| Value | Who sets it | Description |
|---|---|---|
| `confirmed` | Salon / User | Salon accepts, or user accepts an alternate slot |
| `rejected` | Salon | Salon rejects the booking |
| `alternate` | Salon | Salon proposes a new time — include `alt_time` |
| `completed` | Auto / User | Set automatically when appointment datetime passes, or manually by user |
| `cancelled` | User | User cancels — **only allowed if 2+ hours before appointment** |

**Cancellation Policy:**
- If the appointment is less than 2 hours away, `cancelled` status will be rejected
- **Error:** `400 { "error": "Cancellation not allowed. Appointment is in 1.3 hour(s). You can only cancel at least 2 hours before the appointment time.", "hours_left": 1.3 }`
- Frontend also checks this before sending the request and shows a lock badge instead of the cancel button

---

## Chat (US-14)

### GET /chat/\<booking_id\>
Get all chat messages for a booking. **Requires auth.**
**Notes:** Messages ordered oldest first. `sender_type` is `user` or `salon`.

### POST /chat/\<booking_id\>
Send a message. **Requires auth.**
**Body:** `{ "message": "Is parking available?", "sender_type": "user" }`
**Response:** `{ "message_id": 3, "sent": true }`

---

## Reviews (US-15)

### POST /reviews
Submit a review after appointment. **Requires auth.**
**Body:**
```json
{ "salon_id": 2, "booking_id": 1, "rating": 5, "review_text": "Loved it!" }
```
**Notes:**
- Only one review per booking allowed
- Review button only appears once booking status is `completed`
- Salon average rating is recalculated automatically after each review

**Errors:**
- `400` — missing salon_id or invalid rating (must be 1–5)
- `409` — `{ "error": "You have already reviewed this appointment" }`

### GET /salons/\<salon_id\>/reviews
Get all reviews for a salon. **Requires auth.**

---

---

## Database Tables

### Sprint 1 & 2

| Table | Purpose |
|---|---|
| `users` | Accounts — name, email, password hash, undertone, body_type, face_shape |
| `wardrobe` | Clothing items per user |
| `quiz_log` | All quiz submissions |
| `bookmarks` | Saved styling tip IDs |
| `password_reset_tokens` | Active reset tokens with expiry |
| `photo_analysis` | Results from photo uploads |
| `product_recommendations` | Seeded products by undertone |
| `wishlist` | User-saved products |
| `style_suggestions` | Hairstyle/hijab/earring suggestions by face shape |
| `style_bookmarks` | User-saved style suggestions |

### Sprint 3

| Table | Key Columns | Purpose |
|---|---|---|
| `salons` | `latitude`, `longitude` | Salon profiles with GPS coordinates for distance |
| `salon_services` | `service_type`, `price_min`, `price_max` | Services per salon |
| `bookings` | `status`, `datetime`, `alt_time` | Appointments with full status tracking |
| `chat_messages` | `sender_type`, `booking_id` | Chat thread per booking |
| `reviews` | `rating`, `UNIQUE(user_id, booking_id)` | One review per appointment |

---

## Booking Status Flow

```
User submits → [pending]
                   |
       ┌───────────┼────────────┐
  [confirmed]  [rejected]  [alternate] ← salon proposes new time
       |                       |
       |              User accepts → [confirmed]
       |                       |
       └───────────┬───────────┘
                   |
            datetime passes
            (auto by backend)
                   ↓
            [completed]
                   ↓
            Review button appears

Cancel rules:
- pending or confirmed → [cancelled]  only if 2+ hours before appointment
- Less than 2 hours → BLOCKED (frontend badge + backend 400 error)
```

---

## Location & Distance (US-11)

The frontend uses the browser `Geolocation API` to get the user's real GPS coordinates, then calculates the distance to each salon using the **Haversine formula** (straight-line distance in km).

```
User clicks "Use My Location"
        ↓
navigator.geolocation.getCurrentPosition()
        ↓
Real lat/lng obtained
        ↓
haversine(userLat, userLng, salon.latitude, salon.longitude)
        ↓
Salons sorted nearest → farthest
Real "X.X km away" badge shown on each card
```

**No external API is used** — distance is calculated entirely in the browser using the coordinates stored in the database.