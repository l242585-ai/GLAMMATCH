# GlamMatch API Documentation

**Base URL:** `http://localhost:5000/api`  
**Frontend URL:** `http://localhost:5000`  
**Auth:** Protected user routes require a JWT bearer token:

```http
Authorization: Bearer <token>
```

Admin routes require the admin code either in JSON body, query string, or header:

```http
X-Admin-Code: 12345678
```

Default admin code:

```text
12345678
```

---

## 1. Authentication

### POST `/register`

Register a new user.

**Body**

```json
{
  "name": "Ayza Ahmed",
  "email": "ayza@example.com",
  "password": "test1234"
}
```

**Response**

```json
{
  "token": "jwt-token",
  "name": "Ayza Ahmed"
}
```

**Validation**

- Name is required.
- Email must contain `@`.
- Password must be at least 8 characters and include a number.

---

### POST `/login`

Login existing user.

**Body**

```json
{
  "email": "ayza@example.com",
  "password": "test1234"
}
```

**Response**

```json
{
  "token": "jwt-token",
  "name": "Ayza Ahmed",
  "undertone": "warm",
  "body_type": "hourglass",
  "face_shape": "oval"
}
```

---

### GET `/profile`

Get current logged-in user profile. **Requires auth.**

---

## 2. Password Reset

### POST `/forgot-password`

Request password reset.

**Body**

```json
{
  "email": "ayza@example.com"
}
```

**Response**

```json
{
  "message": "If that email is registered, a reset link has been sent."
}
```

---

### POST `/reset-password`

Reset password using token.

**Body**

```json
{
  "token": "reset-token",
  "password": "newpass1"
}
```

---

## 3. Undertone, Palette, and Tips

### GET `/quiz/undertone/questions`

Returns undertone quiz questions. **Requires auth.**

### POST `/quiz/undertone/submit`

Submit undertone answers. **Requires auth.**

**Body**

```json
{
  "answers": {
    "1": "a",
    "2": "b",
    "3": "a",
    "4": "b",
    "5": "a",
    "6": "b"
  }
}
```

**Result values**

```text
warm | cool | neutral
```

### GET `/palette`

Returns saved user's color palette. **Requires auth.**

### GET `/tips`

Returns styling tips for saved undertone. **Requires auth.**

### POST `/bookmarks`

Toggle a styling tip bookmark. **Requires auth.**

**Body**

```json
{
  "tip_id": "w1"
}
```

---

## 4. Body Type Quiz

### GET `/quiz/bodytype/questions`

Returns body type quiz questions. **Requires auth.**

### POST `/quiz/bodytype/submit`

Submit body type quiz answers. **Requires auth.**

**Result values**

```text
hourglass | pear | apple | rectangle | inverted_triangle
```

---

## 5. Photo Analysis and Face Shape

### POST `/photo/save-result`

Save skin tone, undertone, and face shape result from frontend photo analysis. **Requires auth.**

**Body**

```json
{
  "undertone": "warm",
  "skin_tone": "medium",
  "face_shape": "oval",
  "swatch_color": "#C8906A",
  "save_photo": false
}
```

### GET `/face-shape`

Get saved face shape. **Requires auth.**

### GET `/face-shape/quiz/questions`

Get manual face shape quiz questions. **Requires auth.**

### POST `/face-shape/quiz/submit`

Submit manual face shape quiz. **Requires auth.**

---

## 6. Style Suggestions

### GET `/style-suggestions`

Get hairstyle, hijab, or earring suggestions based on saved face shape. **Requires auth.**

Optional query:

```text
?category=hairstyle
?category=hijab
?category=earring
```

### POST `/bookmarks/style`

Toggle a style suggestion bookmark. **Requires auth.**

**Body**

```json
{
  "suggestion_id": 1
}
```

---

## 7. Products and Wishlist

### GET `/products`

Get product recommendations by saved undertone. **Requires auth.**

Optional query:

```text
?category=makeup
?category=clothing
```

### GET `/wishlist`

Get logged-in user's wishlist. **Requires auth.**

### POST `/wishlist`

Toggle product in wishlist. **Requires auth.**

**Body**

```json
{
  "product_id": 3
}
```

---

## 8. Wardrobe and Outfits

### GET `/wardrobe`

Get all wardrobe items. **Requires auth.**

### POST `/wardrobe`

