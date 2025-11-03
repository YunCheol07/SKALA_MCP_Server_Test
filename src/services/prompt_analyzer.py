# src/services/prompt_analyzer.py
"""
프롬프트 분석 서비스
사용자의 요청을 분석하여 필요한 기능을 파악합니다.
"""

import json
from typing import Dict, List, Any
from datetime import datetime
from ..config import AVAILABLE_TOOLS, TOOL_CATEGORIES

class PromptAnalyzer:
    """사용자 프롬프트를 분석하는 클래스"""
    
    # 의도별 키워드 매핑
    INTENT_KEYWORDS = {
        "search": ["찾다", "검색", "조사", "search", "find", "look", "locate"],
        "analyze": ["분석", "분석하다", "평가", "평가하다", "analyze", "evaluate"],
        "retrieve": ["가져오다", "검색", "찾기", "수집", "retrieve", "gather", "fetch"],
        "execute": ["실행", "수행", "처리", "실시", "execute", "run", "perform"],
        "generate": ["생성", "만들다", "작성", "생성하다", "create", "generate", "write"],
        "aggregate": ["통합", "합치다", "모으다", "통합하다", "aggregate", "combine", "merge"],
        "compare": ["비교", "비교하다", "대비", "compare", "contrast"],
        "forecast": ["예측", "예측하다", "추측", "예보", "forecast", "predict", "estimate"]
    }
    
    def __init__(self):
        self.tool_database = AVAILABLE_TOOLS
        self.tool_categories = TOOL_CATEGORIES
    
    def analyze(self, user_prompt: str) -> Dict[str, Any]:
        """
        사용자 프롬프트를 분석합니다.
        
        Args:
            user_prompt: 사용자의 요청 텍스트
            
        Returns:
            분석 결과 딕셔너리
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "original_prompt": user_prompt,
            "intent_analysis": {
                "primary_intent": "",
                "sub_intents": [],
                "confidence": 0.0,
                "complexity_level": ""
            },
            "required_capabilities": [],
            "recommended_tools": [],
            "estimated_workflow_type": "",
            "analysis_details": {}
        }
        
        # 프롬프트 전처리
        keywords = user_prompt.lower().split()
        prompt_length = len(keywords)
        
        # 의도 감지
        detected_intents = self._detect_intents(keywords)
        analysis["intent_analysis"]["primary_intent"] = detected_intents[0] if detected_intents else "unknown"
        analysis["intent_analysis"]["sub_intents"] = detected_intents[1:]
        analysis["intent_analysis"]["confidence"] = min(1.0, len(detected_intents) / 3)
        
        # 복잡도 판단 (프롬프트 길이 기반)
        if prompt_length > 50:
            complexity = "high"
            analysis["intent_analysis"]["complexity_level"] = "high"
        elif prompt_length > 25:
            complexity = "medium"
            analysis["intent_analysis"]["complexity_level"] = "medium"
        else:
            complexity = "low"
            analysis["intent_analysis"]["complexity_level"] = "low"
        
        # 필요한 기능 식별
        required_capabilities = self._identify_capabilities(keywords, user_prompt)
        analysis["required_capabilities"] = required_capabilities
        
        # 추천 도구 선택
        recommended_tools = self._select_tools(required_capabilities)
        analysis["recommended_tools"] = recommended_tools
        
        # 워크플로우 타입 결정
        workflow_type = self._determine_workflow_type(
            len(recommended_tools),
            complexity,
            user_prompt
        )
        analysis["estimated_workflow_type"] = workflow_type
        
        analysis["analysis_details"] = {
            "prompt_word_count": prompt_length,
            "detected_intent_keywords": detected_intents,
            "tool_count": len(recommended_tools),
            "capability_count": len(required_capabilities)
        }
        
        return analysis
    
    def _detect_intents(self, keywords: List[str]) -> List[str]:
        """키워드에서 의도를 감지합니다."""
        detected = []
        
        for intent, words in self.INTENT_KEYWORDS.items():
            if any(word in keywords for word in words):
                detected.append(intent)
        
        return detected
    
    def _identify_capabilities(self, keywords: List[str], full_prompt: str) -> List[str]:
        """필요한 기능을 식별합니다."""
        capabilities = set()
        
        # 키워드 기반 기능 식별
        search_keywords = ["검색", "search", "찾다", "find", "정보", "information"]
        if any(word in full_prompt.lower() for word in search_keywords):
            capabilities.add("information_retrieval")
        
        analysis_keywords = ["분석", "analyze", "통계", "statistics", "계산", "calculate"]
        if any(word in full_prompt.lower() for word in analysis_keywords):
            capabilities.add("data_processing")
        
        code_keywords = ["코드", "code", "파이썬", "python", "실행", "execute"]
        if any(word in full_prompt.lower() for word in code_keywords):
            capabilities.add("computation")
        
        database_keywords = ["데이터베이스", "database", "저장", "저장소", "query"]
        if any(word in full_prompt.lower() for word in database_keywords):
            capabilities.add("data_access")
        
        generate_keywords = ["생성", "generate", "작성", "write", "만들다", "create"]
        if any(word in full_prompt.lower() for word in generate_keywords):
            capabilities.add("generation")
        
        return list(capabilities)
    
    def _select_tools(self, capabilities: List[str]) -> List[Dict[str, Any]]:
        """필요한 도구를 선택합니다."""
        selected_tools = []
        
        for capability in capabilities:
            if capability in self.tool_categories:
                tool_names = self.tool_categories[capability]
                for tool_name in tool_names:
                    if tool_name in self.tool_database:
                        tool_info = self.tool_database[tool_name].copy()
                        tool_info["id"] = tool_name
                        selected_tools.append(tool_info)
        
        # 우선순위로 정렬
        selected_tools.sort(key=lambda x: x.get("priority", 999))
        
        return selected_tools
    
    def _determine_workflow_type(self, tool_count: int, complexity: str, prompt: str) -> str:
        """워크플로우 타입을 결정합니다."""
        
        # 병렬 작업 키워드 감지
        parallel_keywords = ["동시에", "simultaneously", "동시", "parallel", "and"]
        has_parallel = any(word in prompt.lower() for word in parallel_keywords)
        
        # 조건부 처리 키워드 감지
        conditional_keywords = ["만약", "if", "그러면", "조건", "경우에", "depending"]
        has_conditional = any(word in prompt.lower() for word in conditional_keywords)
        
        # 반복 처리 키워드 감지
        loop_keywords = ["반복", "loop", "계속", "매번", "각각", "all"]
        has_loop = any(word in prompt.lower() for word in loop_keywords)
        
        if has_loop:
            return "loop"
        elif has_conditional:
            return "conditional"
        elif has_parallel and tool_count > 1:
            return "parallel"
        else:
            return "sequential"
