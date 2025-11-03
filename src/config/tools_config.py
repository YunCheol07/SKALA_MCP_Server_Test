# src/config/tools_config.py
"""
사용 가능한 도구들의 설정 데이터베이스
"""

AVAILABLE_TOOLS = {
    # 정보 검색 카테고리
    "web_search": {
        "category": "information_retrieval",
        "name": "웹 검색",
        "description": "웹에서 실시간 정보를 검색합니다",
        "priority": 1,
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색 쿼리"
                },
                "max_results": {
                    "type": "integer",
                    "description": "최대 결과 수",
                    "default": 10
                }
            },
            "required": ["query"]
        },
        "dependencies": [],
        "estimated_time_ms": 2000
    },
    
    "document_retrieve": {
        "category": "information_retrieval",
        "name": "문서 검색",
        "description": "저장된 문서 데이터베이스에서 정보를 검색합니다",
        "priority": 2,
        "inputSchema": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "string",
                    "description": "검색 키워드"
                },
                "doc_type": {
                    "type": "string",
                    "description": "문서 타입 (pdf, txt, docx)",
                    "enum": ["pdf", "txt", "docx", "all"]
                }
            },
            "required": ["keywords"]
        },
        "dependencies": [],
        "estimated_time_ms": 1000
    },
    
    # 데이터 처리 카테고리
    "data_analysis": {
        "category": "data_processing",
        "name": "데이터 분석",
        "description": "데이터 분석 및 통계 계산을 수행합니다",
        "priority": 2,
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "description": "분석할 데이터"
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["statistical", "trend", "comparison"],
                    "description": "분석 유형"
                }
            },
            "required": ["data", "analysis_type"]
        },
        "dependencies": [],
        "estimated_time_ms": 1500
    },
    
    "code_execution": {
        "category": "computation",
        "name": "코드 실행",
        "description": "Python 코드를 안전하게 실행합니다",
        "priority": 3,
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "실행할 Python 코드"
                },
                "timeout": {
                    "type": "integer",
                    "description": "타임아웃 (초)",
                    "default": 30
                }
            },
            "required": ["code"]
        },
        "dependencies": [],
        "estimated_time_ms": 3000
    },
    
    # 데이터 접근 카테고리
    "database_query": {
        "category": "data_access",
        "name": "데이터베이스 쿼리",
        "description": "데이터베이스에서 데이터를 조회합니다",
        "priority": 2,
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL 쿼리"
                },
                "database": {
                    "type": "string",
                    "description": "데이터베이스 이름"
                }
            },
            "required": ["query", "database"]
        },
        "dependencies": [],
        "estimated_time_ms": 2000
    },
    
    "api_call": {
        "category": "data_access",
        "name": "API 호출",
        "description": "외부 REST API를 호출합니다",
        "priority": 2,
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "API URL"
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE"],
                    "description": "HTTP 메서드",
                    "default": "GET"
                },
                "payload": {
                    "type": "object",
                    "description": "요청 바디"
                }
            },
            "required": ["url"]
        },
        "dependencies": [],
        "estimated_time_ms": 2000
    },
    
    # 생성 카테고리
    "content_generation": {
        "category": "generation",
        "name": "콘텐츠 생성",
        "description": "텍스트 콘텐츠를 생성합니다",
        "priority": 3,
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "생성 프롬프트"
                },
                "style": {
                    "type": "string",
                    "description": "텍스트 스타일"
                },
                "length": {
                    "type": "string",
                    "enum": ["short", "medium", "long"],
                    "description": "생성할 텍스트 길이"
                }
            },
            "required": ["prompt"]
        },
        "dependencies": ["data_analysis"],
        "estimated_time_ms": 3000
    }
}

# 카테고리별 도구 그룹
TOOL_CATEGORIES = {
    "information_retrieval": ["web_search", "document_retrieve"],
    "data_processing": ["data_analysis"],
    "computation": ["code_execution"],
    "data_access": ["database_query", "api_call"],
    "generation": ["content_generation"]
}
