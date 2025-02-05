# ai_faker/__init__.py
from .__version__ import __version__
from .core.generator import DataGenerator
from .core.llm_interface import LLMInterface
from .core.analyzer import ModelAnalyzer

__all__ = ['DataGenerator', 'LLMInterface', 'ModelAnalyzer', '__version__']