Add wardrobe item. **Requires auth.**

**Body**

```json
{
  "filename": "top.jpg",
  "category": "Top",
  "style_tag": "Casual",
  "color": "red"
}
```

### DELETE `/wardrobe/<item_id>`

Delete wardrobe item. **Requires auth.**

### POST `/wardrobe/outfit`

Generate event-based outfit combinations. **Requires auth.**

**Body**

```json
{
  "event_type": "casual"
}
```

### POST `/wardrobe/favourite`

Save a favourite outfit. **Requires auth.**

**Body**

```json
{
  "item_ids": [1, 2, 3]
}
```

---

# 9. Parlour Portal API

The current system uses `parlour` endpoints, not the old hardcoded `salons` endpoints. Only admin-approved parlours are visible to clients.

---

## 9.1 Parlour Registration

### POST `/parlour/register`

Register a parlour. **Requires auth.**

**Body**

```json
{
  "name": "Glammatch Parlour",
  "owner": "Ayza Naveed",
  "phone": "03054962520",
  "email": "ayza@example.com",
  "address": "269-B Faisal Town Lahore",
  "city": "Lahore",
  "area": "Faisal Town Block B",
  "services": ["Haircut & Styling", "Bridal Makeup", "Facial & Cleanup"],
  "open_time": "09:00",
  "close_time": "21:00",
  "days": "Mon – Sat",
  "cnic": "3410412345672",
  "cnic_front_file": "data:image/png;base64,...",
  "cnic_back_file": "data:image/png;base64,...",
  "business_type": "Beauty Parlour",
  "price_min": 0,
  "price_max": 20000,
  "description": "A modern beauty parlour."
}
```

**Response**

```json
{
  "message": "Parlour registered successfully. Admin verification is pending.",
  "parlour": {
    "id": 1,
    "name": "Glammatch Parlour",
    "status": "pending"
  }
}
```

**Important rules**

- User can register one parlour only.
- CNIC must contain exactly 13 digits.
- CNIC front and back files are required.
- CNIC files must be JPG, PNG, WEBP, or PDF.
- Registration status starts as `pending`.
- Admin must approve before client bookings are allowed.

---

## 9.2 Owner Dashboard

### GET `/parlour/owner-dashboard`

Get logged-in owner's registered parlour, received bookings, and owner notifications. **Requires auth.**

**Response**

```json
{
  "parlour": {
    "id": 1,
    "name": "Glammatch Parlour",
    "status": "approved",
    "masked_cnic": "34104-*******-2"
  },
  "bookings": [],
  "notifications": []
}
```

### PUT `/parlour/my-parlour`

Update owner parlour details. **Requires auth.**

**Notes**

- Admin verification status remains attached to the parlour.
- Editable fields include contact details, address, services, timing, days, price range, and description.
- Validation blocks invalid phone/email/time/day/price values.

---

## 9.3 Approved Parlour Listing

### GET `/parlour/list`

List approved parlours only. **Requires auth.**

Optional query:

```text
?search=lahore
?service=Hair
```

**Response**

```json
{
  "parlours": [
    {
      "id": 1,
      "name": "Glammatch Parlour",
      "services": ["Haircut & Styling", "Bridal Makeup"],
      "status": "approved",
      "open_time": "09:00",
      "close_time": "21:00",
      "days": "Mon – Sat"
    }
  ],
  "count": 1
}
```

### GET `/parlour/<parlour_id>`

Get one approved parlour profile. **Requires auth.**

---

## 9.4 Client Booking

### POST `/parlour/booking`

Create a booking request for an approved parlour. **Requires auth.**

**Body**

```json
{
  "parlour_id": 1,
  "service": "Bridal Makeup",
  "datetime": "2026-05-14T10:30",
  "client_name": "Ayza",
  "client_phone": "03054962520",
  "note": "Please confirm availability."
}
```

**Response**

```json
{
  "booking_id": 10,
  "status": "pending",
  "parlour_name": "Glammatch Parlour"
}
```

**Booking validation**

- Parlour must be `approved`.
- Selected service must be offered by the parlour.
- Past date/time is not allowed.
- Booking more than 90 days ahead is not allowed.
- Closed days are not allowed.
- Time outside parlour open/close hours is not allowed.
- Same parlour and same time slot cannot have another active pending/confirmed booking.
- Client name and phone are required.
- Note maximum length is 500 characters.

