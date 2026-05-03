import requests
from config import TELEGRAM_TOKEN, CHAT_ID


def send_start_report(matches_count, picks, status="🟢 BOT RUNNING"):

    top_pick = picks[0] if picks else None

    msg = f"""
🤖 BOT STATUS REPORT

Status: {status}

📊 Matches detected: {matches_count}
🎯 Picks generated: {len(picks)}

"""

    if top_pick:
        msg += f"""
🔥 TOP PICK

{top_pick['match']}
Odds: {top_pick['odds']}
Prob: {round(top_pick['prob']*100,1)}%
Value: {round(top_pick['value']*100,1)}%
Score: {round(top_pick['score'],3)}
"""

    else:
        msg += "\n⚠️ No picks generated"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })
