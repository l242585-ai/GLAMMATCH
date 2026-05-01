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
  "id": 1,
  "name": "Anoushay",
  "email": "a@test.com",
  "undertone": "warm",
  "body_type": "hourglass",
  "face_shape": "oval",
  "created": "2024-01-01 12:00:00",
  "bookmarks": ["w1", "w3"]
}
```

---

## Forgot / Reset Password

### POST /forgot-password
Request a password reset link. Does NOT require auth.
**Body:**
```json
{ "email": "a@test.com" }
```
**Response:**
```json
{ "message": "If that email is registered, a reset link has been sent." }
```
**Notes:**
- Always returns success to prevent email enumeration
- Reset link is sent to the user's email via Gmail SMTP
- Link format: `http://localhost:5000/?reset_token=<token>`
- Token expires after 1 hour
- Token is stored in the `password_reset_tokens` database table (persists across Flask restarts)

---

### POST /reset-password
Set a new password using a reset token. Does NOT require auth.
**Body:**
```json
{ "token": "abc123...", "password": "newpass1" }
```
**Response:**
```json
{ "message": "Password reset successfully" }
```
**Validation:**
- Token and password are required
- Password must be 8+ characters with at least one number
- Token must be valid and not expired

---

## Undertone Quiz (US-02)

### GET /quiz/undertone/questions
Get all 6 undertone quiz questions. **Requires auth.**
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
        { "id": "c", "t": "A mix of both", "score": { "neutral": 2 } }
      ]
    }
  ],
  "total": 6
}
```

---

### POST /quiz/undertone/submit
Submit quiz answers. **Requires auth.**
**Body:**
```json
{ "answers": { "1": "a", "2": "b", "3": "a", "4": "b", "5": "a", "6": "b" } }
```
**Response:**
```json
{ "undertone": "cool", "description": "Your cool undertone radiates...", "tips": [...] }
```
**Result values:** `warm` | `cool` | `neutral`

---

## Colour Palette (US-03)

### GET /palette
Get personalised colour palette based on saved undertone. **Requires auth.**
**Response:**
```json
{
  "undertone": "warm",
  "palette": {
    "desc": "Your warm undertone glows with earthy, golden tones.",
    "clothing": {
      "rec": [{ "n": "Terracotta", "h": "#C45C3A" }],
      "avoid": [{ "n": "Icy Blue", "h": "#A5C8E1", "r": "Washes out warm skin" }]
    },
    "makeup": {
      "rec": [{ "n": "Peachy Blush", "h": "#FFAE87" }],
      "avoid": [{ "n": "Cool Pink Lip", "h": "#FF69B4", "r": "Creates ashy effect" }]
    }
  }
}
```
**Error (no undertone saved):** `400 { "error": "Complete the undertone quiz first" }`

---

## Styling Tips (US-04)

### GET /tips
Get styling tips for user's undertone. **Requires auth.**
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
Toggle bookmark on a styling tip. **Requires auth.**
**Body:** `{ "tip_id": "w1" }`
**Response:** `{ "bookmarked": true }` or `{ "bookmarked": false }`

---

## Body Type Quiz (US-05)

### GET /quiz/bodytype/questions
Get all 5 body type quiz questions. **Requires auth.**
**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "q": "Stand in front of a mirror. How do your shoulders compare to your hips?",
      "opts": [
        { "id": "a", "t": "Shoulders are clearly broader", "score": { "inverted_triangle": 3 } }
      ]
    }
  ],
  "total": 5
}
```

---

### POST /quiz/bodytype/submit
Submit body type quiz answers. **Requires auth.**
**Body:**
```json
{ "answers": { "1": "a", "2": "a", "3": "c", "4": "d", "5": "a" } }
```
**Response:**
```json
{
  "body_type": "hourglass",
  "info": {
    "name": "Hourglass",
    "emoji": "⏳",
    "desc": "Balanced shoulders and hips with a well-defined waist.",
    "tips": ["Wrap dresses", "High-waisted bottoms"],
    "avoid": ["Shapeless boxy cuts"]
  }
}
```
**Result values:** `hourglass` | `pear` | `apple` | `rectangle` | `inverted_triangle`

