# GlamMatch — Full API Documentation
# All Sprints (1, 2 & 3)

Base URL: `http://localhost:5000/api`
Auth header: `Authorization: Bearer <token>`

---

# Sprint 1 — Auth, Quiz, Palette, Tips, Wardrobe

---

## US-01: Authentication

### POST /register
Create a new user account. **No auth required.**

**Body:**
```json
{ "name": "Ayza", "email": "ayza@example.com", "password": "test1234" }
```

**Validation:**
- All fields required
- Email must contain `@`
- Password: 8+ characters, at least one number

**Response:** `201 { "token": "...", "name": "Ayza" }`

**Errors:** `400` missing fields / weak password — `409` email already registered

---

### POST /login
Login and receive a JWT token. **No auth required.**

**Body:**
```json
{ "email": "ayza@example.com", "password": "test1234" }
```

**Response:**
```json
{ "token": "...", "name": "Ayza", "undertone": "warm", "body_type": "hourglass", "face_shape": "oval" }
```

**Error:** `401` incorrect email or password

---

### GET /profile
Get the logged-in user's profile including saved bookmarks. **Requires auth.**

**Response:**
```json
{
  "id": 1, "name": "Ayza", "email": "ayza@example.com",
  "undertone": "warm", "body_type": "hourglass", "face_shape": "oval",
  "created": "2025-01-01 10:00:00", "bookmarks": ["w1", "w3"]
}
```

---

### POST /forgot-password
Request a password reset email. **No auth required.**

**Body:** `{ "email": "ayza@example.com" }`

**Response:** `{ "message": "If that email is registered, a reset link has been sent." }`

**Notes:**
- Sends HTML email with reset link valid for 1 hour
- Always returns same message whether email exists or not (security)

---

### POST /reset-password
Set a new password using the reset token. **No auth required.**

**Body:** `{ "token": "...", "password": "newpass1" }`

**Validation:** Password must be 8+ characters with at least one number

**Response:** `{ "message": "Password reset successfully" }`

**Errors:** `400` invalid/expired token — `400` weak password

---

## US-02: Undertone Quiz

### GET /quiz/undertone/questions
Get the 6 undertone quiz questions with options and scores. **Requires auth.**

