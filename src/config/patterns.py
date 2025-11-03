# src/config/patterns.py
"""
에이전트 흐름 패턴 정의
"""

NODE_PATTERNS = {
    "sequential": {
        "name": "순차 처리",
        "description": "한 단계씩 순서대로 작업을 수행합니다",
        "use_cases": ["데이터 파이프라인", "단계별 처리"],
        "template": ["input", "process_1", "process_2", "output"],
        "parallelizable": False,
        "complexity": "low"
    },
    
    "parallel": {
        "name": "병렬 처리",
        "description": "여러 작업을 동시에 수행합니다",
        "use_cases": ["다중 정보 수집", "독립적 작업 처리"],
        "template": ["input", "branch_1", "branch_2", "merge", "output"],
        "parallelizable": True,
        "complexity": "medium"
    },
    
    "conditional": {
        "name": "조건부 처리",
        "description": "조건에 따라 다른 경로를 실행합니다",
        "use_cases": ["의사결정 기반 작업", "필터링"],
        "template": ["input", "decision", "branch_true", "branch_false", "merge", "output"],
        "parallelizable": False,
        "complexity": "medium"
    },
    
    "loop": {
        "name": "반복 처리",
        "description": "특정 작업을 반복해서 수행합니다",
        "use_cases": ["배치 처리", "크롤링", "데이터 마이그레이션"],
        "template": ["input", "check_condition", "process", "update", "output"],
        "parallelizable": False,
        "complexity": "high"
    },
    
    "hierarchical": {
        "name": "계층적 처리",
        "description": "상위 에이전트가 하위 에이전트를 관리합니다",
        "use_cases": ["복잡한 프로젝트", "다단계 의사결정"],
        "template": ["input", "agent_1", "agent_2", "coordinator", "output"],
        "parallelizable": True,
        "complexity": "high"
    }
}

WORKFLOW_PATTERNS = {
    "data_pipeline": {
        "name": "데이터 파이프라인",
        "description": "데이터 수집 → 처리 → 저장",
        "recommended_flow": "sequential",
        "required_capabilities": ["information_retrieval", "data_processing", "data_access"],
        "typical_nodes": 3,
        "estimated_time_ms": 5000
    },
    
    "analysis_workflow": {
        "name": "분석 워크플로우",
        "description": "데이터 수집 → 분석 → 보고서 생성",
        "recommended_flow": "sequential",
        "required_capabilities": ["information_retrieval", "data_processing", "generation"],
        "typical_nodes": 3,
        "estimated_time_ms": 6000
    },
    
    "multi_source_gathering": {
        "name": "다중 소스 수집",
        "description": "여러 소스에서 동시에 데이터를 수집",
        "recommended_flow": "parallel",
        "required_capabilities": ["information_retrieval"],
        "typical_nodes": 4,
        "estimated_time_ms": 3000
    },
    
    "decision_tree": {
        "name": "의사결정 트리",
        "description": "조건에 따라 다른 작업 수행",
        "recommended_flow": "conditional",
        "required_capabilities": ["data_processing"],
        "typical_nodes": 5,
        "estimated_time_ms": 3000
    }
}
