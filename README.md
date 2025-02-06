# 🤖 AI Faker
AI-powered fake data generator for SQLAlchemy models using LLMs (OpenAI, Gemini).

## ✨ Implemented Features
- ✅ Generate realistic fake data using AI/LLM
- ✅ Batch generation for efficiency
- ✅ Support for OpenAI and Google's Gemini
- ✅ SQLAlchemy integration
- ✅ Type-aware data generation
- ✅ Unique constraint handling
- ✅ Basic relationship support
- ✅ Environment variables support
- ✅ Multiple provider support
- ✅ Batch processing with JSON

## 🎯 TODO
- ⬜ Foreign key relationship support
- ⬜ Complex relationship handling (one-to-many, many-to-many)
- ⬜ Custom data validation rules
- ⬜ Export to different formats (CSV, JSON, SQL)
- ⬜ CLI interface
- ⬜ Caching mechanism for repeated requests
- ⬜ Test coverage
- ⬜ Documentation site
- ⬜ More providers (Claude, Mistral, etc.)
- ⬜ Performance optimization for large datasets

## 🚀 Installation
```bash
# Install with OpenAI support
pip install ai_faker[openai]

# Install with Gemini support
pip install ai_faker[gemini]

# Install with all providers
pip install ai_faker[all]
```

## 📝 Quick Start
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

## 🔑 Environment Variables
Create a `.env` file:
```env
# OpenAI
OPENAI_API_KEY=your-openai-key

# Gemini
GOOGLE_API_KEY=your-google-key
```

## 🔌 Supported Providers
### 🌟 OpenAI
- Uses GPT models
- Requires OpenAI API key

### 🤖 Gemini
- Uses Google's Gemini models
- Requires Google API key

## 🤝 Contributing
Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add some amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

### 🛠️ Development Setup
```bash
# Clone the repository
git clone https://github.com/otabek-olimjonov/ai_faker.git
cd ai_faker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[all]"
```

### 📋 Guidelines for Contributors
- ✍️ Add tests for new features
- 📚 Update documentation
- 🎨 Follow PEP 8 style guide
- 🧹 Keep commits clean and descriptive
- 📝 Update README.md for significant changes

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/otabek-olimjonov/ai_faker/blob/main/LICENSE) file for details.