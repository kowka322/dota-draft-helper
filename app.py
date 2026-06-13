import joblib
import json
import streamlit as st

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


hero_positions = {
    "1": [1, 4, 6, 8, 9, 10, 11, 12, 15, 18, 19, 21, 25, 32, 35, 41, 42, 44, 46, 47, 48, 49, 53, 54, 56, 63, 67, 70, 72, 73, 75, 77, 80, 81, 89, 92, 93, 94, 95, 102, 104, 109, 114, 136, 138, 145],
    "2": [4, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 19, 21, 22, 23, 25, 26, 29, 30, 32, 34, 35, 36, 38, 39, 40, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 56, 57, 59, 61, 62, 63, 64, 65, 68, 71, 73, 74, 75, 76, 77, 78, 80, 81, 82, 84, 86, 88, 90, 91, 92, 94, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 109, 110, 111, 112, 113, 114, 119, 120, 126, 128, 131, 135, 136, 137, 138, 145],
    "3": [2, 7, 14, 15, 16, 18, 19, 23, 26, 28, 29, 33, 36, 38, 42, 43, 47, 49, 51, 54, 55, 57, 59, 60, 65, 69, 71, 73, 77, 78, 80, 81, 84, 85, 92, 96, 97, 98, 99, 100, 102, 103, 104, 106, 107, 108, 110, 128, 129, 135, 136, 137],
    "4-5": [3, 7, 9, 14, 16, 18, 19, 20, 21, 22, 25, 26, 27, 30, 31, 37, 40, 45, 47, 50, 51, 53, 55, 56, 57, 58, 62, 63, 64, 65, 66, 68, 71, 73, 75, 79, 83, 84, 85, 86, 87, 88, 90, 91, 97, 100, 101, 102, 103, 105, 110, 111, 112, 119, 121, 123, 128, 131, 136, 137],
}


def recommendator(allies, enemies, side, position=None):
    taken = set(allies) | set(enemies)
    candidates = [hero_id for hero_id in hero_to_index if hero_id not in taken]
    
    if position is not None:
        candidates = [hero_id for hero_id in candidates if hero_id in hero_positions[position]]
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
name_to_id = {hero["localized_name"]: hero["id"] for hero in heroes}


st.title("Dota 2 Draft Helper")
all_hero_names = sorted(name_to_id.keys())
allies = st.multiselect("Your team", all_hero_names)
enemies = st.multiselect("Enemy team", all_hero_names)
side = st.radio("Your side", ["radiant", "dire"])
position = st.selectbox("Position to fill", ["Any", "1", "2", "3", "4-5"])

if st.button("Recommend"):
    ally_ids = [name_to_id[name] for name in allies]
    enemy_ids = [name_to_id[name] for name in enemies]

    pos = None if position == "Any" else position

    result = recommendator(ally_ids, enemy_ids, side, position=pos)

    st.subheader("Recommended picks:")
    for hero_id, prob in result:
        st.write(f"{hero_names[hero_id]}: {round(float(prob) * 100, 1)}%")