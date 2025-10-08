# **🎹 Piano Practice Tracker (MVP)**

A minimal full-stack web app that lets users log piano practice sessions and track progress over time.
Built with **FastAPI + PostgreSQL** (backend) and **React + Vite** (frontend).

⸻

## 🚀 Live Demo

🌐 Frontend: https://practice-tracker-rho.vercel.app
🧠 Backend API: https://practice-tracker.onrender.com

⚠️ Note: This is a bare minimum MVP — authentication and basic CRUD work, but UI and data refresh logic are still under active development.

⸻

## ✨ Core Features (MVP)

✅ Google OAuth Login — secure login with Google via FastAPI + Authlib
✅ Database Integration — PostgreSQL + SQLModel for persistent user, piece, and session data
✅ Add & View Pieces — create new piano pieces and associate practice sessions with them
✅ Track Practice Sessions — log minutes practiced per session and view total streak stats
✅ Session-based Auth — user JWTs stored as secure cookies for authenticated API access
✅ Cross-origin Setup — deployed frontend (Vercel) and backend (Render) communicate via CORS
✅ Health & Stats Endpoints — API endpoints for debugging, monitoring, and future data visualization

⸻

## 🛠️ Tech Stack

Frontend:
	•	React + Vite
	•	TypeScript
	•	Fetch API with credentials: "include"
	•	Styled with CSS variables for dark theme

Backend:
	•	FastAPI
	•	SQLModel (ORM over SQLAlchemy)
	•	PostgreSQL (Render free tier)
	•	Authlib (Google OAuth)
	•	Uvicorn + Starlette
	•	Session + CORS Middleware

Deployment:
	•	Frontend on Vercel
	•	Backend on Render
	•	.env secrets set via Render dashboard (no secrets in repo)

⸻

## 🧩 Current API Endpoints

🔐 Authentication
	•	GET /login — Redirects user to Google OAuth consent screen
	•	GET /auth/callback — Handles Google OAuth response and creates a session cookie
	•	GET /logout — Logs out the current user and clears session cookie

👤 User
	•	GET /api/me — Returns the current authenticated user’s profile (name, email)
	•	GET /api/health — Basic health check endpoint for monitoring

🎵 Pieces
	•	GET /api/pieces — Retrieve all pieces added by the user
	•	POST /api/pieces — Add a new piano piece (title, composer, etc.)
	•	(Planned) GET /api/pieces/summary — Returns each piece with total practice minutes

⏱️ Practice Sessions
	•	GET /api/sessions — Retrieve all practice sessions for the logged-in user
	•	POST /api/sessions — Log a new practice session linked to a specific piece

📊 Stats
	•	GET /api/stats — Returns overall statistics such as:
	•	Total number of pieces
	•	Total sessions logged
	•	Total minutes practiced
	•	Current practice streak (days)

⸻

## 💡 Future Features (Planned)

🪄 Auto-refresh on Add — update dropdowns and stats immediately after adding a piece/session
📊 Piece Summary Dashboard — total minutes practiced per piece
🗑️ Edit / Delete Pieces — manage existing pieces and sessions
📈 Data Visualization — charts for daily practice trends and streaks
🔔 Streak Notifications — daily practice reminders
📱 Responsive UI — better mobile layout and visuals
💾 Cloud Storage / Media Uploads — optional audio/video logs for performances
🧠 ML Recommendations (stretch goal) — smart insights on practice focus areas

⸻

## 🧭 Local Development 
## 1️⃣ Backend setup
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in GOOGLE_CLIENT_ID, SECRET_KEY, etc.
uvicorn app.main:app --reload

## 2️⃣ Frontend setup
cd frontend
npm install
npm run dev

Then open http://localhost:5173.
