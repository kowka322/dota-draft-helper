import joblib
import json

model = joblib.load("model.joblib")
hero_to_index = joblib.load("hero_to_index.joblib")


def build_vector(allies, enemies, side):
    vector = [0] * (len(hero_to_index) * 2)
    dire = len(hero_to_index)

    if side == "radiant":
        for hero in allies:
            vector[hero_to_index[hero]] = 1
        for hero in enemies:
            vector[hero_to_index[hero] + dire] = 1
    elif side == "dire":
        for hero in allies:
            vector[hero_to_index[hero] + dire] = 1
        for hero in enemies:
            vector[hero_to_index[hero]] = 1
    return vector





def recommendator(allies, enemies, side):
    taken = set(allies) | set(enemies)
    candidates = [hero_id for hero_id in hero_to_index if hero_id not in taken]

    results = []

    for candidate in candidates:
        my_team = allies + [candidate]
        vector = build_vector(my_team, enemies, side)
        prob = model.predict_proba([vector])[0][1]
        if side == "dire":
            prob = 1 - prob
        results.append((candidate, prob))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]

with open("heroes.json", "r", encoding="utf-8") as f:
    heroes = json.load(f)
hero_names = {hero["id"]: hero["localized_name"] for hero in heroes}

result = recommendator([14, 86, 78, 67], [129, 56, 51, 123, 90], "radiant")
for hero_id, prob in result:
    print(f"{hero_names[hero_id]}: {round(float(prob) * 100, 1)}%")