---

## Photo Analysis (US-06 & US-07) — Sprint 2

### POST /photo/save-result
Save skin tone and/or face shape detected from an uploaded photo. **Requires auth.**
Called automatically by the frontend after face-api.js analysis.
**Body:**
```json
{
  "undertone": "warm",
  "skin_tone": "medium",
  "face_shape": "oval",
  "swatch_color": "#C8906A",
  "save_photo": true
}
```
**Response:**
```json
{ "saved": true, "undertone": "warm", "face_shape": "oval" }
```
**Notes:**
- `face_shape` is optional — skin tone can be saved without it
- `save_photo`: `true` = save photo record, `false` = analyze then discard (privacy mode)
- Skin tone values: `light` | `medium` | `deep` | `rich`

---

### GET /face-shape
Get the saved face shape for the current user. **Requires auth.**
**Response:**
```json
{
  "face_shape": "oval",
  "description": "Slightly wider at cheekbones — the most versatile shape."
}
```
**Face shape values:** `oval` | `round` | `square` | `heart` | `oblong`

---

## Face Shape Quiz (US-07) — Sprint 2

### GET /face-shape/quiz/questions
Get the 4 manual face shape quiz questions. **Requires auth.**
**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "q": "Is your forehead wider than your jaw?",
      "opts": [
        { "id": "a", "t": "Yes, noticeably wider" },
        { "id": "b", "t": "About the same" },
        { "id": "c", "t": "Jaw is wider" }
      ]
    }
  ]
}
```

---

### POST /face-shape/quiz/submit
Submit face shape quiz answers. **Requires auth.**
**Body:**
```json
{ "answers": { "1": "b", "2": "b", "3": "b", "4": "a" } }
```
**Response:**
```json
{ "face_shape": "oval" }
```

---

## Style Suggestions (US-10) — Sprint 2

### GET /style-suggestions
Get hairstyle, hijab and earring suggestions based on saved face shape. **Requires auth.**

Optional query param: `?category=hairstyle` | `hijab` | `earring`

**Response:**
```json
{
  "face_shape": "oval",
  "suggestions": [
    {
      "id": 1,
      "face_shape": "oval",
      "category": "hairstyle",
      "suggestion_name": "Any Length Works",
      "description": "Oval faces suit virtually all hairstyles..."
    },
    {
      "id": 4,
      "face_shape": "oval",
      "category": "hijab",
      "suggestion_name": "Wrap Style Hijab",
      "description": "A simple wrap or Turkish style flatters your oval shape..."
    },
    {
      "id": 7,
      "face_shape": "oval",
      "category": "earring",
      "suggestion_name": "Statement Drops",
      "description": "Long drop earrings or chandeliers look stunning..."
    }
  ]
}
```
**Returns empty suggestions array if no face shape is saved yet.**

---

### POST /bookmarks/style
Toggle bookmark on a style suggestion. **Requires auth.**
**Body:** `{ "suggestion_id": 1 }`
**Response:** `{ "bookmarked": true }` or `{ "bookmarked": false }`

---

## Products (US-08) — Sprint 2

### GET /products
Get product recommendations based on user's undertone. **Requires auth.**

Optional query param: `?category=makeup` | `clothing`

**Response (undertone saved):**
```json
{
  "undertone": "warm",
  "products": [
    {
      "id": 1,
      "category": "makeup",
      "sub_category": "foundation",
      "undertone": "warm",
      "brand": "L'Oreal",
      "product_name": "True Match Foundation",
      "shade_name": "W3 Golden Beige",
      "swatch_color": "#C8906A",
      "product_link": "https://www.loreal-paris.com"
    }
  ]
}
```
**Response (no undertone saved):**
```json
{ "products": [], "undertone": null, "quiz_required": true }
```

---

## Wishlist (US-08) — Sprint 2

### GET /wishlist
Get all wishlisted products for the current user. **Requires auth.**
**Response:**
```json
{
  "wishlist": [
    {
      "wishlist_id": 1,
      "id": 3,
      "product_name": "Matte Lipstick",
      "brand": "MAC",
      "swatch_color": "#B7604A",
      "product_link": "https://www.maccosmetics.com"
    }
  ]
}
```

---

### POST /wishlist
Add or remove a product from wishlist. **Requires auth.**
**Body:** `{ "product_id": 3 }`
**Response:** `{ "saved": true }` or `{ "saved": false }`

---

## Wardrobe (US-09) — Sprint 2

### GET /wardrobe
Get all wardrobe items for the current user. **Requires auth.**
**Response:**
```json
{
  "items": [
    { "id": 1, "category": "Top", "style_tag": "Casual", "color": "red", "filename": "item.jpg", "added": "2024-01-01 12:00:00" }
  ]
}
```

---

### POST /wardrobe
Add a new wardrobe item. **Requires auth.**
**Body:**
```json
{ "filename": "top.jpg", "category": "Top", "style_tag": "Casual", "color": "red" }
```
**Category values:** `Top` | `Shirt` | `Blouse` | `Kurta` | `Sweater` | `Jacket` | `Coat` | `Abaya` | `Trousers` | `Jeans` | `Pants` | `Leggings` | `Skirt` | `Dress` | `Shalwar` | `Hijab` | `Dupatta` | `Bag` | `Shoes` | `Belt` | `Scarf`

**Style tag values:** `Casual` | `Formal` | `Party` | `Traditional` | `Sports`

**Response:**
```json
{ "id": 1, "filename": "top.jpg", "category": "Top", "style_tag": "Casual", "color": "red" }
```

---

### DELETE /wardrobe/\<id\>
Delete a wardrobe item by ID. **Requires auth.**
**Response:** `{ "deleted": true }`

---

### POST /wardrobe/outfit
Generate outfit combinations from wardrobe items. **Requires auth.**
**Body:** `{ "event_type": "casual" }`
**Event type values:** `casual` | `formal` | `party` | `traditional` | `sports`

**Response:**
```json
{
  "outfit": [
    { "id": 1, "category": "Top", "style_tag": "Casual", "color": "red" }
  ],
  "outfits": [
    {
      "items": [
        { "id": 1, "category": "Top", "style_tag": "Casual", "color": "red" },
        { "id": 2, "category": "Jeans", "style_tag": "Casual", "color": "blue" }
      ],
      "event": "casual",
      "badge": "Casual Chic ✦",
      "hijab_color": "#C9956C"
    }
  ],
  "accessory_tip": "Pair with gold accessories",
  "hijab_color": "#C9956C",
  "badge": "Casual Chic ✦"
}
```
**Error (less than 2 items):** `400 { "error": "Add at least 2 wardrobe items to generate an outfit" }`

---

### POST /wardrobe/favourite
Save a favourite outfit combination. **Requires auth.**
**Body:** `{ "item_ids": [1, 2, 3], "event_type": "casual" }`
**Response:** `{ "message": "Outfit saved ⭐" }`

---

---

# Sprint 3 — Salon Connector Platform

## Salon Discovery (US-11)

### GET /salons
Get list of all salons with optional filters. **Requires auth.**

**Query Parameters (all optional):**

| Param | Values | Description |
|---|---|---|
| `category` | `women` \| `men` \| `unisex` \| `all` | Filter by salon category |
| `price_range` | `budget` \| `mid` \| `premium` | Filter by price range |
| `service_type` | `makeup` \| `hair` \| `nails` \| `skincare` \| `bridal` | Filter by service type offered |

**Example:** `GET /api/salons?category=women&price_range=mid&service_type=hair`

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
      "working_hours": "10:00 AM – 9:00 PM",
      "phone": "+92-300-1234567",
      "description": "Premium beauty studio specializing in bridal and editorial makeup."
    }
  ],
  "count": 1
}
```
**Notes:**
- Results are ordered by rating descending
- `category=all` or omitting `category` returns all salons
- When `service_type` is provided, only salons that have at least one service of that type are returned

