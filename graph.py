"""
LangGraph로 멀티 에이전트 시스템 오케스트레이션
- Planner → Search → Editor 흐름
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from agents.planner import planner_agent
from agents.search import search_agent
from agents.editor import editor_agent


# 모든 Agent가 공유하는 상태 정의
class BriefingState(TypedDict):
    keyword: str  # 사용자 입력 키워드
    queries: list[str]  # Planner가 생성한 검색 쿼리
    categories: list[str]  # Planner가 정한 카테고리
    search_results: list[dict]  # Search가 수집한 결과
    briefing: str  # Editor가 작성한 최종 브리핑


# === 각 노드 함수 정의 ===


def planner_node(state: BriefingState) -> dict:
    """Planner Agent 실행"""
    print("\n📋 [1/3] Planner Node 실행 중...")
    plan = planner_agent(state["keyword"])
    print(
        f"   ✓ 쿼리 {len(plan['queries'])}개, 카테고리 {len(plan['categories'])}개 생성"
    )

    # State 업데이트할 부분만 반환
    return {"queries": plan["queries"], "categories": plan["categories"]}


def search_node(state: BriefingState) -> dict:
    """Search Agent 실행"""
    print("\n🔍 [2/3] Search Node 실행 중...")
    results = search_agent(state["queries"])
    total = sum(len(item["results"]) for item in results)
    print(f"   ✓ {total}개 기사 수집")

    return {"search_results": results}


def editor_node(state: BriefingState) -> dict:
    """Editor Agent 실행"""
    print("\n✏️  [3/3] Editor Node 실행 중...")
    briefing = editor_agent(
        keyword=state["keyword"],
        search_results=state["search_results"],
        categories=state["categories"],
    )
    print(f"   ✓ 브리핑 작성 완료")

    return {"briefing": briefing}


# === 그래프 빌드 ===


def build_graph():
    """LangGraph 그래프를 구성하고 컴파일"""
    workflow = StateGraph(BriefingState)

    # 노드 추가
    workflow.add_node("planner", planner_node)
    workflow.add_node("search", search_node)
    workflow.add_node("editor", editor_node)

    # 엣지 정의 (흐름)
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "search")
    workflow.add_edge("search", "editor")
    workflow.add_edge("editor", END)

    return workflow.compile()


# === 실행 ===

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    keyword = input("🎯 키워드를 입력하세요: ").strip() or "삼성전자"

    print(f"\n{'='*60}")
    print(f"   비즈니스 뉴스 브리핑 생성 - '{keyword}'")
    print(f"{'='*60}")

    # 그래프 컴파일
    graph = build_graph()

    # 초기 상태로 실행
    initial_state = {"keyword": keyword}
    final_state = graph.invoke(initial_state)

    # 결과 출력
    print(f"\n{'='*60}")
    print(final_state["briefing"])
    print(f"{'='*60}")
