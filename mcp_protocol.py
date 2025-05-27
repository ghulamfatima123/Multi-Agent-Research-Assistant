"""
Simplified MCP (Model Context Protocol) implementation for agent communication
"""
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class MCPMessage:
    """MCP message format"""
    id: str
    method: str #what action
    params: Dict[str, Any] #data
    timestamp: float
    agent_from: str
    agent_to: str

class MCPAgent(ABC):
    """Base MCP Agent with communication capabilities"""
    
    def __init__(self, name: str):
        self.name = name
        self.message_log = []
    
    def send_message(self, to_agent: str, method: str, params: Dict[str, Any]) -> MCPMessage:
        """Send MCP message to another agent"""
        message = MCPMessage(
            id=f"{self.name}_{int(time.time() * 1000)}",
            method=method,
            params=params,
            timestamp=time.time(),
            agent_from=self.name,
            agent_to=to_agent
        )
        self.message_log.append(message)
        print(f" {self.name} → {to_agent}: {method}")
        return message
    
    def receive_message(self, message: MCPMessage) -> Dict[str, Any]:
        """Receive and process MCP message"""
        self.message_log.append(message)
        print(f" {self.name} ← {message.agent_from}: {message.method}")
        return self.handle_request(message.method, message.params)
    
    @abstractmethod
    def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming request"""
        pass
    
    @abstractmethod
    def run(self, input_data: Any) -> str:
        """Main execution method"""
        pass
