"""
AI 프롬프트 최적화 도구 - 백엔드 소스 코드 패키지
"""

# 패키지 정보
__version__ = "1.0.0"
__author__ = "AI Prompt Optimizer Team"
__description__ = "AI 모델별 프롬프트 최적화 도구의 백엔드 코드"

# 주요 모듈들 import
from . import services
from . import utils

__all__ = [
    'services', 
    'utils'
]
