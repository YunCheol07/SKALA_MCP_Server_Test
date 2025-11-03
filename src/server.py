# src/server.py
"""
Agent Builder MCP 서버의 메인 서버 코드
"""

# src/server.py
import json
import os
import sys
from pathlib import Path

# Python 경로 설정
sys.path.insert(0, str(Path(__file__).parent))

from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv

# ✓ 절대 import로 변경
from config import AVAILABLE_TOOLS, NODE_PATTERNS
from services import PromptAnalyzer, NodeRecommender, WorkflowOptimizer

# 환경 변수 로드
load_dotenv()

# FastMCP 서버 초기화
mcp = FastMCP(
    name="AgentBuilder",
    instructions=(
        "당신은 Agent Builder 어시스턴트입니다. "
        "사용자의 프롬프트를 분석하여 에이전트 흐름을 설계하고, "
        "최적의 노드 구조를 추천하며, 워크플로우를 최적화합니다. "
        "복잡한 AI 에이전트 워크플로우 구축을 지원합니다."
    ),
)

# 서비스 인스턴스 생성
analyzer = PromptAnalyzer()
recommender = NodeRecommender()
optimizer = WorkflowOptimizer()

# ============================================================================
# 도구 1: 프롬프트 분석
# ============================================================================

@mcp.tool()
def analyze_prompt(user_prompt: str) -> str:
    """
    사용자 프롬프트를 분석하여 필요한 에이전트 기능을 파악합니다.
    
    Args:
        user_prompt: 사용자의 에이전트 요청 텍스트
        
    Returns:
        분석 결과 JSON 문자열
    """
    try:
        analysis = analyzer.analyze(user_prompt)
        return json.dumps(analysis, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "message": "프롬프트 분석 중 오류 발생"
        }, ensure_ascii=False)

# ============================================================================
# 도구 2: 노드 구조 추천
# ============================================================================

@mcp.tool()
def recommend_nodes(
    intent: str,
    required_capabilities: list,
    complexity_level: str = "medium",
    workflow_type: str = "sequential"
) -> str:
    """
    분석 결과에 따라 최적의 노드 구조를 추천합니다.
    
    Args:
        intent: 주요 의도 (search, analyze, generate, etc.)
        required_capabilities: 필요한 기능 목록
        complexity_level: 복잡도 (low, medium, high)
        workflow_type: 워크플로우 타입 (sequential, parallel, conditional, loop)
        
    Returns:
        노드 추천 결과 JSON 문자열
    """
    try:
        # 추천 도구 선택
        recommended_tools = []
        for capability in required_capabilities:
            category_tools = AVAILABLE_TOOLS
            for tool_name, tool_info in category_tools.items():
                if tool_info.get("category") == capability:
                    tool_copy = tool_info.copy()
                    tool_copy["id"] = tool_name
                    recommended_tools.append(tool_copy)
        
        # 노드 추천
        recommendation = recommender.recommend(
            intent=intent,
            required_capabilities=required_capabilities,
            recommended_tools=recommended_tools,
            complexity_level=complexity_level,
            workflow_type=workflow_type
        )
        
        return json.dumps(recommendation, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "message": "노드 추천 중 오류 발생"
        }, ensure_ascii=False)

# ============================================================================
# 도구 3: 워크플로우 최적화
# ============================================================================

@mcp.tool()
def optimize_workflow(
    workflow_json: str,
    optimization_goal: str = "speed"
) -> str:
    """
    워크플로우를 최적화합니다.
    
    Args:
        workflow_json: 최적화할 워크플로우의 JSON 문자열
        optimization_goal: 최적화 목표 (speed, cost, reliability)
        
    Returns:
        최적화 결과 JSON 문자열
    """
    try:
        workflow = json.loads(workflow_json)
        optimized = optimizer.optimize(workflow, optimization_goal)
        return json.dumps(optimized, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Invalid JSON format",
            "message": "워크플로우 JSON 형식이 올바르지 않습니다"
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "message": "워크플로우 최적화 중 오류 발생"
        }, ensure_ascii=False)

# ============================================================================
# 도구 4: 사용 가능한 도구 목록 조회
# ============================================================================

@mcp.tool()
def get_available_tools() -> str:
    """
    사용 가능한 모든 도구와 그 설정을 반환합니다.
    
    Returns:
        사용 가능한 도구 목록 JSON 문자열
    """
    try:
        tools_with_ids = {}
        for tool_name, tool_info in AVAILABLE_TOOLS.items():
            tool_copy = tool_info.copy()
            tool_copy["id"] = tool_name
            tools_with_ids[tool_name] = tool_copy
        
        return json.dumps(tools_with_ids, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "message": "도구 목록 조회 중 오류 발생"
        }, ensure_ascii=False)

# ============================================================================
# 도구 5: 노드 패턴 정보 조회
# ============================================================================

@mcp.tool()
def get_node_patterns() -> str:
    """
    사용 가능한 노드 패턴과 각 패턴의 설명을 반환합니다.
    
    Returns:
        노드 패턴 정보 JSON 문자열
    """
    try:
        return json.dumps(NODE_PATTERNS, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "message": "패턴 정보 조회 중 오류 발생"
        }, ensure_ascii=False)

# ============================================================================
# 리소스: 서버 정보
# ============================================================================

@mcp.resource("info://server")
def get_server_info() -> dict:
    """Agent Builder 서버의 정보를 제공합니다."""
    return {
        "name": "AgentBuilder MCP Server",
        "version": "1.0.0",
        "description": "에이전트 흐름 설계 및 노드 추천 시스템",
        "tools_available": list(AVAILABLE_TOOLS.keys()),
        "patterns_available": list(NODE_PATTERNS.keys())
    }

@mcp.resource("info://capabilities")
def get_capabilities() -> dict:
    """서버의 주요 기능을 나열합니다."""
    return {
        "prompt_analysis": "사용자 프롬프트 분석",
        "node_recommendation": "최적 노드 구조 추천",
        "workflow_optimization": "워크플로우 최적화",
        "tool_discovery": "사용 가능한 도구 조회",
        "pattern_information": "노드 패턴 정보 제공"
    }

# ============================================================================
# 서버 시작
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # 디버그 모드 설정
    debug = os.getenv("SERVER_DEBUG", "false").lower() == "true"
    
    if debug:
        print("Agent Builder MCP Server 시작 (디버그 모드)", file=sys.stderr)
    
    mcp.run(transport="stdio")
