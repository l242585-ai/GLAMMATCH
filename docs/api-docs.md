# GlamMatch API Documentation
## Sprint 1 — REST API Endpoints

**Base URL:** `http://localhost:5000/api`  
**Auth:** Bearer token in `Authorization` header (except register/login)

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

### POST /login
Login existing user.
**Body:**
```json
{ "email": "a@test.com", "password": "test1234" }
```
**Response:**
```json
{ "token": "...", "name": "Anoushay", "undertone": "warm", "body_type": "hourglass" }
```

### GET /profile
Get current user profile. **Requires auth.**
**Response:**
```json
{ "id": 1, "name": "Anoushay", "email": "...", "undertone": "warm", "body_type": "hourglass", "bookmarks": ["w1","w3"] }
```

---

## Undertone Quiz (US-02)

### GET /quiz/undertone/questions
Get all 6 undertone quiz questions. **Requires auth.**

### POST /quiz/undertone/submit
Submit quiz answers. **Requires auth.**
**Body:**
```json
{ "answers": {"1":"a","2":"b","3":"a","4":"b","5":"a","6":"b"} }
```
**Response:**
```json
{ "undertone": "cool", "description": "...", "tips": [...] }
```

---

## Colour Palette (US-03)

### GET /palette
Get personalised colour palette. **Requires auth.**
**Response:**
```json
{ "undertone": "warm", "palette": { "desc": "...", "clothing": {...}, "makeup": {...} } }
```

---

## Styling Tips (US-04)

### GET /tips
Get styling tips for user's undertone. **Requires auth.**

### POST /bookmarks
Toggle bookmark on a tip. **Requires auth.**
**Body:** `{ "tip_id": "w1" }`

---

## Body Type Quiz (US-05)

### GET /quiz/bodytype/questions
Get all 5 body type quiz questions. **Requires auth.**

### POST /quiz/bodytype/submit
Submit body type quiz. **Requires auth.**
**Body:**
```json
{ "answers": {"1":"a","2":"a","3":"c","4":"d","5":"a"} }
```
**Response:**
```json
{ "body_type": "hourglass", "info": { "name":"Hourglass","emoji":"⏳","desc":"...","tips":[...],"avoid":[...] } }
```

---

## Wardrobe (US-08 partial)

### GET /wardrobe — Get all items
### POST /wardrobe — Add item
**Body:** `{ "filename": "top.jpg", "category": "Top", "style_tag": "Casual" }`
### DELETE /wardrobe/<id> — Delete item
### POST /wardrobe/outfit — Generate outfit suggestion
