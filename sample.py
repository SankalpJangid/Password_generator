import random
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

pswd_data = pd.read_csv("paswword_strenght.csv", error_bad_lines=False)
pswd = np.array(pswd_data)
random.shuffle(pswd)
ylabels  = [s[1] for s in pswd]
allpasswords = [s[0] for s in pswd]
def makeTokens(f):
    tokens = []
    for i in f:
        tokens.append(i)
    return tokens
vectorizer = TfidfVectorizer(tokenizer=makeTokens)
X = vectorizer.fit_transform(allpasswords)
X_train, X_test, y_train, y_test = train_test_split(X, ylabels, test_size=0.2)	
dt = DecisionTreeClassifier()
dt.fit(X_train,y_train)
site_name = "sankalp"
print(site_name)
sample_1 = [site_name]
X_predict11 = vectorizer.transform(sample_1)
y_Predict11 = dt.predict(X_predict11)
print(y_Predict11)