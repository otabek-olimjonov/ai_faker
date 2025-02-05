import json
from typing import Dict, Any, List, Type
from sqlalchemy.ext.declarative import DeclarativeMeta
from .analyzer import ModelAnalyzer
from .llm_interface import LLMInterface
from ..utils.type_mapper import format_value_for_type

class DataGenerator:
    def __init__(self, llm: LLMInterface):
        self.llm = llm
        
    def generate_fake_data(self, model: Type[DeclarativeMeta], count: int = 10) -> List[Dict[str, Any]]:
        """Generate fake data for the given SQLAlchemy model in batch"""
        analyzer = ModelAnalyzer(model)
        columns = analyzer.analyze()
        
        # Create schema info for the prompt
        schema_info = self._create_schema_info(columns)
        
        # Generate data in batch
        json_data = self._generate_batch_data(schema_info, count)
        
        # Parse and validate the generated data
        return self._process_generated_data(json_data, columns)
    
    def _create_schema_info(self, columns: Dict) -> str:
        """Create a schema description for the prompt"""
        schema_parts = []
        for name, info in columns.items():
            if name != 'id':  # Skip id column as it's auto-generated
                constraints = []
                if not info.nullable:
                    constraints.append("required")
                if info.unique:
                    constraints.append("unique")
                if info.constraints:
                    constraints.extend(info.constraints)
                
                constraint_str = f" ({', '.join(constraints)})" if constraints else ""
                schema_parts.append(f"- {name}: {info.type_hint}{constraint_str}")
        
        return "\n".join(schema_parts)
    
    def _generate_batch_data(self, schema_info: str, count: int) -> str:
        """Generate batch data using LLM"""
        prompt = self.llm.get_batch_generation_prompt(schema_info, count)
        response = self.llm.generate_value_suggestion(prompt)
        
        # Try to find and extract JSON array if the response contains extra text
        try:
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            if start_idx != -1 and end_idx != 0:
                response = response[start_idx:end_idx]
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse generated JSON data: {str(e)}\nResponse: {response}")
    
    def _process_generated_data(self, json_data: List[Dict], columns: Dict) -> List[Dict[str, Any]]:
        """Process and validate generated data"""
        processed_data = []
        used_values = {'username': set(), 'email': set()}  # Track unique values
        
        for item in json_data:
            processed_item = {}
            try:
                for col_name, col_info in columns.items():
                    if col_name == 'id':
                        continue  # Skip ID processing
                    
                    value = item.get(col_name)
                    if value is None and not col_info.nullable:
                        raise ValueError(f"Missing required value for {col_name}")
                    
                    # Format value according to column type
                    if value is not None:
                        value = format_value_for_type(value, col_info.python_type)
                    
                    # Check uniqueness
                    if col_info.unique:
                        if value in used_values.get(col_name, set()):
                            raise ValueError(f"Duplicate value '{value}' for unique column {col_name}")
                        used_values.setdefault(col_name, set()).add(value)
                    
                    processed_item[col_name] = value
                
                processed_data.append(processed_item)
                
            except Exception as e:
                raise ValueError(f"Error processing record {item}: {str(e)}")
        
        return processed_data