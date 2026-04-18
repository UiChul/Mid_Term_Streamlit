import json
import os


DB_FILE = "user_data/users.json"

def load_users():
    if not os.path.exists("user_data"):
        os.makedirs("user_data")
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user(user_id, user_info):
    users = load_users()
    users[user_id] = user_info
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
        
RANKING_FILE = "user_data/users.json"

def get_rankings():
    """랭킹 데이터를 가져와서 점수 순으로 정렬하여 반환합니다."""
    if not os.path.exists(RANKING_FILE):
        return []
    with open(RANKING_FILE, "r", encoding="utf-8") as f:
        try:
            rankings = json.load(f)
            # 맞춘 갯수(count) 기준 내림차순 정렬
            return sorted(rankings, key=lambda x: x['count'], reverse=True)
        except:
            return []

def save_ranking(user_id, count):
    """새로운 랭킹 기록을 저장합니다."""
    rankings = get_rankings()
    rankings.append({"id": user_id, "count": count})
    with open(RANKING_FILE, "w", encoding="utf-8") as f:
        json.dump(rankings, f, indent=4, ensure_ascii=False)