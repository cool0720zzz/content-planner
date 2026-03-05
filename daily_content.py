"""
매일 아침 콘텐츠 기획안을 생성해서 Gmail로 발송하는 스크립트
- OpenAI API → 오늘의 시장 뉴스 수집 + 기획안 생성
- Gmail SMTP → 본인에게 이메일 발송
"""

import smtplib
import os
from openai import OpenAI
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ── 설정 ──────────────────────────────────────────────
OPENAI_API_KEY   = os.environ["OPENAI_API_KEY"]
GMAIL_ADDRESS    = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PW     = os.environ["GMAIL_APP_PW"]
RECIPIENT_EMAIL  = os.environ.get("RECIPIENT_EMAIL", GMAIL_ADDRESS)
# ─────────────────────────────────────────────────────

WEEKDAY_KR = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]


def generate_content_plan() -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    today  = datetime.now()
    date_str    = today.strftime("%Y년 %m월 %d일")
    weekday_str = WEEKDAY_KR[today.weekday()]

    prompt = f"""
오늘은 {date_str} {weekday_str}입니다.

당신은 미국 증시를 공부하는 "동네 허술한 형" 컨셉의 한국어 SNS 크리에이터 콘텐츠 기획 어시스턴트입니다.

[컨셉 설명]
- 전문가처럼 굴지 않고, 동네 형이 카페에서 툭툭 던지는 말투
- 어려운 용어를 쓰되 바로 옆에 쉽게 풀어줌 (모르는 사람도 이해 가능)
- 가끔 허당미 있게 "나도 처음엔 몰랐음 ㅋㅋ" 류의 공감 유도
- AI로 이 모든 걸 자동화하고 있다는 걸 가끔 흘림 (AI 비즈니스 컨셉 연결)
- 진지한 정보 + 피식하는 반전 댓글 조합

[타겟 독자]
- 미국 주식 처음이거나 뉴스 봐도 뭔 말인지 모르는 사람
- 시장 참여는 하는데 제대로 해석 못하는 사람
- AI로 뭔가 해보고 싶은 사람

오늘자 미국 증시 마감 데이터와 주요 뉴스를 검색해서 아래 형식으로 기획안을 작성하세요.

---

📅 {date_str} ({weekday_str}) 콘텐츠 기획안
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏦 오늘의 시장 핵심
• 마감 지수 요약: S&P500 / NASDAQ / DOW / VIX 수치와 등락률
• 오늘의 핵심 이슈 1줄
• 초보자 해석 포인트: 이게 왜 중요한지 1~2줄 (쉽게)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 스레드 포스팅 3개 초안
(실제로 올릴 수 있게 완성된 문장으로. 말투는 "동네 허술한 형" 스타일)
(전문 용어 나오면 바로 옆에 괄호로 쉽게 설명)
(끝에 짧은 질문이나 공감 유도 문장 포함)

[1] 역사 비교형 — "n년 전 같은 상황, QQQ 들고 있었다면?"
- 오늘 시장과 유사한 과거 시점 찾기
- 그때 QQQ(나스닥 100 추종 ETF, 쉽게 말하면 미국 기술주 모음) 들고 있었다면 어떤 일이 있었는지
- 허술한 형 말투로 작성
- 끝: "당신은 버텼을까요, 나가 떨어졌을까요?" 류 질문
→ 본문 (200자 내외):
→ 댓글 (피식 웃기는 한 줄):

[2] 숫자 공감형 — "월 10만원씩 적립했다면?"
- 1번과 연결된 ETF/지수 기준
- 그 시점부터 월 10만원씩 적립투자 했을 때 현재 수익 계산 (실제 숫자로)
- "나 이거 보고 진짜 시작했음 ㅋㅋ" 류 허당미 포함
- 끝: 짧은 질문
→ 본문 (200자 내외):
→ 댓글 (피식 웃기는 한 줄):

[3] 의외의 사실형 — "이거 아세요?"
- 오늘 시장에서 일반인이 모를 만한 인과관계 1개
- 진지하게 설명하되 말투는 허술하게
- 끝: 짧은 질문
→ 본문 (200자 내외):
→ 댓글 (본문 내용을 피식 비틀어서. 예: "전기차가 기름 먹고 크던가? 😏"):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📸 인스타 카드뉴스 기획
오늘 미증시 마감 이슈 기반으로:
• 오늘의 핵심 이슈: [한 줄]
• 관련 키워드 3개: [키워드1 / 키워드2 / 키워드3]
• 각 키워드가 시장에 주는 영향 1줄씩:
  - 키워드1:
  - 키워드2:
  - 키워드3:
• 카드 구성안 (5장):
  1장: 오늘의 이슈 한 줄 임팩트
  2장: 키워드1 — 뜻 + 시장 영향
  3장: 키워드2 — 뜻 + 시장 영향
  4장: 키워드3 — 뜻 + 시장 영향
  5장: 정리 + 내일 주목할 것
• 해시태그 추천: #...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI 비즈니스 한 줄 흘리기
오늘 콘텐츠 어딘가에 자연스럽게 녹일 수 있는
"AI로 이걸 자동화하고 있음" 류의 한 줄 멘트 제안:
(스레드 본문 끝이나 댓글에 가볍게 붙일 수 있는 문장)
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 미증시 뉴스레터 한 줄 흘리기
오늘 콘텐츠 어딘가에 자연스럽게 녹일 수 있는
"미증시 뉴스레터 서비스를 제공하고 있음" 류의 한 줄 멘트 제안:
(스레드 본문 끝이나 댓글에 가볍게 붙일 수 있는 문장)
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": "당신은 미국 증시를 공부하는 허술한 형 컨셉의 한국어 SNS 크리에이터 기획 어시스턴트입니다. 전문 용어는 쓰되 바로 옆에 쉽게 풀어주고, 말투는 동네 형처럼 친근하고 가끔 허당미 있게 작성합니다."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def send_email(content: str):
    today       = datetime.now()
    date_str    = today.strftime("%m/%d")
    weekday_str = WEEKDAY_KR[today.weekday()]
    subject     = f"📅 {date_str} ({weekday_str}) 오늘의 콘텐츠 기획안"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = RECIPIENT_EMAIL

    msg.attach(MIMEText(content, "plain", "utf-8"))

    html_content = content.replace("\n", "<br>").replace("━", "─")
    html_body = f"""
    <html><body style="font-family: 'Apple SD Gothic Neo', sans-serif;
                       max-width: 640px; margin: 0 auto; padding: 24px;
                       color: #1a1a1a; line-height: 1.8;">
      <div style="background:#f8f9fa; border-radius:12px; padding:24px;">
        {html_content}
      </div>
      <p style="color:#999; font-size:12px; margin-top:24px; text-align:center;">
        자동 생성된 콘텐츠 기획안입니다. Powered by GPT-4o + GitHub Actions
      </p>
    </body></html>
    """
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PW)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

    print(f"✅ 발송 완료 → {RECIPIENT_EMAIL}")


if __name__ == "__main__":
    print("🔍 오늘의 콘텐츠 기획안 생성 중...")
    plan = generate_content_plan()
    print(plan)
    print("\n📧 이메일 발송 중...")
    send_email(plan)
