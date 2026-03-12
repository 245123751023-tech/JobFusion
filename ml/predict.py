import os
import joblib
import re
import nltk
from nltk.corpus import stopwords

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR,"toxic_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR,"tfidf_vectorizer.pkl"))

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]',"",text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)


def predict_toxic(comment):
    cleaned = clean_text(comment)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    return int(prediction)
