# Kundli Calc – Next Steps Plan (2025-11-15)

This document summarizes what needs to happen from **now** to a world‑class, deployable kundli web app, based on the current repository.

---

## 0. Fix local environment & backend startup

- **0.1 Activate virtualenv (Windows)**
  - From project root: `\.venv\Scripts\activate`
- **0.2 Run backend with uvicorn via Python**
  - Use: `python -m uvicorn backend.app.main:app --reload --port 8000`
  - Keep using this form so you don’t depend on a globally-installed `uvicorn`.
- **0.3 Quick health check**
  - Open: `http://localhost:8000/api/v1/health` (or `/docs`) in the browser.

Outcome: backend reliably runs on port **8000** using the project’s venv.

---

## 1. Lock in calculation correctness for 09-10-1990 (Loznica)

Goal: certify that the divisional engine + chart pipeline are correct for the reference profile before any more frontend work.

- **1.1 Run full user test script**
  - Command from repo root (with backend running on :8000):
    - `python test_user_complete.py`
  - This will:
    - Call `/charts/calculate` for 1990‑10‑09 09:10 Loznica.
    - Save `user_chart_result.json`.
    - Call `/divisional/calculate` for D2–D60.
    - Compare against `tests/test_profile/kundli.txt`.
- **1.2 Inspect kundli validation report**
  - Open `kundli_validation_report.txt`.
  - Target state:
    - D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60 all **match**.
- **1.3 If mismatches exist**
  - Check `backend/app/core/calculations/divisional_charts.py` formulas for the affected D‑charts.
  - Cross‑verify with:
    - `tests/test_profile/kundli.txt` (house targets).
    - `backend/tests/test_divisional_charts.py` and `backend/tests/test_divisional.py`.
  - Fix logic, re‑run `python test_user_complete.py` until clean.

Outcome: a green validation for your own birth chart, across key D‑charts, frozen as a reference.

---

## 2. Backend stability & APIs (short term)

- **2.1 Verify core endpoints manually**
  - `/charts/calculate` – main chart (D1 + selective vargas).
  - `/divisional/calculate` – Dn as standalone.
  - `/ashtakavarga/*` – strength APIs.
  - `/panchang/calculate` and `/panchang/sun_times` – panchāng + sun times.
- **2.2 Mark calculation core as "frozen"**
  - After tests pass, avoid changing divisional, aspect, shadbala, ashtakavarga logic unless you:
    - Add a failing test first.
    - Re‑run `test_user_complete.py` and relevant unit tests.

Outcome: trusted backend acting as a stable engine for the frontend.

---

## 3. Frontend MVP: from JSON to usable charts

Focus: turn the existing Next.js frontend into a **use‑able kundli app** for your own birth data and arbitrary users.

- **3.1 Input form
  - Build a single page with:
    - Date picker, time selector (with timezone awareness).
    - Location field + coordinates (for now, manual lat/long is acceptable; later, geocoder).
    - Options: ayanamsa, house system, chart types (D1, D9, D10 at minimum).
  - Wire form → call `/charts/calculate`.

- **3.2 Chart rendering
  - Reuse and polish `SouthIndianChart.tsx` and `DivisionalChart.tsx` to:
    - Render a clean South Indian D1 chart.
    - Render D9, D10 and optionally other vargas in a tabbed layout.
  - Highlight planet positions in each house, with tooltips for sign, degrees, nakshatra.

- **3.3 Result layout
  - Layout page sections:
    - Header with core birth details.
    - Main D1 chart.
    - Tabs: Divisional charts, Ashtakavarga, Dasha overview.
    - Raw JSON viewer only as a debug panel.

Outcome: a single, pleasant page where anyone can input data and see a complete, interactive chart.

---

## 4. Persistence, auth, and database choice

You have Postgres/Supabase and Mongo plumbing. Short‑term decision:

- **4.1 Use Supabase/Postgres as system of record**
  - Store:
    - Users (auth via Supabase).
    - Saved charts (normalized: birth data, chart settings, selected outputs).
    - Simple event log (optional).

- **4.2 Keep Mongo optional**
  - Use only if you need to snapshot full JSON payloads or logs.

- **4.3 Minimal schema for MVP**
  - `users` – from Supabase.
  - `charts` – `user_id`, birth data, settings, created_at.

Outcome: basic accounts + "save this chart" for later retrieval, with Supabase as the primary DB.

---

## 5. UX polish and PDFs

Once the core flow is working:

- **5.1 UX improvements**
  - Loading indicators and error states for API calls.
  - Mobile‑responsive layout (Tailwind or existing CSS).
  - Basic theme consistency.

- **5.2 PDF export**
  - Use either:
    - `jsPDF` + `html2canvas`, or
    - `react-pdf` for a templated report.
  - Include:
    - D1 South Indian chart.
    - Planet tables, basic yogas, short interpretations.

Outcome: a shareable, printable artifact that feels like a professional report.

---

## 6. Advanced features (post-MVP)

These are important but can wait until the MVP is live:

- Expand yoga library and tie into frontend display.
- Add better transit views & timelines.
- Implement KP / Jaimini if you choose that direction.
- Multi‑language expansion beyond English.
- More sophisticated matching, muhūrta, prashna.

---

## 7. Deployment and operations

- **7.1 Staging deployment**
  - Frontend → Vercel or Cloudflare Pages.
  - Backend → Railway/Render with Postgres and Redis.
- **7.2 Monitoring**
  - Basic health checks and logging.
  - Error tracking (e.g. Sentry) once traffic appears.

Outcome: live, shareable URL you can give to real users.

---

## 8. Immediate action checklist

1. Fix backend startup on Windows (`python -m uvicorn ...`).
2. Run `python test_user_complete.py` and confirm D‑chart validation against `tests/test_profile/kundli.txt`.
3. Build and wire a proper frontend input form → `/charts/calculate`.
4. Render D1/D9/D10 charts cleanly using existing React components.
5. Hook in Supabase for auth + chart persistence.
6. Add PDF export for a single chart.
7. Deploy a staging version and test on multiple devices.
