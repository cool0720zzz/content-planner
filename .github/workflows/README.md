# 📅 매일 아침 콘텐츠 기획안 자동화

매일 오전 7시, Claude가 오늘의 미국 증시 뉴스를 검색하고
스레드/인스타/블로그/뉴스레터 기획안을 Gmail로 보내줍니다.

---

## 📁 파일 구조

```
your-repo/
├── daily_content.py                  # 메인 스크립트
└── .github/
    └── workflows/
        └── daily.yml                 # GitHub Actions 스케줄러
```

---

## 🚀 세팅 방법 (10분이면 끝)

### 1단계. GitHub 레포 만들기

```bash
# 새 레포 만들고 이 파일들 업로드
git init
git add .
git commit -m "init"
git push origin main
```

> 레포는 **Private**으로 설정하세요 (API 키 보호)

---

### 2단계. Gmail 앱 비밀번호 발급

1. Google 계정 → **보안** → **2단계 인증** 활성화
2. **앱 비밀번호** 생성 (앱: 메일, 기기: 기타)
3. 발급된 16자리 비밀번호 복사

---

### 3단계. GitHub Secrets 등록

레포 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret 이름 | 값 |
|------------|-----|
| `ANTHROPIC_API_KEY` | Anthropic API 키 ([발급](https://console.anthropic.com)) |
| `GMAIL_ADDRESS` | 본인 Gmail 주소 |
| `GMAIL_APP_PW` | 2단계에서 발급한 앱 비밀번호 |
| `RECIPIENT_EMAIL` | 기획안 받을 이메일 (보통 본인과 동일) |

---

### 4단계. 테스트 실행

레포 → **Actions** → **매일 아침 콘텐츠 기획안 생성** → **Run workflow**

30초 후 Gmail 확인 📬

---

## ⏰ 스케줄 변경 방법

`daily.yml` 파일의 cron 값 수정:

```yaml
- cron: "0 22 * * *"   # 매일 오전 7시 KST
- cron: "0 23 * * *"   # 매일 오전 8시 KST
- cron: "30 21 * * 1-5" # 평일만 오전 6시 30분 KST
```

---

## 💰 비용

| 항목 | 비용 |
|------|------|
| GitHub Actions | **무료** (월 2,000분 제공) |
| Claude API | 1회 실행 약 **$0.01~0.02** (월 약 $0.3~0.6) |
| Gmail SMTP | **무료** |

---

## 🔧 커스터마이징

`daily_content.py` 안의 프롬프트를 수정하면
기획안 형식, 주제 개수, 포스팅 스타일을 자유롭게 바꿀 수 있어요.

---

## 다음 단계 자동화

- [ ] 스레드 자동 발행 (Threads API)
- [ ] 인스타 카드뉴스 스크립트 자동 생성
- [ ] 뉴스레터 초안 자동 생성 (Substack/스티비 연동)
