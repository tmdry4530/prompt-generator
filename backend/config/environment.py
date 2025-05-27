# 백엔드 환경 설정 로드 유틸리티
import os
import logging
from dotenv import load_dotenv

class EnvironmentManager:
    """환경 설정 관리 클래스"""
    
    def __init__(self):
        self.env_loaded = False
        self.env_mode = os.environ.get('FLASK_ENV', 'development')
        self.env_file = self._get_env_file()
        self.load_environment()
    
    def _get_env_file(self):
        """현재 환경에 맞는 .env 파일 경로 반환"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_dir = os.path.join(base_dir, 'config')
        
        if self.env_mode == 'production':
            return os.path.join(config_dir, '.env.production')
        else:
            return os.path.join(config_dir, '.env.development')
    
    def load_environment(self):
        """환경 변수 로드"""
        try:
            if os.path.exists(self.env_file):
                load_dotenv(self.env_file)
                self.env_loaded = True
                logging.info(f"환경 설정 로드 완료: {self.env_file}")
            else:
                logging.warning(f"환경 설정 파일을 찾을 수 없습니다: {self.env_file}")
        except Exception as e:
            logging.error(f"환경 설정 로드 중 오류 발생: {str(e)}")
    
    def get_config(self, key, default=None):
        """환경 변수 값 반환"""
        return os.environ.get(key, default)
    
    def get_environment_info(self):
        """현재 환경 정보 반환"""
        return {
            'mode': self.env_mode,
            'env_file': self.env_file,
            'env_loaded': self.env_loaded,
            'port': int(os.environ.get('PORT', 5000)),
            'debug': os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't'),
            'cors_origins': os.environ.get('CORS_ORIGINS', '*').split(','),
            'log_level': os.environ.get('LOG_LEVEL', 'INFO'),
            'log_file': os.environ.get('LOG_FILE', 'api_server.log')
        }
    
    def validate_environment(self):
        """필수 환경 변수 검증"""
        required_vars = ['PORT', 'FLASK_ENV']
        missing_vars = []
        
        for var in required_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            logging.warning(f"다음 필수 환경 변수가 설정되지 않았습니다: {', '.join(missing_vars)}")
            return False
        
        return True
    
    def log_environment_info(self):
        """환경 설정 정보 로깅"""
        env_info = self.get_environment_info()
        logging.info("=== 환경 설정 정보 ===")
        for key, value in env_info.items():
            logging.info(f"{key}: {value}")
        logging.info("=====================")
        
        return env_info

# 환경 관리자 인스턴스 생성
env_manager = EnvironmentManager()
