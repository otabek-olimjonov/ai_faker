from dataclasses import dataclass
from typing import Any, Optional, List

@dataclass
class ColumnInfo:
    name: str
    sql_type: str
    python_type: type
    nullable: bool
    constraints: List[str]
    foreign_key: Optional[str]
    unique: bool
    type_hint: str
    default: Any = None
    
    def to_prompt(self) -> str:
        """Convert column info to LLM prompt format"""
        return (
            f"Column '{self.name}' expects {self.type_hint}\n"
            f"Additional constraints:\n"
            f"- Type: {self.sql_type}\n"
            f"- Nullable: {self.nullable}\n"
            f"- Unique: {self.unique}\n"
            f"- Foreign Key: {self.foreign_key or 'None'}\n"
            f"- Other: {', '.join(self.constraints)}"
        )