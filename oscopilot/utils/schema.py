from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Union
from enum import IntEnum


@dataclass
class RepairingResult:
    """
    Stores the results and intermediate representation of the repairing process
    """
    isTaskCompleted: bool = False
    code: str = ''
    critique: str = ''
    score: str = ''
    result: str = ''


@dataclass
class JudgementResult:
    """
    Stores the results and intermediate representation of the judging process
    """
    need_repair: bool = False
    critique: str = ''
    score: int = 0
    reasoning: str = ''
    error_type: str = ''


@dataclass
class InnerMonologue:
    """
    Stores all the intermediate representation during agent running
    """
    reasoning: str = ''
    error_type: str = ''
    critique: str = ''
    isRePlan: bool = False
    isTaskCompleted: bool = False


@dataclass
class EnvState:
    """
    Represents the state of an environment in which commands are executed.
    """
    command: List[str] = field(default_factory=list)
    result: Optional[str] = None
    error: Optional[str] = None
    pwd: Optional[str] = None
    ls: Optional[str] = None

    def __str__(self):
        return (f"Result: {self.result}\n"
                f"Error: {self.error}\n"
                f"PWD: {self.pwd}\n"
                f"LS: {self.ls}")    
    

@dataclass
class ExecutionState:
    """
    Stores all the intermediate representation during agent executing.
    """
    state: Optional[EnvState] = None
    node_type: str = ''
    description: str = ''
    code: str = ''
    result: str = ''
    relevant_code: str = ''

    def get_all_state(self):
        return self.state, self.node_type, self.description, self.code, self.result, self.relevant_code
    

class TaskStatusCode(IntEnum):
    START = 1
    FAILED = 6
    COMPLETED = 7