"""
Editor Agent
- 입력: 검색 결과 + 카테고리 리스트
- 출력: 카테고리별로 정리된 최종 브리핑
"""

import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def editor_agent(
    keyword: str, search_results: list[dict], categories: list[str]
) -> str:
    """
    검색 결과를 카테고리별로 분류하고 최종 브리핑을 생성한다.

    Args:
        keyword: 원래 키워드 (예: "삼성전자")
        search_results: Search Agent가 수집한 결과
        categories: Planner가 정한 카테고리 리스트

    Returns:
        str: 마크다운 형식의 최종 브리핑
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 검색 결과를 LLM이 읽기 쉽게 텍스트로 변환
    articles_text = ""
    for query_result in search_results:
        for article in query_result["results"]:
            articles_text += f"\n---\n"
            articles_text += f"제목: {article['title']}\n"
            articles_text += f"출처 URL: {article['url']}\n"
            articles_text += f"내용: {article['content']}\n"

    today = datetime.now().strftime("%Y년 %m월 %d일")
    categories_str = ", ".join(categories)

    system_prompt = f"""당신은 비즈니스 뉴스 브리핑 시스템의 Editor Agent입니다.
오늘 날짜는 {today}입니다.

수행할 작업:
1. 주어진 기사들을 분석해서 핵심 정보 추출
2. 각 정보를 다음 카테고리 중 가장 적절한 곳에 분류: {categories_str}
3. 카테고리별로 정리된 마크다운 브리핑 작성

작성 규칙:
- 각 카테고리 안에서 중요도 순으로 bullet point 작성
- 한 bullet은 1-2 문장으로 간결하게
- 출처 URL을 마크다운 링크로 표시: [출처](URL)
- 정보가 없는 카테고리는 출력에서 완전히 생략 (제목도 표시하지 않음)
- 주어진 카테고리 외에 새로운 카테고리를 만들지 마세요
- 비즈니스 의사결정에 도움되는 사실 위주로 작성
- 추측이나 의견은 배제하고 사실만 기술

출력 형식 예시:

위 형식 그대로 마크다운으로 응답하세요. JSON이나 다른 형식은 사용하지 마세요."""

    user_prompt = f"""키워드: {keyword}

수집된 기사들:
{articles_text}

위 기사들을 분석해서 카테고리별 브리핑을 작성해주세요."""

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

    response = llm.invoke(messages)
    return response.content


# 테스트용 코드
if __name__ == "__main__":
    from dotenv import load_dotenv
    from planner import planner_agent
    from search import search_agent

    load_dotenv()

    keyword = "삼성전자"

    # 1단계: Planner
    print(f"🎯 키워드: {keyword}\n")
    print("📋 [1/3] Planner Agent 실행 중...")
    plan = planner_agent(keyword)
    print(
        f"   ✓ 쿼리 {len(plan['queries'])}개, 카테고리 {len(plan['categories'])}개 생성"
    )

    # 2단계: Search
    print(f"\n🔍 [2/3] Search Agent 실행 중...")
    search_results = search_agent(plan["queries"])
    total_articles = sum(len(item["results"]) for item in search_results)
    print(f"   ✓ {total_articles}개 기사 수집")

    # 3단계: Editor
    print(f"\n✏️  [3/3] Editor Agent 실행 중...")
    briefing = editor_agent(keyword, search_results, plan["categories"])
    print(f"   ✓ 브리핑 작성 완료\n")

    # 최종 출력
    print("=" * 60)
    print(briefing)
    print("=" * 60)
