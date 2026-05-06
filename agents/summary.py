"""
Summary Agent
- 입력: Search Agent의 검색 결과
- 출력: 핵심 사실 리스트 (메타데이터 포함)
"""

import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def summary_agent(search_results: list[dict]) -> list[dict]:
    """
    검색 결과에서 핵심 사실을 추출하고 메타데이터를 보존한다.

    Args:
        search_results: Search Agent의 출력

    Returns:
        list[dict]: [
            {
                "fact": "핵심 사실 한 문장",
                "source_url": "출처 URL",
                "source_title": "출처 제목",
                "search_query": "어떤 쿼리로 찾은 정보인지"
            },
            ...
        ]
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    today = datetime.now().strftime("%Y년 %m월 %d일")

    system_prompt = f"""당신은 비즈니스 뉴스 브리핑 시스템의 Summary Agent입니다.
오늘 날짜는 {today}입니다.

수행할 작업:
주어진 기사 하나에서 비즈니스 의사결정에 도움되는 핵심 사실들을 추출하세요.

추출 규칙:
- 각 사실은 1-2 문장으로 간결하게
- 구체적인 수치, 날짜, 회사명 등을 포함
- 추측이나 의견은 배제하고 사실만 기술
- 한 기사에서 1-3개의 핵심 사실 추출 (기사 분량에 따라)
- 중요도가 낮은 정보는 제외

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "facts": [
    "핵심 사실 1",
    "핵심 사실 2"
  ]
}}"""

    all_facts = []

    for query_result in search_results:
        query = query_result["query"]

        for article in query_result["results"]:
            user_prompt = f"""기사 제목: {article['title']}
기사 내용: {article['content']}

위 기사에서 핵심 사실들을 추출해주세요."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]

            try:
                response = llm.invoke(messages)
                result = json.loads(response.content)

                # 각 사실에 메타데이터 추가
                for fact in result.get("facts", []):
                    all_facts.append(
                        {
                            "fact": fact,
                            "source_url": article["url"],
                            "source_title": article["title"],
                            "search_query": query,
                        }
                    )
            except (json.JSONDecodeError, Exception) as e:
                print(f"    ⚠️ 추출 실패: {article['title'][:30]}...")
                continue

    return all_facts


# 테스트용 코드
if __name__ == "__main__":
    from dotenv import load_dotenv
    from planner import planner_agent
    from search import search_agent

    load_dotenv()

    keyword = "삼성전자"
    print(f"🎯 키워드: {keyword}\n")

    # 1단계: Planner
    print("📋 [1/3] Planner Agent...")
    plan = planner_agent(keyword)
    print(f"   ✓ 쿼리 {len(plan['queries'])}개 생성")

    # 2단계: Search
    print(f"\n🔍 [2/3] Search Agent...")
    search_results = search_agent(plan["queries"])
    total_articles = sum(len(item["results"]) for item in search_results)
    print(f"   ✓ {total_articles}개 기사 수집")

    # 3단계: Summary
    print(f"\n📝 [3/3] Summary Agent 실행 중...")
    facts = summary_agent(search_results)
    print(f"   ✓ {len(facts)}개의 핵심 사실 추출\n")

    # 결과 미리보기
    print("=" * 60)
    print("추출된 핵심 사실 (상위 5개)")
    print("=" * 60)
    for i, fact in enumerate(facts[:5], 1):
        print(f"\n[{i}] {fact['fact']}")
        print(f"    출처: {fact['source_title'][:50]}...")
        print(f"    쿼리: {fact['search_query']}")
