from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import json
from typing import Protocol

class AgentInterface(Protocol):
    @abstractmethod
    def send_message(self, recipient: str, message: str) -> None:
        pass

    @abstractmethod
    def receive_message(self) -> Optional[str]:
        pass

class AgentBase:
    """
    Base class for all AI agents in the ecosystem. Implements core functionalities like initialization,
    runtime management, communication, logging, and resource tracking.
    
    Attributes:
        agent_id: Unique identifier of the agent.
        domain: Domain this agent operates in (e.g., 'nlp', 'vision').
        communication_channel: Channel used for inter-agent communication.
        resources: Dictionary tracking resource usage.
        status: Current operational status of the agent.
    """
    
    def __init__(self, agent_id: str, domain: str) -> None:
        self.agent_id = agent_id
        self.domain = domain
        self.communication_channel = None  # Will be set by Fabric
        self.resources = {
            'cpu_usage': 0.0,
            'memory_usage': 0.0,
            'active_connections': 0
        }
        self.status = 'idle'
        self.logger = logging.getLogger(f"Agent_{agent_id}")
        
    def __del__(self) -> None:
        """Cleanup resources when the agent is destroyed."""
        self.deactivate()
        
    def activate(self) -> None:
        """Activate the agent and start its runtime cycle."""
        if self.status == 'active':
            return
            
        # Initialize logging
        self.logger.info("Agent is activating")
        self.status = 'activating'
        
        try:
            self._runtime_loop()
            self.status = 'active'
        except Exception as e:
            self.logger.error(f"Activation failed: {str(e)}")
            self.status = 'error'

    def deactivate(self) -> None:
        """Deactivate the agent and clean up resources."""
        if self.status == 'inactive':
            return
            
        self.logger.info("Agent is deactivating")
        self.status = 'deactivating'
        
        try:
            # Release resources
            if self.communication_channel:
                self.communication_channel.close()
                
            self.status = 'inactive'
        except Exception as e:
            self.logger.error(f"Deactivation failed: {str(e)}")
            self.status = 'error'

    def send_message(self, recipient: str, message: str) -> None:
        """Send a message to another agent via the communication channel."""
        try:
            if not self.communication_channel:
                raise RuntimeError("Communication channel not initialized")
                
            self.logger.debug(f"Sending message to {recipient}: {message}")
            self.communication_channel.send((recipient, message))
        except Exception as e:
            self.logger.error(f"Failed to send message: {str(e)}")

    def receive_message(self) -> Optional[str]:
        """Receive and process a message from the communication channel."""
        try:
            if not self.communication_channel:
                raise RuntimeError("Communication channel not initialized")
                
            message = self.communication_channel.recv()
            if not message:
                return None
                
            recipient, content = message
            if recipient != self.agent_id:
                raise ValueError("Received message for wrong agent")
                
            self.logger.debug(f"Received message: {content}")
            return content
        except Exception as e:
            self.logger.error(f"Failed to receive message: {str(e)}")
            return None

    def _runtime_loop(self) -> None:
        """Core runtime loop of the agent. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement runtime_loop()")