---

## Salon Profile (US-12)

### GET /salons/\<salon_id\>
Get full salon profile including services and recent reviews. **Requires auth.**

**Response:**
```json
{
  "salon": {
    "id": 1,
    "name": "Glamour Studio",
    "address": "12 Mall Road, Lahore",
    "category": "women",
    "price_range": "mid",
    "rating": 4.7,
    "review_count": 38,
    "working_hours": "10:00 AM – 9:00 PM",
    "phone": "+92-300-1234567",
    "description": "Premium beauty studio specializing in bridal and editorial makeup."
  },
  "services": [
    {
      "id": 1,
      "salon_id": 1,
      "service_name": "Bridal Makeup",
      "service_type": "bridal",
      "price_min": 8000,
      "price_max": 15000,
      "duration_min": 180
    }
  ],
  "reviews": [
    {
      "id": 1,
      "user_id": 2,
      "user_name": "Eman",
      "salon_id": 1,
      "booking_id": 3,
      "rating": 5,
      "review_text": "Amazing experience!",
      "created_at": "2024-05-01 14:30:00"
    }
  ]
}
```
**Error:** `404 { "error": "Salon not found" }`

---

## Appointment Booking (US-13)

### GET /bookings
Get all bookings for the current user. **Requires auth.**

**Response:**
```json
{
  "bookings": [
    {
      "id": 1,
      "user_id": 1,
      "salon_id": 2,
      "salon_name": "The Beauty Lounge",
      "service_id": 5,
      "service_name": "Hair Cut & Blow Dry",
      "datetime": "2024-05-10T14:00",
      "status": "pending",
      "note": "I prefer a female stylist",
      "alt_time": null,
      "created_at": "2024-05-01 10:00:00"
    }
  ]
}
```

