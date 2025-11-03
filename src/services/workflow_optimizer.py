# src/services/workflow_optimizer.py
"""
워크플로우 최적화 서비스
생성된 워크플로우를 최적화합니다.
"""

import json
from typing import Dict, List, Any
from datetime import datetime

class WorkflowOptimizer:
    """워크플로우를 최적화하는 클래스"""
    
    def optimize(self,
                workflow: Dict[str, Any],
                optimization_goal: str = "speed") -> Dict[str, Any]:
        """
        워크플로우를 최적화합니다.
        
        Args:
            workflow: 워크플로우 정보
            optimization_goal: 최적화 목표 (speed, cost, reliability)
            
        Returns:
            최적화된 워크플로우
        """
        optimized = {
            "timestamp": datetime.now().isoformat(),
            "original_workflow_id": workflow.get("workflow_id"),
            "optimization_goal": optimization_goal,
            "recommendations": [],
            "optimized_workflow": workflow.copy(),
            "improvement_metrics": {}
        }
        
        if optimization_goal == "speed":
            optimized["recommendations"] = self._optimize_for_speed(workflow)
            optimized["improvement_metrics"] = {
                "potential_speedup": "30-50%",
                "focus": "병렬 처리 및 캐싱"
            }
        
        elif optimization_goal == "cost":
            optimized["recommendations"] = self._optimize_for_cost(workflow)
            optimized["improvement_metrics"] = {
                "potential_savings": "20-40%",
                "focus": "API 호출 수 감소"
            }
        
        elif optimization_goal == "reliability":
            optimized["recommendations"] = self._optimize_for_reliability(workflow)
            optimized["improvement_metrics"] = {
                "reliability_improvement": "99%+",
                "focus": "오류 처리 및 재시도"
            }
        
        return optimized
    
    def _optimize_for_speed(self, workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
        """속도 최적화 추천사항을 반환합니다."""
        recommendations = []
        
        connections = workflow.get("connections", [])
        sequential_count = sum(1 for c in connections if c.get("type") == "direct")
        
        if sequential_count > 1:
            recommendations.append({
                "type": "parallelization",
                "priority": "high",
                "description": "독립적인 노드들을 병렬 처리로 변경",
                "implementation": "현재 순차 노드 중 독립적인 노드를 병렬 실행",
                "estimated_improvement": "30-50%",
                "implementation_complexity": "medium"
            })
        
        recommendations.append({
            "type": "caching",
            "priority": "high",
            "description": "자주 사용되는 데이터 캐싱",
            "implementation": "반복 요청 데이터에 메모리 캐시 추가",
            "estimated_improvement": "20-40% (반복 요청 시)",
            "implementation_complexity": "low"
        })
        
        recommendations.append({
            "type": "async_execution",
            "priority": "medium",
            "description": "비동기 처리 도입",
            "implementation": "I/O 바운드 작업을 async/await로 변경",
            "estimated_improvement": "15-25%",
            "implementation_complexity": "medium"
        })
        
        return recommendations
    
    def _optimize_for_cost(self, workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
        """비용 최적화 추천사항을 반환합니다."""
        recommendations = []
        
        nodes = workflow.get("nodes", [])
        api_call_nodes = [n for n in nodes if "api" in n.get("tool_id", "").lower()]
        
        if len(api_call_nodes) > 1:
            recommendations.append({
                "type": "tool_consolidation",
                "priority": "high",
                "description": "여러 API 호출을 단일 배치 호출로 통합",
                "implementation": "API 호출 수를 50%까지 감소",
                "estimated_savings": "40-50%",
                "implementation_complexity": "high"
            })
        
        recommendations.append({
            "type": "batch_processing",
            "priority": "high",
            "description": "개별 요청을 배치 처리로 변경",
            "implementation": "여러 작은 요청을 하나의 큰 배치로 처리",
            "estimated_savings": "30-40%",
            "implementation_complexity": "medium"
        })
        
        recommendations.append({
            "type": "model_downgrade",
            "priority": "medium",
            "description": "고급 모델을 필요에 따라 더 저렴한 모델로 다운그레이드",
            "implementation": "간단한 작업에는 더 저렴한 모델 사용",
            "estimated_savings": "20-30%",
            "implementation_complexity": "low"
        })
        
        return recommendations
    
    def _optimize_for_reliability(self, workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
        """신뢰성 최적화 추천사항을 반환합니다."""
        recommendations = []
        
        nodes = workflow.get("nodes", [])
        
        recommendations.append({
            "type": "error_handling",
            "priority": "high",
            "description": "각 노드에 오류 처리 및 재시도 로직 추가",
            "implementation": "try-except 블록 및 exponential backoff 재시도 추가",
            "reliability_gain": "95%+",
            "implementation_complexity": "low"
        })
        
        recommendations.append({
            "type": "fallback_paths",
            "priority": "high",
            "description": "각 노드의 실패 시 대체 경로 추가",
            "implementation": "대체 도구 또는 데이터 소스 지정",
            "reliability_gain": "99%+",
            "implementation_complexity": "medium"
        })
        
        recommendations.append({
            "type": "monitoring_alerts",
            "priority": "medium",
            "description": "실시간 모니터링 및 알림 시스템 추가",
            "implementation": "각 노드의 성공/실패 로깅 및 알림",
            "reliability_gain": "faster recovery",
            "implementation_complexity": "medium"
        })
        
        recommendations.append({
            "type": "input_validation",
            "priority": "high",
            "description": "입력 데이터 검증 강화",
            "implementation": "스키마 검증 및 데이터 정제",
            "reliability_gain": "prevent errors",
            "implementation_complexity": "low"
        })
        
        return recommendations
