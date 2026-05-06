import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 환경변수 로드
load_dotenv()

# 도구 준비
search_tool = TavilySearchResults(max_results=3, search_depth="basic")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 1단계: 검색
keyword = "리멤버 AI Lab"
print(f"🔍 검색 중: '{keyword}'\n")
results = search_tool.invoke(keyword)

# 2단계: 검색 결과를 하나의 텍스트로 합치기
search_context = "\n\n".join(
    [f"[기사 {i+1}] {r['title']}\n{r['content']}" for i, r in enumerate(results)]
)

# 3단계: LLM에게 요약 요청
print("🤖 LLM이 요약 중...\n")

messages = [
    SystemMessage(
        content="당신은 비즈니스 뉴스 브리핑 작성 전문가입니다. 주어진 기사들을 바탕으로 핵심 내용을 3-5개 bullet point로 요약해주세요."
    ),
    HumanMessage(content=f"다음 기사들을 요약해주세요:\n\n{search_context}"),
]

response = llm.invoke(messages)

# 결과 출력
print("=" * 50)
print(f"📰 '{keyword}' 비즈니스 브리핑")
print("=" * 50)
print(response.content)
