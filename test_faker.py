from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from ai_faker import DataGenerator, LLMInterface
from ai_faker.core.llm_providers import GeminiProvider, OpenAIProvider
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create SQLite database engine
engine = create_engine('sqlite:///fake_data.db', echo=False)
Session = sessionmaker(bind=engine)

# Create a simple model for testing
Base = declarative_base()

class TestUser(Base):
    __tablename__ = 'test_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f"ID: {self.id} | Username: {self.username} | Email: {self.email}"

# Create all tables in the database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def save_to_db(data_list):
    """Save generated data to database"""
    session = Session()
    try:
        for data in data_list:
            user = TestUser(**data)
            session.add(user)
        session.commit()
        print("\n✅ Data successfully saved to database!")
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error saving to database: {str(e)}")
        raise
    finally:
        session.close()

def test_provider(name, provider_class, api_key):
    """Test provider with batch generation"""
    print(f"\n🚀 Testing {name} provider...")
    print("-" * 50)
    
    try:
        provider = provider_class(api_key=api_key)
        llm = LLMInterface(provider)
        generator = DataGenerator(llm)
        
        # Generate 50 records in one batch
        print(f"Generating 50 records using {name}...")
        data = generator.generate_fake_data(TestUser, count=50)
        
        print(f"\nSuccessfully generated {len(data)} records:")
        for i, item in enumerate(data[:5], 1):  # Show first 5 records
            print(f"\nRecord {i}:")
            print(f"- Username: {item['username']}")
            print(f"- Email: {item['email']}")
        
        if len(data) > 5:
            print(f"\n... and {len(data) - 5} more records")
        
        save_to_db(data)
        print(f"✨ {name} test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ {name} test failed: {str(e)}")

def view_database_contents():
    """View sample of records in the database"""
    session = Session()
    try:
        total_count = session.query(TestUser).count()
        sample_users = session.query(TestUser).order_by(TestUser.id).limit(5).all()
        
        print(f"\n📊 Database contents (showing 5 of {total_count} records):")
        print("-" * 50)
        for user in sample_users:
            print(user)
        
        if total_count > 5:
            print(f"\n... and {total_count - 5} more records")
            
    except Exception as e:
        print(f"\n❌ Error viewing database: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    print("\n🔧 Starting batch fake data generation test...")
    print("=" * 50)
    
    # Test providers
    if os.getenv('OPENAI_API_KEY'):
        test_provider("OpenAI", OpenAIProvider, os.getenv('OPENAI_API_KEY'))
    else:
        print("\n⚠️  Skipping OpenAI test - no API key found")
    
    if os.getenv('GOOGLE_API_KEY'):
        test_provider("Gemini", GeminiProvider, os.getenv('GOOGLE_API_KEY'))
    else:
        print("\n⚠️  Skipping Gemini test - no API key found")
    
    # View the database contents
    view_database_contents()
    
    print("\n✨ Test run completed!")
    print("=" * 50)