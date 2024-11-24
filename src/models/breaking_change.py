from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

class ChangeType(Enum):
    COLUMN_REMOVED = "column_removed"
    TYPE_CHANGED = "type_changed"
    CYCLIC_DEPENDENCY = "cyclic_dependency"
    SCHEMA_CHANGED = "schema_changed"

@dataclass
class BreakingChange:
    file_path: str
    change_type: ChangeType
    details: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "change_type": self.change_type.value,
            "details": self.details
        }

    def __str__(self) -> str:
        return f"Breaking change in {self.file_path}: {self.change_type.value}\nDetails: {self.details}"