from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

base_requirements = [
    'sqlalchemy>=1.4.0',
    'typing-extensions>=4.0.0',
    'python-dotenv>=0.19.0',
]

provider_requirements = {
    'openai': ['openai>=1.0.0'],
    'gemini': ['google-generativeai>=0.3.0'],
}

all_requirements = []
for reqs in provider_requirements.values():
    all_requirements.extend(reqs)

setup(
    name='sql-ai-faker',
    version='1.0.0',
    description='AI-powered fake data generator for SQLAlchemy models using LLMs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Otabek Olimjonov',
    author_email='bekdevs01@gmail.com',
    url='https://github.com/otabek-olimjonov/ai_faker',
    packages=find_packages(include=['ai_faker', 'ai_faker.*']),
    install_requires=base_requirements,
    extras_require={
        **provider_requirements,
        'all': list(set(all_requirements)),
    },
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
    ],
    keywords='sqlalchemy, faker, ai, llm, testing, database, openai, gemini',
    project_urls={
        'Bug Reports': 'https://github.com/otabek-olimjonov/ai_faker/issues',
        'Source': 'https://github.com/otabek-olimjonov/ai_faker',
    },
    license='MIT',
)