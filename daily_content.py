"""
매일 아침 콘텐츠 기획안을 생성해서 Gmail로 발송하는 스크립트
- Anthropic Claude API -> 오늘의 시장 뉴스 수집 + 기획안 생성
- Gmail SMTP -> 본인에게 이메일 발송
"""

import anthropic
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# -- 설정 ------------------------------------------------------
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GMAIL_ADDRESS     = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PW      = os.environ["GMAIL_APP_PW"]
RECIPIENT_EMAIL   = os.environ.get("RECIPIENT_EMAIL", GMAIL_ADDRESS)
# --------------------------------------------------------------

WEEKDAY_KR = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]


def generate_content_plan() -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    today  = datetime.now()
    date_str    = today.strftime("%Y년 %m월 %d일")
    weekday_str = WEEKDAY_KR[today.weekday()]

    prompt = (
        f"오늘은 {date_str} {weekday_str}입니다.\n\n"
        "당신은 미국 증시 콘텐츠를 운영하는 SNS 크리에이터의 기획 어시스턴트입니다.\n\n"
        "[캐릭터 설명]\n"
        "- 형이 어쩌고, 형 믿어봐 같은 말 절대 금지\n"
        "- 진지하게 시황 설명하다가 마지막에 긍정적으로 뒤집기\n"
        "- 본문: 시황 설명 + 이거 바겐세일 아님?, 오늘이 딱 그날 아님? 류로 마무리\n"
        "- 댓글: 현실 자폭 공감형. 독자가 읽고 ㅋㅋㅋ 나 얘기네 하는 한 줄\n"
        "  예시: 문제는 내 주머니 😭\n"
        "  예시: 시장이 공포인 게 아니라 내 계좌가 공포임 🤣\n"
        "  예시: 공포에 못 사는 이유는 하나임. 이미 계좌가 비었음...\n"
        "- 전문 용어 쓰되 바로 옆에 쉽게 풀어줌\n"
        "- 좋은 기운, 긍정 에너지. 시장이 힘들어도 유머로 이겨내는 분위기\n\n"
        "[타겟 독자]\n"
        "- 미국 주식 처음이거나 뉴스 봐도 뭔 말인지 모르는 사람\n"
        "- 시장 참여는 하는데 해석이 어려운 사람\n"
        "- 계좌는 작아도 공부하면서 성장하고 싶은 사람\n\n"
        "오늘자 미국 증시 마감 데이터와 주요 뉴스를 웹에서 검색해서 아래 형식으로 기획안을 작성하세요.\n\n"
        "---\n\n"
        f"[{date_str} ({weekday_str}) 콘텐츠 기획안]\n\n"
        "[시장 핵심]\n"
        "- 마감 지수: S&P500 / NASDAQ / DOW / VIX 수치와 등락률\n"
        "- 오늘의 핵심 이슈 1줄\n"
        "- 초보자 해석 포인트: 쉽게 1~2줄\n\n"
        "---\n\n"
        "[스레드 포스팅 3개]\n\n"
        "[1] 역사 비교형\n"
        "오늘 시장과 비슷했던 과거 시점 찾아서,\n"
        "QQQ(나스닥 100 ETF, 미국 기술주 모음) 들고 있었다면 어떤 일이 있었는지.\n"
        "결말은 긍정적으로. 근데 그때 버틴 사람은 지금 웃고 있음 류.\n"
        "끝에 당신은 버텼을까요? 질문.\n"
        "-> 본문:\n"
        "-> 댓글 (현실 자폭 공감 한 줄):\n\n"
        "[2] 숫자 공감형\n"
        "1번과 연결된 시점부터 월 10만원씩 적립했을 때 현재 수익 실제 숫자로.\n"
        "이거 보면 진짜 시작하고 싶어짐 분위기.\n"
        "끝에 짧은 질문.\n"
        "-> 본문:\n"
        "-> 댓글 (현실 자폭 공감 한 줄):\n\n"
        "[3] 긍정 반전형\n"
        "오늘 시황 진지하게 설명하다가 마지막에 뒤집기.\n"
        "떨어지면 어때? 바겐세일 아님? 류.\n"
        "댓글은 현실 자폭으로 웃음 유도.\n"
        "-> 본문:\n"
        "-> 댓글 (현실 자폭 공감 한 줄):\n\n"
        "---\n\n"
        "[인스타 카드뉴스 기획]\n"
        "- 오늘의 핵심 이슈:\n"
        "- 관련 키워드 3개:\n"
        "- 각 키워드 뜻 + 시장 영향 1줄:\n"
        "  키워드1:\n"
        "  키워드2:\n"
        "  키워드3:\n"
        "- 카드 구성 (5장):\n"
        "  1장: 오늘 이슈 임팩트 한 줄\n"
        "  2장: 키워드1\n"
        "  3장: 키워드2\n"
        "  4장: 키워드3\n"
        "  5장: 정리 + 내일 주목할 것\n"
        "- 해시태그:\n\n"
        "---\n\n"
        "[뉴스레터 유입 한 줄 흘리기]\n"
        "스레드 댓글이나 본문 끝에 자연스럽게 붙일 수 있는\n"
        "미증시 뉴스레터 서비스 티 안 나게 녹이는 한 줄 제안:\n"
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )

    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text

    return result


def send_email(content: str):
    today       = datetime.now()
    date_str    = today.strftime("%m/%d")
    weekday_str = WEEKDAY_KR[today.weekday()]
    subject     = f"[{date_str} {weekday_str}] 오늘의 콘텐츠 기획안"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = RECIPIENT_EMAIL

    msg.attach(MIMEText(content, "plain", "utf-8"))

    html_body = f"""
    <html><body style="font-family: 'Apple SD Gothic Neo', sans-serif;
                       max-width: 640px; margin: 0 auto; padding: 24px;
                       color: #1a1a1a; line-height: 1.8;">
      <div style="background:#f8f9fa; border-radius:12px; padding:24px;">
        {content.replace(chr(10), "<br>")}
      </div>
      <p style="color:#999; font-size:12px; margin-top:24px; text-align:center;">
        자동 생성된 콘텐츠 기획안 | Powered by Claude + GitHub Actions
      </p>
    </body></html>
    """
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PW)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

    print(f"발송 완료 -> {RECIPIENT_EMAIL}")


if __name__ == "__main__":
    print("오늘의 콘텐츠 기획안 생성 중...")
    plan = generate_content_plan()
    print(plan)
    print("\n이메일 발송 중...")
    send_email(plan)