**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "q": "Look at the inner side of your wrist...",
      "opts": [
        { "id": "a", "t": "Pinkish or reddish", "score": { "cool": 2 } },
        { "id": "b", "t": "Yellowish or golden", "score": { "warm": 2 } },
        { "id": "c", "t": "A mix of both",       "score": { "neutral": 2 } }
      ]
    }
  ],
  "total": 6
}
```

---

### POST /quiz/undertone/submit
Submit undertone quiz answers and get result. **Requires auth.**

**Body:** `{ "answers": { "1": "a", "2": "b", "3": "a", "4": "b", "5": "c", "6": "a" } }`

**Response:**
```json
{ "undertone": "warm", "description": "Your warm undertone glows with earthy, golden tones.", "tips": [...] }
```

**Notes:**
- Result saved to `users.undertone` and logged in `quiz_log`
- Possible values: `warm` | `cool` | `neutral`

---

## US-03: Colour Palette

### GET /palette
Get personalized colour palette for the logged-in user's undertone. **Requires auth.**

**Response:**
```json
{
  "undertone": "warm",
  "palette": {
    "desc": "Your warm undertone glows with earthy, golden tones.",
    "clothing": {
      "rec":   [{ "n": "Terracotta", "h": "#C45C3A" }],
      "avoid": [{ "n": "Icy Blue",   "h": "#A5C8E1", "r": "Washes out warm skin" }]
    },
    "makeup": {
      "rec":   [{ "n": "Peachy Blush", "h": "#FFAE87" }],
      "avoid": [{ "n": "Cool Pink Lip", "h": "#FF69B4", "r": "Creates ashy effect" }]
    }
  }
}
```

**Error:** `400` undertone quiz not yet completed

---

## US-04: Styling Tips & Bookmarks

### GET /tips
Get styling tips for the user's undertone. **Requires auth.**

**Response:**
```json
{
  "tips": [
    { "id": "w1", "cat": "Clothing", "emoji": "👗", "tip": "Opt for earth tones..." }
  ]
}
```

---

### POST /bookmarks
Toggle a styling tip bookmark. **Requires auth.**

**Body:** `{ "tip_id": "w1" }`

**Response:** `{ "bookmarked": true }` or `{ "bookmarked": false }`

---

## US-05: Body Type Quiz

### GET /quiz/bodytype/questions
Get the 5 body type quiz questions. **Requires auth.**

**Response:** `{ "questions": [...], "total": 5 }`

---

### POST /quiz/bodytype/submit
Submit body type quiz answers. **Requires auth.**

**Body:** `{ "answers": { "1": "b", "2": "a", "3": "d", "4": "c", "5": "d" } }`

**Response:**
```json
{
  "body_type": "hourglass",
  "info": {
    "name": "Hourglass", "emoji": "⏳",
    "desc": "Balanced shoulders and hips with a well-defined waist.",
    "tips": ["Wrap dresses highlight your curves"],
    "avoid": ["Shapeless boxy cuts"]
  }
}
```

**Notes:** Result saved to `users.body_type` and logged in `quiz_log`

---

## US-08 (partial): Wardrobe

### GET /wardrobe
Get all wardrobe items for the logged-in user. **Requires auth.**

**Response:** `{ "items": [{ "id": 1, "filename": "top1.jpg", "category": "Top", "style_tag": "Casual", "color": "terracotta", "added": "..." }] }`

---

### POST /wardrobe
Add a clothing item. **Requires auth.**

**Body:** `{ "filename": "top1.jpg", "category": "Top", "style_tag": "Casual", "color": "terracotta" }`

**Response:** `201 { "id": 1, "filename": "top1.jpg", "category": "Top", "style_tag": "Casual", "color": "terracotta" }`

---

### DELETE /wardrobe/\<item_id\>
Delete a wardrobe item. **Requires auth.**

**Response:** `{ "deleted": true }`

---

### POST /wardrobe/outfit
Generate event-based outfit combinations. **Requires auth.**

**Body:** `{ "event_type": "casual" }` — options: `casual` | `formal` | `party` | `traditional` | `sports`

**Response:**
```json
{
  "outfits": [
    { "items": [...], "event": "casual", "badge": "Casual Chic ✦", "hijab_color": "#C9956C" }
  ],
  "accessory_tip": "Pair with gold accessories",
  "hijab_color": "#C9956C",
  "badge": "Casual Chic ✦"
}
```

**Error:** `400` fewer than 2 wardrobe items

---

### POST /wardrobe/favourite
Save a favourite outfit. **Requires auth.**

**Body:** `{ "item_ids": [1, 3] }`

**Response:** `{ "message": "Outfit saved ⭐" }`

---

---

# Sprint 2 — Photo Analysis, Products, Style Suggestions

---

## US-06 & US-07: Photo Analysis & Face Shape

### POST /photo/save-result
Save skin tone, undertone and face shape results from face-api.js. **Requires auth.**

**Body:**
```json
{
  "undertone": "warm", "skin_tone": "medium",
  "face_shape": "oval", "save_photo": false, "swatch_color": "#C8A882"
}
```

**Response:** `{ "saved": true, "undertone": "warm", "face_shape": "oval" }`

**Notes:** Updates `users.undertone` and `users.face_shape`; logs to `photo_analysis`

---

### GET /face-shape
Get the user's saved face shape. **Requires auth.**

**Response:** `{ "face_shape": "oval", "description": "Slightly wider at cheekbones — the most versatile shape." }`

Possible values: `oval` | `round` | `square` | `heart` | `oblong`

---

### GET /face-shape/quiz/questions
Get the 4 manual face shape quiz questions. **Requires auth.**

**Response:** `{ "questions": [...] }`

---

### POST /face-shape/quiz/submit
Submit manual face shape quiz. **Requires auth.**

**Body:** `{ "answers": { "1": "b", "2": "a", "3": "b", "4": "a" } }`

**Response:** `{ "face_shape": "oval" }`

---

## US-08: Products & Wishlist

### GET /products
Get makeup and clothing recommendations by undertone. **Requires auth.**

**Query:** `?category=makeup` or `?category=clothing` (optional)

**Response:**
```json
{
  "undertone": "warm",
  "products": [
    {
      "id": 1, "category": "makeup", "sub_category": "foundation",
      "brand": "L'Oreal", "product_name": "True Match Foundation",
      "shade_name": "W3 Golden Beige", "swatch_color": "#C8906A",
      "product_link": "https://www.loreal-paris.com"
    }
  ]
}
```

**Notes:** Returns `{ "quiz_required": true }` if undertone quiz not done

---

### GET /wishlist
Get user's saved products. **Requires auth.**

**Response:** `{ "wishlist": [{ "wishlist_id": 1, "id": 3, "product_name": "..." }] }`

---

### POST /wishlist
Toggle a product in the wishlist. **Requires auth.**

**Body:** `{ "product_id": 3 }`

**Response:** `{ "saved": true }` or `{ "saved": false }`

---

## US-10: Style Suggestions & Bookmarks

### GET /style-suggestions
Get style suggestions for the user's face shape. **Requires auth.**

**Query:** `?category=hairstyle` | `?category=hijab` | `?category=earring` (optional)

**Response:**
```json
{
  "face_shape": "oval",
  "suggestions": [
    { "id": 1, "face_shape": "oval", "category": "hairstyle",
      "suggestion_name": "Side-Swept Bangs", "description": "..." }
  ]
}
```

---

### POST /bookmarks/style
Toggle a style suggestion bookmark. **Requires auth.**

**Body:** `{ "suggestion_id": 1 }`

**Response:** `{ "bookmarked": true }` or `{ "bookmarked": false }`

---

---

# Sprint 3 — Parlour Portal

All Parlour Portal endpoints require auth except `/api/parlour/stats`.

---

## PP-01: Register a Parlour

### POST /parlour/register
Submit parlour for admin review. **Requires auth.**

**Required fields:** `name`, `owner`, `phone`, `address`, `city`

**Optional:** `email`, `area`, `services` (array), `open_time`, `close_time`, `days`, `cnic`, `business_type`, `price_min`, `price_max`, `description`

**Response:** `201 { "message": "Parlour registration submitted for review.", "parlour_id": 1 }`

**Notes:**
- Phone stored in `parlours.phone` at registration — automatically sent to clients in chat
- Status starts as `pending` until admin approves

---

## PP-02: List Approved Parlours

### GET /parlour/list
Get all approved parlours. **Requires auth.**

**Query:** `?city=Lahore` (optional)

**Response:** `{ "parlours": [...], "count": 6 }`

**Notes:** Only `status = 'approved'` returned. Ordered by `rating DESC`.

---

## PP-03: Get Single Parlour

### GET /parlour/\<parlour_id\>
Full parlour detail including phone. **Requires auth.**

**Response:** `{ "parlour": { "id": 1, "name": "Rosé Beauty Lounge", "phone": "0311-1234567", ... } }`

**Error:** `404` not found

---

## PP-04: Book an Appointment

### POST /parlour/booking
Create a booking. **Requires auth.**

**Required:** `parlour_id`, `parlour_name`, `service`, `datetime`, `client_name`, `client_phone`

**Optional:** `note`

**Response:** `201 { "booking_id": 5, "status": "pending" }`

**Notes:** `user_id` saved from auth token — enables cross-session persistence

---

## PP-05: My Bookings

### GET /parlour/my-bookings
Get all bookings for logged-in user. **Requires auth.**

**Response:**
```json
{
  "bookings": [
    {
      "id": 5, "parlour_id": 1, "parlour_name": "Rosé Beauty Lounge",
      "service": "Bridal Makeup", "datetime": "2025-06-15T14:00",
      "client_name": "Ayza", "status": "pending", "created_at": "..."
    }
  ]
}
```

**Notes:** Ordered by `created_at DESC`. Called on every page load to restore bookings after re-login.

---

## PP-05b: Cancel a Booking

### POST /parlour/booking/\<booking_id\>/cancel
Cancel a booking. **Requires auth.**

**Response:** `{ "cancelled": true }`

**Errors:**

| Code | Reason |
|---|---|
| `404` | Booking not found or belongs to another user |
| `400` | Booking status is not `pending` or `confirmed` |
| `400` | Appointment is within 2 hours — cancellation blocked |

**2-hour rule error response:**
```json
{
  "error": "Cannot cancel — your appointment is in 1.3 hour(s). Cancellation is not allowed within 2 hours of the booking time.",
  "hours_left": 1.3
}
```

**Notes:**
- Frontend also checks the 2-hour rule before calling this endpoint and shows a toast error to the user
- On success, booking `status` is updated to `cancelled` in DB — the booking remains visible in My Bookings with a Cancelled badge

---

## PP-06: Automated Chat Bot (General)

### POST /parlour/chat
GlamMatch general landing-page chatbot. **Requires auth.**

**Body:** `{ "message": "How do I register my salon?", "parlour_id": 1 }`

**`parlour_id` optional** — when given, fetches parlour phone from DB and appends to reply:
> 📞 For further queries, you can contact the parlour directly at: 0311-1234567

**Response:** `{ "reply": "...", "parlour_phone": "0311-1234567" }`

**Rule-based triggers:**

| Keywords | Reply topic |
|---|---|
| `register`, `list`, `owner`, `partner` | How to register a parlour |
| `book`, `appointment`, `reserve` | How to book |
| `price`, `cost`, `rate`, `pkr`, `fee` | Pricing |
| `bridal`, `wedding`, `dulhan` | Bridal services |
| `location`, `near`, `city`, `lahore` | City coverage |
| `hour`, `open`, `timing`, `time` | Operating hours |
| `hi`, `hello`, `hey`, `salam` | Greeting |
| *(anything else)* | General help |

**Important:** This endpoint is for the **general chatbot only**. The per-booking chat (`/parlour/booking-chat/<id>`) does NOT call this — it generates contextual replies locally to avoid irrelevant "how to book" instructions inside a chat where the booking already exists.

---

## PP-07: Per-Booking Chat Thread

### GET /parlour/booking-chat/\<booking_id\>
Get all messages for a booking's chat thread. **Requires auth.**

**Response:** `{ "messages": [{ "id": 1, "booking_id": 5, "message": "...", "reply": "...", "sent_at": "..." }] }`

**Error:** `404` booking not found or belongs to another user

---

### POST /parlour/booking-chat/\<booking_id\>
Send a message in a booking chat thread. **Requires auth.**

**Body:** `{ "message": "Is there parking?" }`

**Response:** `201 { "message_id": 3, "sent": true }`

**Notes:** Frontend generates the reply locally based on message context:
- "cancel" → cancel instructions
- "confirm/status" → current booking status
- "reschedule/change" → reschedule instructions
- "price/cost/pkr" → contact parlour for pricing
- anything else → "will get back to you" + parlour phone number

---

## PP-Stats: Public Stats

### GET /parlour/stats
Landing page counters. **No auth required.**

**Response:** `{ "registered_parlours": 6, "cities": 8, "clients": "12K+", "avg_rating": 4.8 }`

---

---

## Database Tables Summary

### Sprint 1

| Table | Key Columns | Purpose |
|---|---|---|
| `users` | `id`, `email`, `undertone`, `body_type`, `face_shape` | User accounts |
| `wardrobe` | `user_id FK`, `category`, `style_tag`, `color` | Clothing items per user |
| `quiz_log` | `user_id FK`, `type`, `answers`, `result` | All quiz submissions |
| `bookmarks` | `user_id FK`, `tip_id` | Saved tip IDs — UNIQUE(user_id, tip_id) |
| `password_reset_tokens` | `token PK`, `user_id FK`, `expires` | Reset tokens — 1 hour expiry |

### Sprint 2

| Table | Key Columns | Purpose |
|---|---|---|
| `photo_analysis` | `user_id FK`, `skin_tone`, `undertone`, `face_shape` | Photo / face-shape quiz results |
| `product_recommendations` | `category`, `sub_category`, `undertone` | Seeded products by undertone |
| `wishlist` | `user_id FK`, `product_id FK` | Saved products — UNIQUE(user_id, product_id) |
| `style_suggestions` | `face_shape`, `category`, `suggestion_name` | Hairstyle/hijab/earring suggestions |
| `style_bookmarks` | `user_id FK`, `suggestion_id FK` | Saved suggestions — UNIQUE(user_id, suggestion_id) |

### Sprint 3

| Table | Key Columns | Purpose |
|---|---|---|
| `parlours` | `phone`, `status` | Parlour profiles; phone sent to clients via chat |
| `parlour_bookings` | `user_id FK`, `parlour_id FK`, `status` | Appointments; `user_id` enables cross-session persistence |
| `parlour_chat_log` | `booking_id FK`, `message`, `reply` | Chat messages per booking thread |