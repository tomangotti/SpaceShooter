

#posting score

def post_score(SCORE):
    import requests
    url = "https://gaminghub.onrender.com/high_score_boards"
    data = {"name": "TEST", "score": SCORE, "game_id": 1}
    response1 = requests.post(url, data=data)
