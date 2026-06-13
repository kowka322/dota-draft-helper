import streamlit as st
import joblib
import json

model = joblib.load("model.joblib")
hero_to_index = joblib.load("hero_to_index.joblib")

with open("heroes.json", "r", encoding="utf-8") as f:
    heroes = json.load(f)

hero_names = {hero["id"]: hero["localized_name"] for hero in heroes}
name_to_id = {hero["localized_name"]: hero["id"] for hero in heroes}



