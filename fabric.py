from typing import Dict, Any, Optional, List
import logging
from collections import defaultdict
import json

class FabricConnectionError(Exception):
    pass

class AdaptiveFabric:
    """
    Orchestrator class managing the adaptive fabric connecting AI agents across domains.
    
    Attributes:
        agents: Dictionary mapping agent IDs to their respective Agent instances.
        connections: Dictionary tracking active connections between agents.
        communication_channels: Mapping of channels for inter-agent communication.
        resource_usage: Tracking current resource usage across the fabric.
        status: Current operational status of the fabric.
    """
    
    def __init__(self) -> None:
        self.agents = {}
        self.connections = defaultdict(list)
        self.communication_channels = {}
        self.resource_usage = {'cpu': 0.0, 'memory': 0.0}
        self.status = 'offline'
        self.logger = logging.getLogger("AdaptiveFabric")
        
    def register_agent(self, agent_id: str, domain: str) -> None:
        """Register a new agent with the fabric."""
        if agent_id in self.agents:
            raise FabricConnectionError(f"Agent {agent_id} already registered")
            
        self.agents[agent_id] = AgentBase(agent_id, domain)
        self.logger.info(f"Registered new agent: {agent_id}")
        
    def connect_agents(self, source_agent: str, target_agent: str) -> None:
        """Establish a communication channel between two agents."""
        if source_agent not in self.agents or target_agent not in self.agents:
            raise FabricConnectionError("Agents not found")
            
        # Create a communication channel
        channel = {
            'source': source_agent,
            'target': target_agent,
            'timestamp': datetime.now().isoformat()
        }
        
        self.communication_channels[f"{source_agent}_{target_agent}"] = channel
        self.connections[source_agent].append(target_agent)
        self.connections[target_agent].append(source_agent)
        self.logger.info(f"Established connection between {source_agent} and {target_agent}")
        
    def disconnect_agents(self, source_agent: str, target_agent: str) -> None:
        """Disconnect two agents."""
        if f"{source_agent}_{target_agent}" not in self.communication_channels:
            raise FabricConnectionError("Agents are not connected")
            
        # Remove connection
        del self.communication_channels[f"{source_agent}_{target_agent}"]
        self.connections[source_agent].remove(target_agent)
        self.connections[target_agent].remove(source_agent)
        self.logger.info(f"Disconnected {source_agent} and {target_agent}")
        
    def relay_message(self, source_agent: str, target_agent: str, message: str) -> None:
        """Relay a message through the fabric."""
        if source_agent not in self.agents or target_agent not in self.agents:
            raise FabricConnectionError("Agents not found")
            
        # Check if agents are connected
        if target_agent not in self.connections[source_agent]:
            self.logger.warning(f"No direct connection between {source_agent} and {target_agent}")
            return
            
        self.agents[source