---

### GET `/parlour/my-bookings`

Get current client's bookings. **Requires auth.**

**Notes**

- Past active bookings automatically show/update as `completed` after appointment time passes.
- Client can see booking status, parlour address, phone, chat availability, cancel availability, and 2-hour lock state.

---

### PUT `/parlour/booking/<booking_id>/cancel`

Client cancels own booking. **Requires auth.**

**Rules**

- Only `pending` or `confirmed` bookings can be cancelled.
- Cannot cancel if appointment time has already passed.
- Cannot cancel within 2 hours of appointment time.
- When client cancels, notification goes to the parlour owner only.

**Response**

```json
{
  "message": "Booking cancelled. Notification sent.",
  "status": "cancelled"
}
```

---

## 9.5 Owner Booking Management

### PUT `/parlour/owner-booking/<booking_id>/status`

Owner updates booking status. **Requires auth.**

**Allowed status values**

```text
pending | confirmed | rejected
```

**Important rules**

- Owner can manage bookings only after admin approval.
- Owner cannot manually mark a booking `completed`.
- Completion happens automatically after appointment time passes.
- Owner cannot reject within 2 hours of appointment time.
- When owner rejects, notification goes to the client only.

**Body**

```json
{
  "status": "confirmed"
}
```

---

## 9.6 Booking Chat

### GET `/parlour/booking-chat/<booking_id>`

Get booking-specific chat messages. **Requires auth.**

**Rules**

- Client can access chat for their own booking.
- Owner can access chat for bookings of their own parlour.
- Chat is closed when booking is `cancelled`, `rejected`, `completed`, or appointment time has passed.

---

### POST `/parlour/booking-chat/<booking_id>`

Send a booking-specific message. **Requires auth.**

**Body**

```json
{
  "message": "Hi, can you confirm my appointment?",
  "sender_type": "client"
}
```

`sender_type` values:

```text
client | parlour
```

**Response**

```json
{
  "message_id": 4,
  "sent": true,
  "sender_type": "client"
}
```

---

## 9.7 Notifications

### GET `/parlour/notifications`

Get role-based notifications. **Requires auth.**

Query:

```text
?role=client
?role=owner
```

**Rules**

- Client cancellation notification is shown to owner only.
- Parlour rejection notification is shown to client only.

### PUT `/parlour/notifications/read-all`

Mark notifications as read. **Requires auth.**

Query:

```text
?role=client
?role=owner
```

---

## 9.8 Parlour Chatbot

### POST `/parlour/chat`

Simple informational chatbot for parlour portal help. **Requires auth.**

**Body**

```json
{
  "message": "How do I register my parlour?"
}
```

---

## 9.9 Parlour Stats

### GET `/parlour/stats`

Returns basic parlour portal stats for the frontend. **Requires auth.**

---

# 10. Admin API

## POST `/admin/login`

Validate admin code.

**Body**

```json
{
  "admin_code": "12345678"
}
```

**Response**

```json
{
  "ok": true,
  "message": "Admin access granted"
}
```

---

## GET `/admin/parlours`

List parlours for admin review.

**Admin code required.**

Optional query:

```text
?status=pending
?status=approved
?status=rejected
?status=all
```

**Notes**

- Admin response includes CNIC front/back document data for review.
- Frontend opens these documents in the in-page viewer.

---

## PUT `/admin/parlours/<parlour_id>/status`

Approve/reject/mark pending a parlour.

**Admin code required.**

**Body**

```json
{
  "status": "approved",
  "note": "CNIC verified."
}
```

Allowed values:

```text
pending | approved | rejected
```

---

## GET `/admin/bookings`

List all parlour bookings for admin. **Admin code required.**

---

# 11. Booking Status Flow

```text
Client submits booking
        ↓
[pending]
   ↓ accepted by parlour
[confirmed]
   ↓ appointment time passes
[completed]  ← automatic only
```

Other flows:

```text
pending/confirmed → cancelled  client cancellation only if 2+ hours before time
pending/confirmed → rejected   owner rejection only if 2+ hours before time
```

Closed states:

```text
cancelled | rejected | completed
```

When a booking reaches a closed state:

- Chat is hidden/closed.
- Action buttons are hidden.
- Booking remains visible for record tracking.
