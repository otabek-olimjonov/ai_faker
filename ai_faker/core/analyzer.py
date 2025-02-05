from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import List, Dict, Type, Optional
from ..models.column_info import ColumnInfo
from ..utils.type_mapper import (
    map_sql_to_python_type,
    get_type_constraints,
    get_type_hint
)

class ModelAnalyzer:
    def __init__(self, model: Type[DeclarativeMeta]):
        self.model = model
        self.inspector = inspect(model)
    
    def analyze(self) -> Dict[str, ColumnInfo]:
        """Analyze SQLAlchemy model and return column information"""
        columns = {}
        
        for column in self.inspector.columns:
            # Get Python type and constraints
            python_type = map_sql_to_python_type(column.type)
            type_constraints = get_type_constraints(column.type)
            type_hint = get_type_hint(column.type)
            
            # Convert constraints to list format
            constraints = []
            for key, value in type_constraints.items():
                constraints.append(f"{key}:{value}")
            
            columns[column.name] = ColumnInfo(
                name=column.name,
                sql_type=str(column.type),
                python_type=python_type,
                nullable=column.nullable,
                constraints=constraints,
                foreign_key=self._get_foreign_key(column),
                unique=self._is_unique(column),
                default=column.default.arg if column.default else None,
                type_hint=type_hint  # Add type hint to help LLM
            )
            
        return columns
    
    def _get_foreign_key(self, column) -> Optional[str]:
        if column.foreign_keys:
            return next(iter(column.foreign_keys)).target_fullname
        return None
    
    def _is_unique(self, column) -> bool:
        return column.unique or column.primary_key