---

### POST /bookings
Create a new booking request. **Requires auth.**
**Body:**
```json
{
  "salon_id": 2,
  "service_id": 5,
  "datetime": "2024-05-10T14:00",
  "note": "I prefer a female stylist"
}
```
**Validation:**
- `salon_id` and `datetime` are required
- `service_id` and `note` are optional
- `salon_id` must exist in the database

**Response:**
```json
{ "booking_id": 1, "status": "pending" }
```
**Error:** `404 { "error": "Salon not found" }`

---

### GET /bookings/\<booking_id\>
Get a single booking by ID. **Requires auth.**

**Response:**
```json
{
  "booking": {
    "id": 1,
    "salon_name": "The Beauty Lounge",
    "service_name": "Hair Cut & Blow Dry",
    "datetime": "2024-05-10T14:00",
    "status": "confirmed",
    "note": "I prefer a female stylist",
    "alt_time": null
  }
}
```
**Error:** `404 { "error": "Booking not found" }`

---

### PUT /bookings/\<booking_id\>
Update booking status (used by salon to confirm/reject or user to cancel/complete). **Requires auth.**
**Body:**
```json
{ "status": "confirmed", "alt_time": "" }
```
**Status values:**

| Value | Description |
|---|---|
| `confirmed` | Salon accepts the booking (or user accepts an alternate slot) |
| `rejected` | Salon rejects the booking |
| `alternate` | Salon proposes a new time — include `alt_time` in body |
| `completed` | Appointment has taken place — user can now leave a review |
| `cancelled` | User cancels the booking |

**Body for alternate slot:**
```json
{ "status": "alternate", "alt_time": "2024-05-11T10:00" }
```

**Response:**
```json
{ "booking_id": 1, "status": "alternate" }
```

---

## Chat (US-14)

