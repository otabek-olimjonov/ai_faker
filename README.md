# AI Faker

AI-powered fake data generator for SQLAlchemy models using LLMs (OpenAI, Gemini).

## Features

- Generate realistic fake data using AI/LLM
- Batch generation for efficiency
- Support for OpenAI and Google's Gemini
- SQLAlchemy integration
- Type-aware data generation
- Unique constraint handling
- Relationship support

## Installation

```bash
# Install with OpenAI support
pip install ai_faker[openai]

# Install with Gemini support
pip install ai_faker[gemini]

# Install with all providers
pip install ai_faker[all]
```

## Quick Start

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from ai_faker import DataGenerator, LLMInterface
from ai_faker.core.llm_providers import OpenAIProvider

# Create your SQLAlchemy model
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)

# Initialize the provider and generator
provider = OpenAIProvider(api_key="your-api-key")
llm = LLMInterface(provider)
generator = DataGenerator(llm)

# Generate fake data
fake_users = generator.generate_fake_data(User, count=50)

print(fake_users)
```

## Environment Variables

Create a `.env` file:

```env
# OpenAI
OPENAI_API_KEY=your-openai-key

# Gemini
GOOGLE_API_KEY=your-google-key
```

## Supported Providers

### OpenAI
- Uses GPT models
- Requires OpenAI API key

### Gemini
- Uses Google's Gemini models
- Requires Google API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.