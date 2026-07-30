TalentTrack — Mini Recruitment CRM
A small, resume-worthy Python project: track job candidates through a hiring pipeline (Applied → Screening → Interview → Offer → Hired/Rejected).

Built with Python + SQLite + Pandas + Streamlit — all skills already on your resume, and directly relevant to Recruit CRM's product (a recruitment CRM SaaS).

Run it
pip install streamlit pandas
streamlit run app.py
This opens a local web app in your browser. It creates candidates.db (SQLite) automatically on first run.

What it demonstrates
Reusable, modular code — one data-access layer (get_connection, add_candidate, update_stage, delete_candidate, fetch_candidates) that the UI calls into, so it's easy to extend without touching SQL scattered everywhere.
CRUD + persistence — SQLite table, add/update/delete candidates.
Data analysis basics — Pandas for filtering/search, a live dashboard with per-stage counts and a bar chart.
CSV export — a common "ops" feature recruitment CRMs need.
Easy ways to extend it (good for interview talk-track)
Add authentication (login/signup) — you already did this in your Godot internship project with SQLite, so it's a natural next step here.
Add a "days in stage" column using date_added to flag stalled candidates.
Swap SQLite for MySQL/MongoDB (both already on your resume) to show you can work with more than one database.
Add a simple time-series view: candidates added per week, using the same Pandas/resampling skills from your screen-addiction project.
Talking about it in the interview
"Why did you build it?" — Recruit CRM's product is literally a recruitment CRM, so I built a small one myself to understand the domain and practice writing reusable, scalable Python.
"How would you scale it?" — separate the data layer behind an API (Flask/FastAPI), move SQLite to a real database, add auth and role-based access.
