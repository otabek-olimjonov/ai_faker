import re
from typing import Dict, Any, Optional

def analyze_column_name(name: str) -> Dict[str, bool]:
    """Analyze column name to infer potential data characteristics"""
    patterns = {
        'email': r'email|e_mail|mail',
        'phone': r'phone|telephone|mobile|cell',
        'name': r'name|full_name|first_name|last_name',
        'address': r'address|street|city|state|country',
        'date': r'date|created_at|updated_at|timestamp',
        'price': r'price|cost|amount|fee',
        'status': r'status|state|condition',
        'description': r'description|desc|details|text',
    }
    
    results = {}
    name_lower = name.lower()
    
    for category, pattern in patterns.items():
        if re.search(pattern, name_lower):
            results[category] = True
            
    return results

def format_value_by_type(value: str, python_type: type) -> Optional[Any]:
    """Format string value according to Python type"""
    try:
        if python_type == bool:
            return value.lower() in ('true', '1', 'yes', 'y')
        return python_type(value)
    except (ValueError, TypeError):
        return None

def snake_to_title(text: str) -> str:
    """Convert snake_case to Title Case"""
    return ' '.join(word.capitalize() for word in text.split('_'))

def is_valid_identifier(text: str) -> bool:
    """Check if the string is a valid Python identifier"""
    return text.isidentifier()

def clean_string(text: str, max_length: Optional[int] = None) -> str:
    """Clean and normalize string values"""
    # Remove leading/trailing whitespace
    cleaned = text.strip()
    
    # Replace multiple spaces with single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Truncate if max_length is specified
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned

def extract_numeric(text: str) -> Optional[float]:
    """Extract numeric value from string"""
    match = re.search(r'[-+]?\d*\.?\d+', text)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    return None

def normalize_phone(phone: str) -> str:
    """Normalize phone number format"""
    # Remove all non-numeric characters
    digits = re.sub(r'\D', '', phone)
    
    # Handle different length phone numbers
    if len(digits) == 10:  # Standard US number
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('1'):  # US number with country code
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return digits  # Return cleaned digits if format is unknown

def normalize_email(email: str) -> str:
    """Normalize email address"""
    # Convert to lowercase
    email = email.lower().strip()
    
    # Remove any whitespace
    email = re.sub(r'\s+', '', email)
    
    return email

def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    
    return slug.strip('-')

def is_probable_sentence(text: str) -> bool:
    """Check if text is likely a complete sentence"""
    # Basic sentence patterns
    sentence_patterns = [
        r'^[A-Z].*[.!?]$',  # Starts with capital, ends with punctuation
        r'^[A-Z].*\w+.*[.!?]$',  # Has at least one word character
    ]
    
    return any(re.match(pattern, text) for pattern in sentence_patterns)