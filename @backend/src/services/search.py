import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self):
        # Google Gemini API 키 확인
        api_key = os.getenv('GEMINI_API_KEY')
        force_mock = os.getenv('USE_MOCK') == 'true'

        logger.info(f"Gemini API Key 존재: {bool(api_key)}")
        logger.info(f"API Key 길이: {len(api_key) if api_key else 0}")
        logger.info(f"Force Mock: {force_mock}")

        # Mock 강제 모드가 아니고 API 키가 있으면 실제 Gemini 사용
        self.use_mock = force_mock or not bool(api_key)

        logger.info(f"최종 use_mock 결정: {self.use_mock}")

        if not self.use_mock:
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0.3,
                    max_tokens=500,
                    google_api_key=api_key
                )
                logger.info("Gemini 클라이언트 초기화 성공")

                # API 키 유효성 테스트
                self._test_api_key()

            except Exception as e:
                logger.error(f"Gemini 클라이언트 초기화 실패: {e}")
                self.use_mock = True

    def _test_api_key(self):
        """Gemini API 키 유효성 테스트"""
        try:
            logger.info("Gemini API 키 유효성 테스트 시작...")
            response = self.llm.invoke("Hello")
            logger.info(f"API 키 테스트 성공: {response.content[:50]}...")
        except Exception as e:
            logger.error(f"API 키 테스트 실패: {type(e).__name__}: {str(e)}")
            raise e

    def search_and_summarize(self, query: str) -> tuple[list, str]:
        """질문에 대한 AI 답변 생성"""

        if self.use_mock:
            # Mock 응답 (API 키 문제시 사용)
            mock_response = f"""This is a mock response for: "{query}"

            Since this is a demo service, here are some key points about your question:
            • This would normally be answered by AI
            • The service is working correctly
            • You can test the API structure

            To use real AI responses, please check your OpenAI API key and billing."""

            fake_results = [{
                "title": "Mock AI Response",
                "link": "#mock",
                "snippet": "Demo response - API working correctly"
            }]

            return fake_results, mock_response

        # 실제 Gemini API 호출
        try:
            logger.info(f"Gemini API 호출 시작 - query: {query}")

            prompt = f"""Please provide a comprehensive and informative answer to the following question:

            Question: {query}

            Please provide a detailed response with key points and relevant information."""

            response = self.llm.invoke(prompt)
            logger.info("Gemini API 호출 성공")

            fake_results = [{
                "title": "Gemini AI Generated Response",
                "link": "#",
                "snippet": "AI-powered answer from Google Gemini"
            }]

            return fake_results, response.content

        except Exception as e:
            # API 에러 상세 로깅
            logger.error(f"Gemini API 호출 실패: {type(e).__name__}: {str(e)}")
            logger.error(f"에러 발생 위치: search_and_summarize, query: {query}")

            # 500 에러로 처리하지 않고 에러 정보를 포함한 응답 반환
            error_response = f"Gemini API Error occurred: {str(e)}\n\nThis is a fallback response for: '{query}'"

            error_results = [{
                "title": "Error - Fallback Response",
                "link": "#error",
                "snippet": "Gemini API temporarily unavailable"
            }]

            return error_results, error_response