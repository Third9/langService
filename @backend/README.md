# LangChain 웹 검색 API

## 필수 요구사항

- Python 3.9 이상 (LangChain 요구사항)
- Google Gemini API 키 (https://ai.google.dev 에서 무료로 발급)

## 환경 설정

1. Python 버전 확인

```bash
python --version
```

2. Python 3.9 이상이 아닌 경우 업그레이드

```bash
# macOS에서 Homebrew 사용시
pyenv install 3.9
```

3. 가상환경 생성 및 활성화

```bash
python -m venv .venv
source .venv/bin/activate
```

4. 의존성 설치

```bash
uv sync
```

5. 환경 변수 설정

`.env` 파일을 생성하고 Google Gemini API 키를 설정합니다:

```bash
cp .env.example .env
# .env 파일을 편집하여 실제 Gemini API 키 입력
```

6. API 키 테스트

```bash
python test_api_key.py
```

성공시 다음과 같은 메시지를 확인할 수 있습니다:

- ✅ Gemini API key found
- ✅ Gemini API key test successful
- 📝 Response from Gemini

오류가 발생하는 경우:

- **401/PERMISSION_DENIED**: 잘못된 API 키 - https://ai.google.dev 에서 새로 발급
- **429/QUOTA_EXCEEDED**: 일일 요청 한도 초과 (1,500회)
- **API_KEY_INVALID**: 잘못된 API 키 형식

## 서버 실행

```bash
uvicorn src.main:app --reload
```

**중요**: 서버 로그에서 API 키 검증 및 오류 정보를 확인하세요.

## 문제 해결

### API 키 관련 문제

1. **API 키 테스트**:

```bash
python test_api_key.py
```

2. **Mock 모드로 테스트** (Gemini 우회):

```bash
USE_MOCK=true uvicorn src.main:app --reload
```

3. **무료 Gemini API 키 발급**:

- https://ai.google.dev 방문
- "Get API Key" 클릭
- Google 계정으로 로그인
- API 키 생성 (완전 무료!)

## API 엔드포인트

- `/search` (POST): 웹 검색 수행 및 요약 반환

## cURL 사용 예시

```bash
# 기본 웹 검색
curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "2024년 최신 AI 트렌드"}'

# 특정 주제 검색
curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "헬스케어 분야 머신러닝 발전"}'
```

### 응답 예시

```json
{
  "results": [
    {
      "title": "AI in Healthcare",
      "link": "https://example.com/ai-healthcare",
      "snippet": "Recent advancements in machine learning are transforming healthcare..."
    }
  ],
  "summary": "머신러닝은 진단 정확도 향상, 개인화된 치료 계획, 예측 의료 분석을 통해 헬스케어를 혁신하고 있습니다."
}
```
