import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier


with open("heroes.json","r", encoding="utf-8") as f:
    heroes = json.load(f)
hero_to_index  = {hero["id"]: x for x, hero in enumerate(heroes)}
    
def match_to_vector(match: dict, hero_to_index: dict) -> list[int]:
    vector = [0] * (len(hero_to_index) * 2)
    dire = len(hero_to_index)
    for i in match["radiant_team"]:
        index = hero_to_index[i]
        vector[index] = 1
    for i in match["dire_team"]:
        index = hero_to_index[i]
        vector[index + dire] = 1
    return vector
    
with open("raw_matches.json","r", encoding="utf-8") as f:
    matches = json.load(f)

    
X = [match_to_vector(m, hero_to_index) for m in matches]
y = [m["radiant_win"] for m in matches]
print(len(X), len(X[0]), len(y))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
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