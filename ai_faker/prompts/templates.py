"""
Prompt templates for AI Faker data generation.
Contains various templates for different generation scenarios and LLM providers.
"""

# Main batch generation prompt for generating multiple records at once
BATCH_DATA_GENERATION_PROMPT = '''
You are a database records generator. Generate {count} database records according to the following schema:

{schema_info}

Return the data as a JSON array of objects. Example format:
[
    {{ ... record 1 fields ... }},
    {{ ... record 2 fields ... }},
    ...
]

Requirements:
1. Generate exactly {count} records
2. Each record must be complete and valid
3. All records must be unique
4. Use realistic and contextually appropriate values
5. Follow field-specific patterns:

Username patterns:
- Combine letters, numbers (e.g., john_doe123, tech_user42)
- Allow underscores, no other special characters
- Keep between 5-20 characters
- Must be unique across all records

Email patterns:
- Use realistic domains (example.com, gmail.com, company.com)
- Match email convention (username@domain.com)
- Can include dots, underscores in local part
- Must be unique across all records

Name patterns:
- Use realistic human names
- Include mix of different cultural backgrounds
- Proper capitalization (e.g., "John Smith", "María García")

Address patterns:
- Use realistic street names and numbers
- Include apartment/suite numbers where appropriate
- Use real city and state combinations
- Valid postal codes for the region

Phone patterns:
- Use region-appropriate formats
- Include country codes if international
- Use proper separators (e.g., +1-555-123-4567)

Date patterns:
- Use ISO format (YYYY-MM-DD)
- Generate realistic dates
- Respect logical date ranges (e.g., birthdates for adults)

Return only the JSON array without any additional text or explanation.
'''

# Fallback prompt for single record generation
SINGLE_RECORD_PROMPT = '''
Generate a single database record for the following schema:

{schema_info}

Requirements:
- Generate complete and valid data
- Use realistic and contextually appropriate values
- Follow all type constraints and patterns
- Return as a single JSON object

Return only the JSON object without any additional text.
'''

# Prompt for generating related records
RELATED_RECORDS_PROMPT = '''
Generate {count} related database records according to these schemas and relationships:

{schema_info}
{relationship_info}

Requirements:
1. Generate valid records for all related tables
2. Maintain referential integrity
3. Create realistic relationships between records
4. Follow all unique constraints
5. Return as a single JSON object with arrays for each table

Example format:
{{
    "main_table": [ ... records ... ],
    "related_table1": [ ... records ... ],
    "related_table2": [ ... records ... ]
}}

Return only the JSON object without any additional text.
'''

# Prompt for generating specific data types
TYPE_SPECIFIC_PROMPTS = {
    'email': 'Generate a unique email address using common patterns and domains.',
    'username': 'Generate a unique username (5-20 chars, letters, numbers, underscores only).',
    'name': 'Generate a realistic full name using proper capitalization.',
    'address': 'Generate a complete mailing address with proper formatting.',
    'phone': 'Generate a phone number in international format with country code.',
    'date': 'Generate a date in ISO format (YYYY-MM-DD) within appropriate range.',
    'text': 'Generate realistic text content appropriate for the field.',
    'number': 'Generate a number within the specified range and constraints.',
    'boolean': 'Generate a boolean value based on field context.',
    'url': 'Generate a valid URL with appropriate structure.',
    'ip': 'Generate a valid IP address (v4 or v6 as specified).',
    'color': 'Generate a color value in specified format (hex, rgb, etc).',
    'currency': 'Generate a currency amount with proper formatting.',
}

# Prompt for handling custom constraints
CONSTRAINT_HANDLING_PROMPT = '''
Generate a value for field "{field_name}" that satisfies these constraints:

{constraints}

Field type: {field_type}
Additional context: {context}

Return only the generated value without any explanation.
'''

# Prompt for generating enum/choice fields
ENUM_GENERATION_PROMPT = '''
Generate a value for field "{field_name}" from these allowed values:

{allowed_values}

Context: {context}

Return only the selected value without any explanation.
'''

# Special handling for sensitive data fields
SENSITIVE_DATA_PROMPT = '''
Generate an anonymized but realistic value for sensitive field "{field_name}".
Field type: {field_type}
Purpose: {purpose}

Return only the generated value without any explanation.
'''