# jobfusion/ml/people_recommendation.py

import numpy as np
import pandas as pd
from sklearn.cluster import OPTICS
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobfusion.settings')
django.setup()

from home.models import Profile


# ── Global cache (built once per server session) ───────────────────────────
_people_cache = {}


def _parse_skills(skills_str, otherskills_str=None):
    """
    Combine skills + otherskills into one clean list.
    "Python, Django" + "React, SQL" → ["python", "django", "react", "sql"]
    """
    combined = str(skills_str or '')
    if otherskills_str:
        combined += ',' + str(otherskills_str)
    return [s.strip().lower() for s in combined.split(',') if s.strip()]


def _build_people_model():
    """
    Fetch all profiles, vectorize skills + role, run OPTICS, cache everything.
    """
    profiles = Profile.objects.all().values('id', 'skills', 'otherskills', 'Role')
    df = pd.DataFrame(list(profiles))

    if df.empty:
        raise ValueError("No profiles found in database.")

    # ── Combine skills + otherskills into one list per profile ─────────────
    df['skills_list'] = df.apply(
        lambda row: _parse_skills(row['skills'], row['otherskills']), axis=1
    )

    # ── MLB: skills → binary matrix ────────────────────────────────────────
    mlb = MultiLabelBinarizer()
    skills_matrix = mlb.fit_transform(df['skills_list'])

    # ── Label encode Role ──────────────────────────────────────────────────
    le_role = LabelEncoder()
    role_encoded = le_role.fit_transform(df['Role'].astype(str)).reshape(-1, 1)

    # ── Final feature matrix ───────────────────────────────────────────────
    # Multiply role column by 2 so it has slightly more weight than a single skill
    X = np.hstack([skills_matrix, role_encoded * 2]).astype(float)

    # ── OPTICS clustering ──────────────────────────────────────────────────
    optics = OPTICS(min_samples=2, metric='cosine')
    labels = optics.fit_predict(X)

    _people_cache.update({
        'df': df,
        'X': X,
        'labels': labels,
        'mlb': mlb,
        'le_role': le_role,
    })

    return _people_cache


def _get_people_cache():
    """Return cache, building it if empty."""
    if not _people_cache:
        _build_people_model()
    return _people_cache


def refresh_people_model():
    """Call after a new user registers or updates their profile."""
    _people_cache.clear()
    _build_people_model()


# ── Main recommendation function ───────────────────────────────────────────
def recommend_people(current_profile_id, top_n=10):
    """
    Given a profile ID, returns top_n similar people (excluding self).

    Returns:
        [{'id': 5, 'score': 0.94}, {'id': 12, 'score': 0.87}, ...]

    Flow:
        1. Get current user's vector from cache
        2. Find their closest cluster via centroid matching
        3. Rank people inside that cluster by cosine similarity
        4. Exclude self
    """
    cache = _get_people_cache()
    df, X, labels = cache['df'], cache['X'], cache['labels']

    # ── Find current user's row ────────────────────────────────────────────
    user_rows = df[df['id'] == current_profile_id]

    if user_rows.empty:
        # New profile not in cache yet → rebuild once and retry
        refresh_people_model()
        cache = _get_people_cache()
        df, X, labels = cache['df'], cache['X'], cache['labels']
        user_rows = df[df['id'] == current_profile_id]

    if user_rows.empty:
        return []  # profile genuinely doesn't exist

    user_idx  = user_rows.index[0]
    user_vector = X[user_idx].reshape(1, -1)

    # ── Find best cluster ──────────────────────────────────────────────────
    unique_clusters = [c for c in np.unique(labels) if c != -1]

    best_cluster = None
    if unique_clusters:
        centroids = np.array([
            X[labels == c].mean(axis=0) for c in unique_clusters
        ])
        centroid_sims = cosine_similarity(user_vector, centroids)[0]
        best_cluster  = unique_clusters[int(centroid_sims.argmax())]

    # ── Filter to best cluster (fallback: all profiles) ───────────────────
    if best_cluster is not None:
        cluster_mask  = labels == best_cluster
        candidate_X   = X[cluster_mask]
        candidate_df  = df[cluster_mask].copy().reset_index(drop=True)
        candidate_orig_idx = np.where(cluster_mask)[0]
    else:
        # All noise or only 1 cluster → search everyone
        candidate_X        = X
        candidate_df       = df.copy().reset_index(drop=True)
        candidate_orig_idx = np.arange(len(df))

    # ── Cosine similarity against cluster candidates ───────────────────────
    similarities = cosine_similarity(user_vector, candidate_X)[0]

    # ── Rank, exclude self, collect top_n ─────────────────────────────────
    results = []
    for rank_idx in similarities.argsort()[::-1]:
        pid = int(candidate_df.iloc[rank_idx]['id'])

        if pid == current_profile_id:
            continue  # skip self

        results.append({
            'id':      pid,
            'score':   round(float(similarities[rank_idx]), 4),
            'cluster': int(best_cluster) if best_cluster is not None else -1,
        })

        if len(results) >= top_n:
            break

    return results