# JobFusion

A full-stack **Job & Social Platform** built with Django. Users can post jobs, apply for them, connect with people, share posts, and get ML-powered recommendations — all in one place.

---

## Features

### ML Recommendations
- **Job Recommendations** — OPTICS clustering + cosine similarity on job listings. Skills vectorized with `MultiLabelBinarizer`, job type and location with `LabelEncoder`. Finds the closest cluster centroid to the user's profile, then ranks jobs within that cluster. Falls back to keyword search if ML fails.
- **People Recommendations** — Same OPTICS approach on user profiles. Combines `skills` + `otherskills` into a single feature vector with role encoding. Returns top-N similar profiles excluding self.
- **Post Recommendations** — TF-IDF vectorization on post captions/descriptions. Clusters posts with OPTICS, matches user's skills+bio vector to the closest cluster centroid, ranks posts by cosine similarity. Noise posts shown at the end.

### Social
- Posts with image/video uploads via Cloudinary
- Like / dislike posts
- Comments with **toxic comment filtering** (`ml/predict.py`)
- Connection requests — send, accept, reject
- View other users' profiles

### Jobs
- Post, view, and delete job listings
- Apply for jobs (requires resume + skills on profile)
- HR/Recruiter view to see applicants
- Job search by title, location, company, type, salary

### Other
- Multi-step onboarding (name/phone/location → role → skills & education → profile pic)
- Role-based flows — Student/Intern/Freelancer vs HR/Manager/Recruiter
- Resume upload and delete
- AI Resume enhancer (GPT-4o-mini via RapidAPI)
- Real-time chat (Firebase)
- Contact us form

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django |
| Database | PostgreSQL (prod), SQLite (dev) |
| ML | scikit-learn — OPTICS, TF-IDF, cosine similarity |
| Media | Cloudinary |
| Real-time Chat | Firebase Realtime Database |
| Deployment | Render.com, Gunicorn, WhiteNoise |

---

## Project Structure

```
JobFusion/
├── authentication/        # Signup, login, logout, onboarding (page1–4)
├── home/                  # Feed, jobs, posts, connections, profile, chat
│   ├── models.py          # Profile, Posts, postjob, Application, Requests, Comment
│   └── views.py           # All main views
├── ml/
│   ├── job_recommendation.py    # OPTICS job recommender
│   ├── people_recommendation.py # OPTICS people recommender
│   ├── post_recommendation.py   # TF-IDF + OPTICS post recommender
│   └── predict.py               # Toxic comment classifier
├── jobfusion/             # Django settings
├── firebase_config.py     # Firebase Admin SDK init
├── firebase_chat.py       # Firebase chat utilities
├── import_jobs.py         # Import jobs into DB
├── build.sh               # Render build script
├── render.yaml            # Render deployment config
└── requirements.txt
```

---

## Local Setup

```bash
git clone https://github.com/PraveenAchary/JobFusion.git
cd JobFusion
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Deployment

Deployed on **Render.com** using `render.yaml` and `build.sh`.

Live: https://jobfusion-0bo7.onrender.com/

---

**Built by [Praveen Achary](https://github.com/PraveenAchary)**
