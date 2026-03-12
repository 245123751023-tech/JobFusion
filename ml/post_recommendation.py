import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import OPTICS
from sklearn.metrics.pairwise import cosine_similarity

def get_recommended_posts(user_profile, posts_qs):
    # Need at least 5 posts for clustering to make sense
    posts = list(posts_qs)
    if len(posts) < 5:
        return posts  # fallback: return as-is

    # Build post texts
    post_texts = []
    for post in posts:
        caption = post.caption or ""
        desc = post.description or ""
        post_texts.append(caption + " " + desc)

    # User text from skills + bio
    user_text = (user_profile.skills or "") + " " + (user_profile.bio or "")

    # TF-IDF — fit on posts, transform both posts and user
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    post_matrix = vectorizer.fit_transform(post_texts).toarray()  # (n_posts, n_features)
    user_vector = vectorizer.transform([user_text]).toarray()     # (1, n_features)

    # OPTICS clustering on posts
    optics = OPTICS(min_samples=2, metric='cosine')
    labels = optics.fit_predict(post_matrix)

    # Separate noise points (label == -1)
    unique_clusters = set(labels)
    unique_clusters.discard(-1)

    if not unique_clusters:
        # All noise — fallback to direct cosine similarity ranking
        scores = cosine_similarity(user_vector, post_matrix)[0]
        sorted_posts = [p for _, p in sorted(zip(scores, posts), reverse=True)]
        return sorted_posts

    # Compute centroid for each cluster
    centroids = {}
    for cluster_id in unique_clusters:
        indices = [i for i, l in enumerate(labels) if l == cluster_id]
        centroids[cluster_id] = np.mean(post_matrix[indices], axis=0)

    # Find best cluster — closest centroid to user vector
    best_cluster = None
    best_score = -1
    for cluster_id, centroid in centroids.items():
        score = cosine_similarity(user_vector, centroid.reshape(1, -1))[0][0]
        if score > best_score:
            best_score = score
            best_cluster = cluster_id

    # Get posts from best cluster + sort by individual similarity
    best_indices = [i for i, l in enumerate(labels) if l == best_cluster]
    best_post_matrix = post_matrix[best_indices]
    scores = cosine_similarity(user_vector, best_post_matrix)[0]

    cluster_posts = [posts[i] for i in best_indices]
    sorted_posts = [p for _, p in sorted(zip(scores, cluster_posts), key=lambda x: x[0], reverse=True)]

    # Noise posts appended at the end (not recommended but still shown)
    noise_posts = [posts[i] for i, l in enumerate(labels) if l == -1]

    return sorted_posts + noise_posts