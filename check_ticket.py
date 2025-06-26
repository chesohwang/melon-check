import requests
import os
from slack_sdk.webhook import WebhookClient

# 환경변수에서 슬랙 Webhook 주소 가져오기
webhook_url = os.getenv("SLACK_WEBHOOK_URL")
webhook = WebhookClient(webhook_url)

# 기본 설정
product_id = "211408"
schedule_ids = ["100001", "100002", "100003"]  # 7월 4,5,6일
poc_code = "SC0002"
corp_code_no = ""

for schedule_id in schedule_ids:
    url = "https://ticket.melon.com/tktapi/product/seat/seatGradeList.json"
    payload = {
        "prodId": product_id,
        "scheduleNo": schedule_id,
        "pocCode": poc_code,
        "corpCodeNo": corp_code_no
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://ticket.melon.com/",
        "Origin": "https://ticket.melon.com"
    }

    res = requests.post(url, data=payload, headers=headers)
    if res.status_code == 200:
        result = res.json()
        for item in result.get("summary", []):
            seat_name = item.get("seatGradeName")
            cnt = item.get("realSeatCntlk", 0)
            if cnt > 0:
                msg = f"🎫 티켓 떴어요!\n일정: {schedule_id}\n좌석: {seat_name}\n잔여: {cnt}석"
                webhook.send(text=msg)
                print(msg)
    else:
        print(f"[에러] 일정 {schedule_id} → API 실패: {res.status_code}")
