# src/utils/helpers.py
"""
유틸리티 함수들
"""

import json
from typing import Any, Dict

def safe_json_dumps(obj: Any) -> str:
    """안전한 JSON 직렬화"""
    return json.dumps(obj, ensure_ascii=False, indent=2, default=str)

def safe_json_loads(json_str: str) -> Dict[str, Any]:
    """안전한 JSON 역직렬화"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": f"JSON 파싱 실패: {str(e)}"}

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """두 딕셔너리를 병합합니다."""
    result = dict1.copy()
    result.update(dict2)
    return result
