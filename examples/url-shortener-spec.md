# URL Shortener

> A simple URL shortening service like bit.ly

**Generated:** 2024-01-15 10:30  
**Type:** Web App (Full-stack)  
**Stack:** Next.js, PostgreSQL, Tailwind CSS

---

## 🎯 Overview

### Problem
I frequently share long URLs that look ugly and are hard to track. Existing services have ads, require accounts, or have privacy concerns.

### Solution
Build my own minimal URL shortener that:
- Creates short links instantly
- Tracks click counts
- No account required
- Self-hosted = privacy

### Target User
Me, for personal use. Maybe friends/family later.

---

## ✨ Features

### Must Have (P0)
- Paste long URL, get short URL
- Short URLs redirect correctly
- Basic click tracking (count only)
- Copy to clipboard button
- Custom short codes (optional)

### Nice to Have (P1)
- QR code generation
- Expiring links
- Click analytics (referrer, location)
- Password-protected links
- API for automation

### Non-Goals (Out of Scope)
- User accounts/auth
- Team features
- Link editing after creation
- Branded domains
- Monetization/ads

---

## 🔧 Technical Decisions

### Stack
- **Frontend**: Next.js 14 + App Router
- **Styling**: Tailwind CSS
- **Database**: PostgreSQL (Supabase free tier)
- **Hosting**: Vercel

### Constraints
- Must work without JavaScript (progressive enhancement)
- Page load under 1 second
- Short codes: 6 characters, alphanumeric

---

## 🚶 User Flows

### Flow 1: Shorten URL
```
1. User visits homepage
2. Pastes long URL in input
3. (Optional) Enters custom short code
4. Clicks "Shorten"
5. Sees short URL
6. Clicks "Copy" button
7. Short URL is in clipboard
```

### Flow 2: Access Short URL
```
1. Someone visits short URL (e.g., mysite.com/abc123)
2. Server logs the click
3. Redirects to original URL (301)
4. User sees original destination
```

### Flow 3: Invalid Short URL
```
1. Someone visits invalid short URL
2. Server returns 404 page
3. Page has link back to homepage
```

---

## 💾 Data Model

### Link
```sql
links:
  - id: SERIAL PRIMARY KEY
  - short_code: VARCHAR(20) UNIQUE NOT NULL
  - original_url: TEXT NOT NULL
  - clicks: INTEGER DEFAULT 0
  - created_at: TIMESTAMP DEFAULT NOW()
```

No user table needed (no auth).

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage with form |
| POST | `/api/shorten` | Create short URL |
| GET | `/:code` | Redirect to original |
| GET | `/api/stats/:code` | Get click count |

### POST /api/shorten
```json
// Request
{
  "url": "https://very-long-url.com/path",
  "customCode": "mylink"  // optional
}

// Response
{
  "shortUrl": "https://mysite.com/mylink",
  "originalUrl": "https://very-long-url.com/path"
}
```

---

## 📁 File Structure

```
url-shortener/
├── src/
│   ├── app/
│   │   ├── page.tsx           # Homepage
│   │   ├── [code]/
│   │   │   └── route.ts       # Redirect handler
│   │   ├── api/
│   │   │   ├── shorten/
│   │   │   │   └── route.ts   # Create link
│   │   │   └── stats/
│   │   │       └── [code]/
│   │   │           └── route.ts
│   │   └── layout.tsx
│   ├── components/
│   │   └── ShortenForm.tsx
│   └── lib/
│       └── db.ts
├── tailwind.config.js
└── package.json
```

---

## 📊 Implementation Phases

### Phase 1: Basic Shortening
- [x] Next.js project setup
- [ ] Database schema + connection
- [ ] Homepage with form
- [ ] POST /api/shorten endpoint
- [ ] Display result with copy button

### Phase 2: Redirects
- [ ] Dynamic route for /:code
- [ ] Look up and redirect
- [ ] Increment click counter
- [ ] Handle 404 for invalid codes

### Phase 3: Polish
- [ ] Input validation (valid URL)
- [ ] Custom code validation
- [ ] Loading states
- [ ] Error messages
- [ ] Mobile responsive

### Phase 4: Deploy
- [ ] Set up Supabase database
- [ ] Deploy to Vercel
- [ ] Custom domain (optional)

---

## 🎯 Success Criteria

- [ ] Can shorten a URL and get result
- [ ] Short URLs redirect correctly
- [ ] Click count increments
- [ ] Works on mobile
- [ ] Deployed and shareable

---

## 💬 Instructions for AI

Start with Phase 1. Let's get basic shortening working first.

Focus areas:
- Simple, clean UI (just one input and button)
- Proper URL validation
- Handle duplicate URLs (return existing short code)

Questions to address:
- Should we use Supabase client or raw SQL?
- How to generate short codes? (nanoid suggested)

---

*Generated with Speckit 🛠️*
