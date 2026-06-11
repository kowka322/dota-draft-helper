from collections.abc import Iterator
from decorators import retry_on_429
import requests
import json 
import time


@retry_on_429()
def fetch_one_page(less_than_match_id=None):
    url = "https://api.opendota.com/api/publicMatches"
    params = {"mmr_descending": 1}
    if less_than_match_id:
        params["less_than_match_id"] = less_than_match_id
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def is_valid_match(match):
    if match["duration"] == 0:
        return False
    if match["lobby_type"] != 7:
        return False
    if match["game_mode"] != 22:
        return False
    if 0 in match["radiant_team"]:
        return False
    if 0 in match["dire_team"]:
        return False
    if match["num_rank_tier"] < 6:
        return False
    if match["avg_rank_tier"] < 71:
        return False
    return True


def save_to_json(matches, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
        
        
        
def fetch_all_pages(target_count: int = 5000) -> Iterator[dict]:
    seen_id = set()
    less_than_match_id = None
    count = 0
    while count < target_count:
        page = fetch_one_page(less_than_match_id)
        
        time.sleep(1)
        
        if not page:
            print("API empty")
            break
        
        if not isinstance(page, list):
            print(f"API returned non-list: {page}")
            break


        less_than_match_id = page[-1]["match_id"]
        
        for match in page:
            if match["match_id"] in seen_id:
                continue
            seen_id.add(match["match_id"])
            
            if is_valid_match(match):
                yield match
                count += 1
                print(f"collected: {count}")
            if count >= target_count:
                return

class  JsonSaver:
    def __init__(self, filename: str, save_every: int = 50):
        self.filename = filename
        self.save_every = save_every
        self.matches = []
    
    def __enter__(self):
        return self
    
    
    
    def add(self, match: dict) -> None:
        self.matches.append(match)
        if len(self.matches) % self.save_every == 0:
            save_to_json(self.matches, self.filename)
            

    def __exit__(self, exc_type, exc, tb):
        save_to_json(self.matches, self.filename)
    

if __name__ == "__main__":
    with JsonSaver("raw_matches.json") as saver:
        for match in fetch_all_pages(5000):
            saver.add(match)