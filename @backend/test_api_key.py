#!/usr/bin/env python3
"""
Google Gemini API 키 유효성 테스트 스크립트
"""
import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def test_gemini_api_key():
    """Google Gemini API 키 테스트"""
    # .env 파일 로드
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("💡 .env 파일에 GEMINI_API_KEY=your_key_here 를 추가하세요.")
        print("🌐 무료 API 키는 https://ai.google.dev 에서 받을 수 있습니다.")
        return False
    
    print(f"✅ Gemini API 키 발견 (길이: {len(api_key)})")
    print(f"🔑 API 키 시작: {api_key[:7]}...")
    
    try:
        # Gemini 클라이언트 초기화
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            max_tokens=50,
            google_api_key=api_key
        )
        
        print("🔄 Gemini API 키 유효성 테스트 중...")
        
        # 간단한 테스트 호출
        response = llm.invoke("Say 'Hello, Gemini API test successful!'")
        
        print("✅ Gemini API 키 테스트 성공!")
        print(f"📝 응답: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API 키 테스트 실패: {type(e).__name__}")
        print(f"💬 에러 메시지: {str(e)}")
        
        if "401" in str(e) or "Unauthorized" in str(e) or "PERMISSION_DENIED" in str(e):
            print("💡 API 키가 유효하지 않습니다. https://ai.google.dev 에서 새 키를 받으세요.")
        elif "429" in str(e) or "quota" in str(e) or "QUOTA_EXCEEDED" in str(e):
            print("💡 일일 사용량 한도(1,500 requests)를 초과했습니다. 내일 다시 시도하세요.")
        elif "API_KEY_INVALID" in str(e):
            print("💡 잘못된 API 키 형식입니다. 올바른 Gemini API 키인지 확인하세요.")
        
        return False

if __name__ == "__main__":
    print("🚀 Google Gemini API 키 테스트 시작")
    print("=" * 50)
    
    success = test_gemini_api_key()
    
    print("=" * 50)
    if success:
        print("🎉 모든 테스트 통과! FastAPI 서버를 시작할 수 있습니다.")
        sys.exit(0)
    else:
        print("💥 API 키 문제가 있습니다. 위의 지침을 따라 해결하세요.")
        sys.exit(1)