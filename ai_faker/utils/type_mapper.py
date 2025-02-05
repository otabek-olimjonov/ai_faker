from typing import Type, Any, Dict, Optional
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, Date, Time,
    Numeric, BigInteger, SmallInteger, Text, Unicode, UnicodeText,
    LargeBinary, Enum, JSON, ARRAY, Interval, TIMESTAMP, DECIMAL
)
from datetime import datetime, date, time
from decimal import Decimal

# Mapping of SQLAlchemy types to Python types
TYPE_MAPPING: Dict[Type, Type] = {
    # String types
    String: str,
    Text: str,
    Unicode: str,
    UnicodeText: str,
    
    # Numeric types
    Integer: int,
    BigInteger: int,
    SmallInteger: int,
    Float: float,
    Numeric: Decimal,
    DECIMAL: Decimal,
    
    # Boolean type
    Boolean: bool,
    
    # Date/Time types
    DateTime: datetime,
    TIMESTAMP: datetime,
    Date: date,
    Time: time,
    Interval: str,  # Intervals stored as string representation
    
    # Binary types
    LargeBinary: bytes,
    
    # JSON types
    JSON: dict,
    
    # Array types
    ARRAY: list,
}

def map_sql_to_python_type(sql_type: Any) -> Type:
    """
    Map SQLAlchemy column type to corresponding Python type.
    
    Args:
        sql_type: SQLAlchemy type object

    Returns:
        Type: Corresponding Python type
    """
    # Check for exact type match
    for sql_class, python_type in TYPE_MAPPING.items():
        if isinstance(sql_type, sql_class):
            return python_type
    
    # Handle Enum type separately
    if isinstance(sql_type, Enum):
        return str
    
    # Default to string for unknown types
    return str

def get_type_constraints(sql_type: Any) -> Dict[str, Any]:
    """
    Extract constraints from SQLAlchemy type for data generation.
    
    Args:
        sql_type: SQLAlchemy type object

    Returns:
        Dict containing type-specific constraints
    """
    constraints = {}
    
    # String length constraints
    if hasattr(sql_type, 'length') and sql_type.length is not None:
        constraints['max_length'] = sql_type.length
    
    # Numeric constraints
    if isinstance(sql_type, (Numeric, DECIMAL)):
        constraints['precision'] = sql_type.precision
        constraints['scale'] = sql_type.scale
    
    # Enum constraints
    if isinstance(sql_type, Enum):
        constraints['choices'] = sql_type.enums
    
    # Array constraints
    if isinstance(sql_type, ARRAY):
        constraints['item_type'] = map_sql_to_python_type(sql_type.item_type)
    
    return constraints

def format_value_for_type(value: Any, target_type: Type) -> Optional[Any]:
    """
    Format a value to match the target Python type.
    
    Args:
        value: Value to format
        target_type: Target Python type

    Returns:
        Formatted value or None if conversion fails
    """
    try:
        if target_type == bool:
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'y', 't')
            return bool(value)
            
        if target_type in (datetime, date, time):
            if isinstance(value, str):
                # Handle different date/time string formats
                if target_type == datetime:
                    return datetime.fromisoformat(value)
                elif target_type == date:
                    return date.fromisoformat(value)
                elif target_type == time:
                    return time.fromisoformat(value)
                    
        if target_type == Decimal:
            return Decimal(str(value))
            
        if target_type == bytes and isinstance(value, str):
            return value.encode('utf-8')
            
        # Default conversion
        return target_type(value)
        
    except (ValueError, TypeError, AttributeError):
        return None

def get_type_hint(sql_type: Any) -> str:
    """
    Get human-readable hint about the expected data type.
    
    Args:
        sql_type: SQLAlchemy type object

    Returns:
        str: Description of expected data type
    """
    if isinstance(sql_type, String):
        return f"text with maximum length of {sql_type.length}" if sql_type.length else "text"
    
    if isinstance(sql_type, (Integer, SmallInteger, BigInteger)):
        return "whole number"
    
    if isinstance(sql_type, (Float, Numeric, DECIMAL)):
        return "decimal number"
    
    if isinstance(sql_type, Boolean):
        return "true/false value"
    
    if isinstance(sql_type, DateTime):
        return "date and time"
    
    if isinstance(sql_type, Date):
        return "date"
    
    if isinstance(sql_type, Time):
        return "time"
    
    if isinstance(sql_type, Enum):
        return f"one of: {', '.join(sql_type.enums)}"
    
    if isinstance(sql_type, JSON):
        return "JSON data"
    
    if isinstance(sql_type, ARRAY):
        return f"list of {get_type_hint(sql_type.item_type)}"
    
    return "text"  # Default hint for unknown types