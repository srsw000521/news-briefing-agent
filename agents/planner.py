"""
Planner Agent
- 입력: 사용자 키워드 (예: "삼성전자")
- 출력: 검색 쿼리 리스트 + 예상 카테고리
"""

import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def planner_agent(keyword: str) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 현재 날짜 주입
    today = datetime.now().strftime("%Y년 %m월 %d일")
    current_year = datetime.now().year

    system_prompt = f"""당신은 비즈니스 뉴스 브리핑 시스템의 Planner Agent입니다.
오늘 날짜는 {today}입니다. 모든 검색은 현재 시점({current_year}년) 기준의 최신 정보를 찾는 것이 목표입니다.

수행할 작업:

1. 검색 쿼리 6-8개 생성
   - 구체적이고 세부적인 검색어
   - 다양한 비즈니스 측면을 폭넓게 커버
   - 같은 주제라도 여러 각도에서 검색
   - 연도가 필요한 경우 반드시 {current_year}년 또는 "최근"을 사용
   - 예: "삼성전자 {current_year}년 실적", "삼성전자 최근 신제품"

2. 카테고리 3-4개 정의
   - 검색 결과를 묶어서 보여줄 큰 분류
   - 추상적이고 포괄적인 그룹
   - 여러 쿼리의 결과가 하나의 카테고리에 모일 수 있음
   - 예: "재무 성과", "제품 및 기술", "시장 및 투자", "조직 및 전략"

중요: 쿼리는 많고 구체적으로, 카테고리는 적고 포괄적으로 만드세요.

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "queries": ["쿼리1", "쿼리2", ...],
  "categories": ["카테고리1", "카테고리2", ...]
}}"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"키워드: {keyword}"),
    ]

    response = llm.invoke(messages)

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        print("⚠️ JSON 파싱 실패, 원본 응답:")
        print(response.content)
        return {"queries": [keyword], "categories": ["일반"]}

    return result


# 테스트용 코드
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    keyword = "삼성전자"
    print(f"🎯 키워드: {keyword}\n")

    plan = planner_agent(keyword)

    print("📋 검색 쿼리:")
    for i, query in enumerate(plan["queries"], 1):
        print(f"  {i}. {query}")

    print("\n📂 예상 카테고리:")
    for i, category in enumerate(plan["categories"], 1):
        print(f"  {i}. {category}")
