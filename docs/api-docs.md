# GlamMatch API Documentation
## Sprint 1 & 2 — REST API Endpoints

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
- `save_photo` controls whether the image is stored or discarded
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

## Database Tables

| Table | Purpose |
|-------|---------|
| `users` | User accounts with undertone, body_type, face_shape |
| `wardrobe` | Wardrobe items per user |
| `quiz_log` | History of all quiz submissions |
| `bookmarks` | Bookmarked styling tips |
| `photo_analysis` | Results from uploaded photo analysis |
| `product_recommendations` | Seeded product data by undertone |
| `wishlist` | User wishlisted products |
| `style_suggestions` | Seeded hairstyle/hijab/earring suggestions by face shape |
| `style_bookmarks` | Bookmarked style suggestions |
| `password_reset_tokens` | Active password reset tokens with expiry |
