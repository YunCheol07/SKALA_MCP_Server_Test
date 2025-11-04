***

# Agent Builder MCP Server

에이전트 흐름 초안 및 노드 구조를 **자동 추천**하고 개발을 지원하는 MCP 서버입니다. Claude Code 및 LangGraph/LangChain과 연동하여 복잡한 AI 에이전트 워크플로우 생성 자동화를 제공합니다.

## 주요 기능

- **프롬프트 분석:** 사용자의 요구를 분석하여 필요한 도구 및 흐름 파악
- **노드 추천:** 의도/기능/복잡도 기반 최적 노드 구조 및 연결 자동 설계
- **워크플로우 최적화:** 속도/비용/신뢰성 목표에 맞춰 자동 최적화 제안
- **도구 목록/패턴 제공:** Agent 설계에 필요한 모든 컴포넌트 정보 API 제공

## 폴더 구조

```
agent-builder-mcp/
└── src/
    ├── __init__.py
    ├── server.py
    ├── config/
    │   ├── __init__.py
    │   ├── tools_config.py
    │   └── patterns.py
    ├── services/
    │   ├── __init__.py
    │   ├── prompt_analyzer.py
    │   ├── node_recommender.py
    │   └── workflow_optimizer.py
    └── utils/
        ├── __init__.py
        └── helpers.py
├── tests/
│   ├── __init__.py
│   └── test_services.py
├── requirements.txt
├── .env
├── .env.example
├── pyproject.toml
├── .gitignore
├── README.md
└── setup.sh
```

## 설치 및 실행

1. **가상환경 생성 및 활성화**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

2. **의존성 설치**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **환경 변수 설정**
   - `.env.example` 기반으로 `.env` 생성 후, 필요한 API 키 등 수정

4. **서버 실행**
   ```bash
   python -m src.server
   ```
   - 최초 실행 시 정상적으로 FastMCP 서버 화면이 나오면 성공!

## 주요 서버 진입점/구현 설명

- **src/server.py**
  - FastMCP 기반 MCP 서버 진입점
  - MCP 도구 등록: `analyze_prompt`, `recommend_nodes`, `optimize_workflow`, `get_available_tools`, `get_node_patterns`
- **src/config/tools_config.py**
  - MCP에서 제공할 도구의 스키마, 설명, 의존 정보 등 DB화
- **src/config/patterns.py**
  - 흐름/노드 패턴 정의 (순차, 병렬, 조건, 반복 등)
- **src/services/prompt_analyzer.py**
  - 프롬프트 의도 및 기능 분석, 필요한 도구/캡빌리티 자동 추출
- **src/services/node_recommender.py**
  - 분석 결과 기반, 실제 노드 및 연결 설계 자동 추천
- **src/services/workflow_optimizer.py**
  - 목표(속도/비용/신뢰성)별 워크플로우 최적화 로직

## .gitignore 주요 항목

- 가상환경, 캐시, 로그, 환경변수 파일, MCP 캐싱 등 모두 제외

## Claude MCP 서버 연동법

1. MCP 서버 실행
2. 새로운 터미널에서:
   ```bash
   claude mcp add --scope user agent-builder python -m src.server
   claude mcp list
   claude mcp get agent-builder
   ```
3. Claude Code에서 워크플로우 설계 자동화 도구 사용

## 예시 사용 흐름

1. Claude에서 프롬프트 입력:
   ```
   "특정 고객의 구매 이력과 관심사를 분석해서 자동으로 추천 상품 워크플로우를 설계해줘"
   ```
2. MCP 서버가 필수 노드・흐름・최적화 제안 제공
3. LangGraph 기반 자동 상태 그래프 생성/실행 가능

## 요구사항

- Python 3.9+
- FastMCP, MCP, LangChain, LangGraph 등 requirements.txt 참고

## 참고

- FastMCP Docs: https://gofastmcp.com
- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- Claude Code Docs: https://docs.anthropic.com/claude

***
