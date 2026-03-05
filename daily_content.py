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
    """OpenAI API로 오늘의 콘텐츠 기획안 생성"""

    client = OpenAI(api_key=OPENAI_API_KEY)
    today  = datetime.now()
    date_str    = today.strftime("%Y년 %m월 %d일")
    weekday_str = WEEKDAY_KR[today.weekday()]

    prompt = f"""
오늘은 {date_str} {weekday_str}입니다.

당신은 다음 두 가지 주제로 한국어 콘텐츠를 운영하는 크리에이터의 콘텐츠 기획 어시스턴트입니다.

[운영 채널]
- 스레드(Threads): 매일 참여 유도 포스팅
- 인스타그램: 주 3회 카드뉴스
- 블로그: 주 1회 롱폼 아티클
- 뉴스레터: 주 1회 심층 분석

[핵심 주제]
1. 미국 증시 — 초보자도 스스로 시장을 읽을 수 있도록 돕는 콘텐츠
2. AI 비즈니스 — AI를 활용해 시드 없이도 비즈니스를 설계하고 자동화하는 방법

[타겟 독자]
- 미국 주식을 처음 시작하거나 어디서 공부해야 할지 모르는 사람
- 시장에 참여하고 있지만 정보를 제대로 해석 못하는 사람
- AI로 업무/비즈니스를 바꾸고 싶은 사람

웹에서 오늘자 미국 증시 관련 주요 뉴스와 AI/테크 비즈니스 트렌드를 검색하고,
아래 형식으로 오늘의 콘텐츠 기획안을 작성해주세요.

---

📅 {date_str} ({weekday_str}) 콘텐츠 기획안
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏦 오늘의 시장 핵심
• [핵심 뉴스 1줄 요약]
• 초보자 해석 포인트: [이걸 왜 알아야 하는지 1~2줄]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 스레드 포스팅 3개 초안
(각각 150자 내외, 끝에 질문 또는 공감 유도 문장 포함)

[1] 참여유도형
(내용)

[2] 정보/인사이트형
(내용)

[3] 공감/스토리형
(내용)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📸 인스타 카드뉴스 주제
• 주제: [제목]
• 구성: 1장~5장 각 장의 핵심 메시지 1줄씩
• 해시태그 추천: #...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 블로그 롱폼 주제 제안
• 제목 후보 3개:
  1.
  2.
  3.
• 추천 제목:
• 목차 구성 (H2 기준 3~5개):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📬 이번 주 뉴스레터 각도
• 메인 주제:
• 도입부 후킹 문장:
• 핵심 섹션 구성 (3개):
• CTA:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ 오늘의 우선순위
1순위:
2순위:
3순위:
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": "당신은 미국 증시와 AI 비즈니스 콘텐츠 기획 전문가입니다. 최신 뉴스를 반영해서 실용적인 콘텐츠 기획안을 작성합니다."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def send_email(content: str):
    """Gmail SMTP으로 기획안 발송"""

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
