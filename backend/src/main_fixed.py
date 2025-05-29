from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import logging
from datetime import datetime

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 프롬프트 최적화 엔진 임포트
from src.services.optimizer import PromptOptimizer

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Flask 앱 초기화
app = Flask(__name__, static_folder='../../frontend/dist')
CORS(app)  # CORS 설정

# 프롬프트 최적화 엔진 초기화
optimizer = PromptOptimizer()

# API 라우트들 (먼저 정의)
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    서버 상태 확인 엔드포인트
    """
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """
    사용 가능한 모든 AI 모델 정보를 반환하는 엔드포인트
    """
    try:
        models = optimizer.get_available_models()
        return jsonify({
            "success": True,
            "models": models
        })
    except Exception as e:
        logger.error(f"모델 정보 조회 중 오류 발생: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"모델 정보 조회 중 오류 발생: {str(e)}"
        }), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_prompt():
    """
    사용자 입력을 분석하고 선택된 모델에 최적화된 프롬프트를 생성하는 엔드포인트
    """
    try:
        data = request.json
        
        # 필수 파라미터 확인
        if not data or 'input_text' not in data or 'model_id' not in data:
            return jsonify({
                "success": False,
                "error": "필수 파라미터가 누락되었습니다. 'input_text'와 'model_id'는 필수입니다."
            }), 400
        
        input_text = data['input_text']
        model_id = data['model_id']
        additional_params = data.get('additional_params', {})
        
        # 입력 텍스트 검증
        if not input_text or not isinstance(input_text, str):
            return jsonify({
                "success": False,
                "error": "유효하지 않은 입력 텍스트입니다."
            }), 400
        
        # 모델 ID 검증
        if not model_id or not isinstance(model_id, str):
            return jsonify({
                "success": False,
                "error": "유효하지 않은 모델 ID입니다."
            }), 400
        
        # 추가 파라미터 검증
        if additional_params and not isinstance(additional_params, dict):
            return jsonify({
                "success": False,
                "error": "유효하지 않은 추가 파라미터 형식입니다."
            }), 400
        
        # 프롬프트 최적화 실행
        result = optimizer.optimize_prompt(input_text, model_id, additional_params)
        
        # 결과 반환
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"프롬프트 최적화 중 오류 발생: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"프롬프트 최적화 중 오류 발생: {str(e)}"
        }), 500

@app.route('/api/model/<model_id>/tips', methods=['GET'])
def get_model_tips(model_id):
    """
    특정 모델의 최적화 팁을 반환하는 엔드포인트
    """
    try:
        capability = request.args.get('capability')
        tips = optimizer.get_model_specific_tips(model_id, capability)
        
        return jsonify({
            "success": True,
            "model_id": model_id,
            "capability": capability,
            "tips": tips
        })
    except Exception as e:
        logger.error(f"모델 팁 조회 중 오류 발생: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"모델 팁 조회 중 오류 발생: {str(e)}"
        }), 500

@app.route('/api/model/<model_id>/structure', methods=['GET'])
def get_model_structure(model_id):
    """
    특정 모델의 프롬프트 구조를 반환하는 엔드포인트
    """
    try:
        structure = optimizer.get_model_prompt_structure(model_id)
        
        if "error" in structure:
            return jsonify({
                "success": False,
                "error": structure["error"]
            }), 404
        
        return jsonify({
            "success": True,
            "model_id": model_id,
            "structure": structure
        })
    except Exception as e:
        logger.error(f"모델 구조 조회 중 오류 발생: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"모델 구조 조회 중 오류 발생: {str(e)}"
        }), 500

@app.route('/api/model/<model_id>/info', methods=['GET'])
def get_model_info(model_id):
    """
    특정 모델의 정보를 반환하는 엔드포인트
    """
    try:
        info = optimizer.get_model_info(model_id)
        
        if "error" in info:
            return jsonify({
                "success": False,
                "error": info["error"]
            }), 404
        
        return jsonify({
            "success": True,
            "model_id": model_id,
            "info": info
        })
    except Exception as e:
        logger.error(f"모델 정보 조회 중 오류 발생: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"모델 정보 조회 중 오류 발생: {str(e)}"
        }), 500

@app.route('/api/compare', methods=['POST'])
def compare_models():
    """
    여러 모델을 비교하는 엔드포인트
    """
    try:
        data = request.json
        
        # 필수 파라미터 확인
        if not data or 'model_ids' not in data:
            return jsonify({
                "success": False,
                "error": "필수 파라미터가 누락되었습니다. 'model_ids'는 필수입니다."
            }), 400
        
        model_ids = data['model_ids']
        
        # 모델 ID 목록 검증
        if not isinstance(model_ids, list) or not model_ids:
            return jsonify({
                "success": False,
                "error": "유효하지 않은 모델 ID 목록입니다."
            }), 400
        
        # 모델 비교 실행
        comparison = optimizer.compare_models(model_ids)
        
        # 결과 반환
        return jsonify({
            "success": True,
            "comparison": comparison
        })
    except Exception as e:
        logger.error(f"모델 비교 중 오류 발생: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"모델 비교 중 오류 발생: {str(e)}"
        }), 500

# 에러 핸들러들
@app.errorhandler(404)
def not_found(error):
    """
    404 에러 핸들러
    """
    return jsonify({
        "success": False,
        "error": "요청한 리소스를 찾을 수 없습니다."
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """
    405 에러 핸들러
    """
    return jsonify({
        "success": False,
        "error": "허용되지 않은 메서드입니다."
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    """
    500 에러 핸들러
    """
    return jsonify({
        "success": False,
        "error": "서버 내부 오류가 발생했습니다."
    }), 500

# 정적 파일 서빙을 위한 라우트 (맨 마지막에 정의)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    프론트엔드 정적 파일 서빙
    """
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # 환경 변수에서 포트 가져오기 (기본값: 5000)
    port = int(os.environ.get('PORT', 5000))
    
    # 디버그 모드 설정
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"서버를 포트 {port}에서 시작합니다.")
    logger.info(f"디버그 모드: {debug}")
    
    # 서버 시작
    app.run(host='0.0.0.0', port=port, debug=debug) 