"""
Search Agent
- 입력: 검색 쿼리 리스트
- 출력: 각 쿼리별 검색 결과 모음
"""

from langchain_community.tools.tavily_search import TavilySearchResults


def search_agent(queries: list[str], max_results_per_query: int = 3) -> list[dict]:
    """
    여러 쿼리를 받아서 각각 검색을 수행한다.

    Args:
        queries: 검색할 쿼리 리스트
        max_results_per_query: 쿼리당 가져올 검색 결과 개수

    Returns:
        list[dict]: [
            {
                "query": "검색 쿼리",
                "results": [
                    {"title": "...", "url": "...", "content": "..."},
                    ...
                ]
            },
            ...
        ]
    """
    search_tool = TavilySearchResults(
        max_results=max_results_per_query, search_depth="basic"
    )

    all_results = []

    for i, query in enumerate(queries, 1):
        print(f"  [{i}/{len(queries)}] 검색 중: {query}")

        try:
            results = search_tool.invoke(query)
            all_results.append({"query": query, "results": results})
        except Exception as e:
            print(f"    ⚠️ 검색 실패: {e}")
            all_results.append({"query": query, "results": []})

    return all_results


# 테스트용 코드
if __name__ == "__main__":
    from dotenv import load_dotenv
    from planner import planner_agent

    load_dotenv()

    # 1단계: Planner로 검색 전략 수립
    keyword = "삼성전자"
    print(f"🎯 키워드: {keyword}\n")

    print("📋 [Planner Agent] 검색 전략 수립 중...")
    plan = planner_agent(keyword)

    print(f"\n생성된 쿼리 {len(plan['queries'])}개:")
    for i, q in enumerate(plan["queries"], 1):
        print(f"  {i}. {q}")

    # 2단계: Search Agent로 검색 실행
    print(f"\n🔍 [Search Agent] 검색 실행 중...")
    search_results = search_agent(plan["queries"])

    # 결과 요약 출력
    print(f"\n✅ 검색 완료!")
    total_articles = sum(len(item["results"]) for item in search_results)
    print(f"   총 {len(search_results)}개 쿼리에서 {total_articles}개 기사 수집\n")

    # 첫 번째 쿼리 결과만 미리보기
    if search_results and search_results[0]["results"]:
        print("=" * 50)
        print(f"📰 미리보기: '{search_results[0]['query']}'")
        print("=" * 50)
        for j, article in enumerate(search_results[0]["results"], 1):
            print(f"\n[{j}] {article['title']}")
            print(f"    URL: {article['url']}")
            print(f"    내용: {article['content'][:150]}...")
