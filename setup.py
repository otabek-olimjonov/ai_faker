from setuptools import setup, find_packages

# Define base requirements
base_requirements = [
    'sqlalchemy>=1.4.0',
    'typing-extensions>=4.0.0',
    'python-dotenv>=0.19.0',  # Added dotenv
]

# Provider-specific requirements
provider_requirements = {
    'openai': [
        'openai>=1.0.0',
    ],
    'gemini': [
        'google-generativeai>=0.3.0',
    ],
}

# Define all requirements (both OpenAI and Gemini)
all_requirements = []
for reqs in provider_requirements.values():
    all_requirements.extend(reqs)

# Create extras_require dictionary
extras_require = {
    **provider_requirements,  # Individual provider requirements
    'all': list(set(all_requirements)),  # Both OpenAI and Gemini requirements
}

setup(
    name='ai_faker',
    version='0.1.0',
    description='AI-powered fake data generator for SQLAlchemy models using LLMs',
    author='Otabek Olimjonov',
    author_email='bekdevs01@gmail.com',
    packages=find_packages(include=['ai_faker', 'ai_faker.*']),
    install_requires=base_requirements,
    extras_require=extras_require,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)