import json
import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
import joblib

with open("heroes.json","r", encoding="utf-8") as f:
    heroes = json.load(f)
hero_to_index  = {hero["id"]: x for x, hero in enumerate(heroes)}
    

def partial_match_to_vector(match, hero_to_index, n_per_side):
    vector = [0] * (len(hero_to_index) * 2)
    dire = len(hero_to_index)
    
    radiant_sample = random.sample(match["radiant_team"], n_per_side)
    dire_sample = random.sample(match["dire_team"], n_per_side)

    for i in radiant_sample:
        index = hero_to_index[i]
        vector[index] = 1
        
    for i in dire_sample:
        index = hero_to_index[i]
        vector[index + dire] = 1
    return vector


with open("raw_matches.json","r", encoding="utf-8") as f:
    matches = json.load(f)


train_matches, test_matches = train_test_split(matches, test_size=0.2, random_state=42)

def build_dataset(match_list):
    X, y = [], []
    for m in match_list:
        for n in [2, 4, 5]:
            X.append(partial_match_to_vector(m, hero_to_index, n))
            y.append(m["radiant_win"])
    return X, y

X_train, y_train = build_dataset(train_matches)
X_test, y_test = build_dataset(test_matches)


model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))




model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))



joblib.dump(model, "model.joblib")
joblib.dump(hero_to_index, "hero_to_index.joblib")