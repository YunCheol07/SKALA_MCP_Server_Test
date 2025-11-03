# src/services/node_recommender.py
"""
노드 추천 서비스
최적의 노드 구조를 제안합니다.
"""

import json
from typing import Dict, List, Any
from uuid import uuid4
from datetime import datetime
from ..config import AVAILABLE_TOOLS, NODE_PATTERNS

class NodeRecommender:
    """노드 구조를 추천하는 클래스"""
    
    def __init__(self):
        self.node_patterns = NODE_PATTERNS
        self.tools = AVAILABLE_TOOLS
    
    def recommend(self,
                  intent: str,
                  required_capabilities: List[str],
                  recommended_tools: List[Dict[str, Any]],
                  complexity_level: str,
                  workflow_type: str) -> Dict[str, Any]:
        """
        분석 결과에 따라 노드 구조를 추천합니다.
        
        Args:
            intent: 주요 의도
            required_capabilities: 필요한 기능 목록
            recommended_tools: 추천 도구 목록
            complexity_level: 복잡도 (low, medium, high)
            workflow_type: 워크플로우 타입
            
        Returns:
            노드 추천 결과
        """
        recommendation = {
            "timestamp": datetime.now().isoformat(),
            "workflow_id": str(uuid4()),
            "workflow_type": workflow_type,
            "pattern": self.node_patterns.get(workflow_type, {}),
            "nodes": [],
            "connections": [],
            "tool_mappings": {},
            "execution_order": [],
            "metadata": {
                "complexity": complexity_level,
                "intent": intent,
                "capability_count": len(required_capabilities),
                "tool_count": len(recommended_tools)
            }
        }
        
        # 기본 노드 생성
        nodes = self._create_base_nodes()
        
        # 도구 기반 프로세스 노드 생성
        process_nodes = self._create_process_nodes(recommended_tools)
        nodes.extend(process_nodes)
        
        # 최종 출력 노드
        nodes.append(self._create_output_node())
        
        # 패턴에 따른 연결 생성
        connections = self._create_connections(nodes, workflow_type)
        
        # 실행 순서 결정
        execution_order = self._determine_execution_order(nodes, connections, workflow_type)
        
        recommendation["nodes"] = nodes
        recommendation["connections"] = connections
        recommendation["tool_mappings"] = {n["id"]: n.get("tool_id") for n in process_nodes}
        recommendation["execution_order"] = execution_order
        
        return recommendation
    
    def _create_base_nodes(self) -> List[Dict[str, Any]]:
        """기본 입력 노드를 생성합니다."""
        return [
            {
                "id": "input_node",
                "name": "입력 수신",
                "type": "start",
                "description": "사용자 입력 또는 외부 데이터 수신",
                "status": "pending"
            }
        ]
    
    def _create_process_nodes(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """도구에 기반한 프로세스 노드를 생성합니다."""
        process_nodes = []
        
        for idx, tool in enumerate(tools, 1):
            node = {
                "id": f"process_node_{idx}",
                "name": tool.get("name", "처리"),
                "type": "process",
                "description": tool.get("description", ""),
                "tool_id": tool.get("id"),
                "tool_schema": tool.get("inputSchema", {}),
                "category": tool.get("category", ""),
                "priority": tool.get("priority", 999),
                "estimated_time_ms": tool.get("estimated_time_ms", 1000),
                "status": "pending",
                "retry_count": 3,
                "timeout_ms": 30000
            }
            process_nodes.append(node)
        
        return process_nodes
    
    def _create_output_node(self) -> Dict[str, Any]:
        """출력 노드를 생성합니다."""
        return {
            "id": "output_node",
            "name": "결과 출력",
            "type": "end",
            "description": "최종 결과 반환",
            "status": "pending"
        }
    
    def _create_connections(self,
                           nodes: List[Dict[str, Any]],
                           workflow_type: str) -> List[Dict[str, Any]]:
        """노드 간 연결을 생성합니다."""
        connections = []
        
        if workflow_type == "sequential":
            connections = self._create_sequential_connections(nodes)
        elif workflow_type == "parallel":
            connections = self._create_parallel_connections(nodes)
        elif workflow_type == "conditional":
            connections = self._create_conditional_connections(nodes)
        elif workflow_type == "loop":
            connections = self._create_loop_connections(nodes)
        else:
            connections = self._create_sequential_connections(nodes)
        
        return connections
    
    def _create_sequential_connections(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """순차 연결을 생성합니다."""
        connections = []
        
        for i in range(len(nodes) - 1):
            connections.append({
                "id": f"conn_{i}",
                "from_node": nodes[i]["id"],
                "to_node": nodes[i + 1]["id"],
                "type": "direct",
                "condition": None
            })
        
        return connections
    
    def _create_parallel_connections(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """병렬 연결을 생성합니다."""
        connections = []
        process_nodes = [n for n in nodes if n["type"] == "process"]
        
        # 입력에서 모든 프로세스로 연결
        for process_node in process_nodes:
            connections.append({
                "id": f"conn_input_to_{process_node['id']}",
                "from_node": "input_node",
                "to_node": process_node["id"],
                "type": "parallel"
            })
        
        # 모든 프로세스에서 출력으로 연결
        for process_node in process_nodes:
            connections.append({
                "id": f"conn_{process_node['id']}_to_output",
                "from_node": process_node["id"],
                "to_node": "output_node",
                "type": "parallel"
            })
        
        return connections
    
    def _create_conditional_connections(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """조건부 연결을 생성합니다."""
        connections = []
        
        # 이 부분은 더 복잡한 로직이 필요하므로
        # 여기서는 기본 구조만 제공
        if len(nodes) > 2:
            connections.append({
                "id": "conn_input_decision",
                "from_node": "input_node",
                "to_node": nodes[1]["id"],
                "type": "conditional",
                "condition": "if_condition"
            })
        
        return connections
    
    def _create_loop_connections(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """반복 연결을 생성합니다."""
        connections = []
        
        if len(nodes) >= 2:
            connections.append({
                "id": "conn_loop_start",
                "from_node": "input_node",
                "to_node": nodes[1]["id"],
                "type": "direct"
            })
            
            # 반복 루프
            if len(nodes) > 2:
                connections.append({
                    "id": "conn_loop_back",
                    "from_node": nodes[-2]["id"],
                    "to_node": nodes[1]["id"],
                    "type": "loop_back",
                    "condition": "while_condition"
                })
        
        return connections
    
    def _determine_execution_order(self,
                                  nodes: List[Dict[str, Any]],
                                  connections: List[Dict[str, Any]],
                                  workflow_type: str) -> List[str]:
        """노드 실행 순서를 결정합니다."""
        
        if workflow_type == "parallel":
            # 병렬: 입력 → 모든 프로세스 동시 → 출력
            process_ids = [n["id"] for n in nodes if n["type"] == "process"]
            return ["input_node"] + process_ids + ["output_node"]
        elif workflow_type == "sequential":
            # 순차: 입력 → 프로세스1 → 프로세스2 → ... → 출력
            return [n["id"] for n in nodes]
        else:
            # 기타: 입력 → 모든 프로세스 → 출력
            return [n["id"] for n in nodes]
