# News Briefing Multi-Agent System

LangGraph 기반 멀티 에이전트 시스템으로, 키워드를 입력하면
뉴스를 자동 수집·요약·분류해 카테고리별 브리핑을 생성합니다.

## Architecture

- **Planner Agent**: 검색 쿼리 분해
- **Search Agent**: 웹 검색 Tool 호출 및 뉴스 수집
- **Summary Agent**: 핵심 내용 추출
- **Editor Agent**: 카테고리별 브리핑 생성

## Stack

- LangGraph
- Claude API (Anthropic)
- Tavily Search API

## Status

🚧 Work in progress