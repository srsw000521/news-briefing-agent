# 🤖 News Briefing Multi-Agent System

LangGraph 기반 멀티 에이전트 시스템으로, 키워드를 입력하면 비즈니스 뉴스를 자동으로 수집·분류·요약해 카테고리별 브리핑을 생성합니다.

## 🎯 Project Goal

비즈니스 뉴스 검색은 단순히 키워드로 검색하는 것만으로는 충분하지 않습니다. 다양한 측면(실적, 제품, 시장, 전략)을 폭넓게 수집하고, 의미 있는 카테고리로 분류해야 의사결정에 도움이 되는 정보가 됩니다.

이 프로젝트는 이 과정을 4개의 전문화된 Agent가 협력하는 멀티 에이전트 시스템으로 풀어냅니다.

## Architecture

<p align="center">
  <img src="docs/images.png" alt="Architecture Diagram" width="700"/>
</p>

각 Agent는 LangGraph의 노드로 정의되며, TypedDict 기반 공유 State를 통해 데이터를 주고받습니다.

## Key Features

- **역할 분리 설계**: 각 Agent가 단일 책임을 가지도록 분리해 디버깅과 확장이 용이
- **동적 카테고리 주입**: Planner가 정한 카테고리가 Editor의 SystemMessage에 동적으로 주입되어 새로운 도메인에 자동 적응
- **현재 시점 인지**: LLM의 학습 데이터 시점 한계를 보정하기 위해 시스템 시간을 SystemMessage에 주입
- **출처 추적 가능**: 모든 정보에 출처 URL이 마크다운 링크로 보존
- **장애 감내**: 일부 검색 실패 시에도 전체 흐름이 중단되지 않음

## 🛠 Tech Stack

- **LangGraph**: 멀티 에이전트 오케스트레이션
- **LangChain**: LLM 호출 및 Tool 통합
- **OpenAI API**: 각 Agent의 LLM 백엔드
- **Tavily Search API**: 웹 검색 Tool
- **Python 3.10+**