### GET /chat/\<booking_id\>
Get all chat messages for a booking. **Requires auth.**

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "booking_id": 1,
      "sender_type": "user",
      "message": "Hi, can I confirm my appointment for Friday?",
      "sent_at": "2024-05-01 10:15:00"
    },
    {
      "id": 2,
      "booking_id": 1,
      "sender_type": "salon",
      "message": "Yes, your appointment is confirmed for Friday at 2 PM!",
      "sent_at": "2024-05-01 10:20:00"
    }
  ]
}
```
**Notes:**
- Messages are returned in ascending order (oldest first)
- `sender_type` is either `user` or `salon`
- Chat is linked to a specific booking — a booking must exist before chatting

---

### POST /chat/\<booking_id\>
Send a message in a booking chat thread. **Requires auth.**
**Body:**
```json
{ "message": "Can I reschedule to Saturday?", "sender_type": "user" }
```
**sender_type values:** `user` | `salon`

**Response:**
```json
{ "message_id": 3, "sent": true }
```
**Error:** `400 { "error": "message is required" }`

---

## Reviews (US-15)

### POST /reviews
Submit a rating and review for a salon after an appointment. **Requires auth.**
**Body:**
```json
{
  "salon_id": 2,
  "booking_id": 1,
  "rating": 5,
  "review_text": "Absolutely loved the experience!"
}
```
**Validation:**
- `salon_id` and `rating` are required
- `rating` must be an integer between 1 and 5
- `booking_id` is optional but recommended to prevent duplicate reviews
- A user cannot review the same booking twice

**Response:**
```json
{ "saved": true, "rating": 5 }
```
**Errors:**
- `400` — missing salon_id or invalid rating
- `409` — `{ "error": "You have already reviewed this appointment" }`

**Notes:**
- After a review is saved, the salon's average `rating` and `review_count` are automatically recalculated
- Salon cannot edit or delete user reviews

---

### GET /salons/\<salon_id\>/reviews
Get all reviews for a specific salon. **Requires auth.**

**Response:**
```json
{
  "reviews": [
    {
      "id": 1,
      "user_id": 2,
      "user_name": "Eman",
      "salon_id": 1,
      "booking_id": 3,
      "rating": 5,
      "review_text": "Amazing experience!",
      "created_at": "2024-05-01 14:30:00"
    }
  ]
}
```
**Notes:**
- Results are ordered by `created_at` descending (newest first)

---

---

## Database Tables

### Sprint 1 & 2 Tables

| Table | Purpose |
|---|---|
| `users` | User accounts with undertone, body_type, face_shape |
| `wardrobe` | Wardrobe items per user |
| `quiz_log` | History of all quiz submissions (undertone, bodytype, outfit_fav) |
| `bookmarks` | Bookmarked styling tips per user |
| `photo_analysis` | Results from uploaded photo analysis (skin_tone, undertone, face_shape, photo_saved) |
| `product_recommendations` | Seeded product data (makeup & clothing) by undertone |
| `wishlist` | User wishlisted products |
| `style_suggestions` | Seeded hairstyle / hijab / earring suggestions by face shape |
| `style_bookmarks` | Bookmarked style suggestions per user |
| `password_reset_tokens` | Active password reset tokens with expiry timestamp |

### Sprint 3 Tables

| Table | Purpose |
|---|---|
| `salons` | Salon profiles — name, address, category, price_range, rating, working_hours, phone, description |
| `salon_services` | Services offered by each salon — name, type, price range, duration |
| `bookings` | Appointment requests — links user to salon + service, stores status and alt_time |
| `chat_messages` | Chat messages per booking — sender_type (user/salon), message, timestamp |
| `reviews` | Post-appointment reviews — rating (1–5), review_text, linked to user + salon + booking |

### Booking Status Flow

```
[User submits] → pending
                    ↓
        ┌───────────┼───────────┐
     confirmed   rejected   alternate (salon proposes new time)
        ↓                       ↓
     completed            confirmed (user accepts)
        ↓                       ↓
    [Review enabled]         completed
                                ↓
                           [Review enabled]

At any point while pending or confirmed → cancelled (user cancels)
```