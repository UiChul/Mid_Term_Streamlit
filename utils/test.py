import json
import os


RANKING_FILE = "user_data/ranking.json"

def get_rankings():
    """랭킹 데이터를 가져와서 점수 순으로 정렬하여 반환합니다."""
    if not os.path.exists(RANKING_FILE):
        return []
    with open(RANKING_FILE, "r", encoding="utf-8") as f:
        rankings = json.load(f)
        print(rankings)
    
get_rankings()
        
