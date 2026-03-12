# jobfusion/ml/job_recommendation.py

import numpy as np
import pandas as pd
from sklearn.cluster import OPTICS
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobfusion.settings')
django.setup()

from home.models import postjob


# ── Global state (fitted once per server session) ──────────────────────────
_cache = {}


def _build_model():
    """Fetch jobs, vectorize, run OPTICS, cache everything."""
    jobs = postjob.objects.all().values('id', 'req', 'job_type', 'location')
    df = pd.DataFrame(list(jobs))

    if df.empty:
        raise ValueError("No jobs found in database.")

    # Skills
    df['skills_list'] = df['req'].apply(
        lambda x: [s.strip().lower() for s in str(x).split(',')]
    )
    mlb = MultiLabelBinarizer()
    skills_matrix = mlb.fit_transform(df['skills_list'])

    # Categorical encoders
    le_type = LabelEncoder()
    le_loc  = LabelEncoder()
    type_enc = le_type.fit_transform(df['job_type'].astype(str)).reshape(-1, 1)
    loc_enc  = le_loc.fit_transform(df['location'].astype(str)).reshape(-1, 1)

    X = np.hstack([skills_matrix, type_enc, loc_enc]).astype(float)

    # ── OPTICS clustering ──────────────────────────────────────────────────
    optics = OPTICS(min_samples=2, metric='cosine')
    labels = optics.fit_predict(X)          # -1 = noise

    _cache.update({
        'df': df,
        'X': X,
        'labels': labels,
        'mlb': mlb,
        'le_type': le_type,
        'le_loc': le_loc,
    })
    return _cache


def _get_cache():
    """Return cache, building it if empty."""
    if not _cache:
        _build_model()
    return _cache


def refresh_model():
    """Call this after new jobs are added to re-cluster."""
    _cache.clear()
    _build_model()


# ── Main recommendation function ───────────────────────────────────────────
def recommend_jobs(user_skills: str, user_job_type: str, user_location: str, top_n: int = 10):
    """
    Returns a DataFrame with columns: id, score, cluster
    Flow:
      1. Vectorize user input using fitted encoders
      2. Find the closest cluster via cosine similarity to cluster centroids
      3. Recommend top-N jobs from that cluster (fallback: global top-N)
    """
    cache = _get_cache()
    df, X, labels = cache['df'], cache['X'], cache['labels']
    mlb, le_type, le_loc = cache['mlb'], cache['le_type'], cache['le_loc']

    # ── Vectorize user ─────────────────────────────────────────────────────
    user_skills_list = [s.strip().lower() for s in user_skills.split(',')]

    # Skills — unknown skills become all-zero columns (transform handles it)
    known_skills = [s for s in user_skills_list if s in mlb.classes_]
    user_skill_vec = mlb.transform([known_skills]) if known_skills else np.zeros((1, len(mlb.classes_)))

    try:
        user_type = le_type.transform([user_job_type])[0]
    except ValueError:
        user_type = 0          # fallback for unseen label

    try:
        user_loc = le_loc.transform([user_location])[0]
    except ValueError:
        user_loc = 0

    user_vector = np.hstack([user_skill_vec, [[user_type]], [[user_loc]]]).astype(float)

    # ── Find best cluster ──────────────────────────────────────────────────
    unique_clusters = [c for c in np.unique(labels) if c != -1]

    best_cluster = None
    if unique_clusters:
        # Centroid of each cluster → pick closest to user vector
        centroids = np.array([
            X[labels == c].mean(axis=0) for c in unique_clusters
        ])
        centroid_sims = cosine_similarity(user_vector, centroids)[0]
        best_cluster = unique_clusters[int(centroid_sims.argmax())]

    # ── Score jobs inside that cluster ────────────────────────────────────
    if best_cluster is not None:
        cluster_mask = labels == best_cluster
        candidate_X  = X[cluster_mask]
        candidate_df = df[cluster_mask].copy()
    else:
        # All noise or single cluster — fall back to full search
        candidate_X  = X
        candidate_df = df.copy()

    similarities = cosine_similarity(user_vector, candidate_X)[0]
    top_idx = similarities.argsort()[::-1][:top_n]

    result = candidate_df.iloc[top_idx][['id']].copy()
    result['score']   = similarities[top_idx].round(4)
    result['cluster'] = best_cluster if best_cluster is not None else -1

    return result.reset_index(drop=True)