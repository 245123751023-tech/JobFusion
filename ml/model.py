import numpy as np
import pandas as pd

import os
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
train_path = os.path.join(script_dir, "train.csv")

data = pd.read_csv(train_path)
# data = pd.read_csv("train.csv")
print(data.head())

data['toxic_comment'] = data[['toxic','severe_toxic','obscene','threat','insult','identity_hate']].max(axis=1)

x = data['comment_text']
y = data['toxic_comment']

import re
import nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
from nltk.corpus import stopwords 

#NLTK-Natural Language Tool Kit

stop_words = set(stopwords.words('english')) # creates set of english words which are mostly common usless words i.e I,am,the.a,in,is,....


#Lets clean the text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]','',text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

data['clean_message'] = data['comment_text'].apply(clean_text)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english',max_features=20000)

x = vectorizer.fit_transform(data['clean_message'])

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=42,stratify=y)


from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()
model.fit(x_train,y_train)
# y_pred = model.predict(x_test)

# from sklearn.metrics import accuracy_score
# print("accuracy:",accuracy_score(y_pred,y_test))

import joblib

joblib.dump(model,"toxic_model.pkl")
joblib.dump(vectorizer,"tfidf_vectorizer.pkl")