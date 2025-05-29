"""
Model Optimization Prompt Generator API Server
Flask 기반 REST API 서버
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from typing import Dict, Any
import os
import logging
from datetime import datetime

from model_optimizer import ModelOptimizationPromptGenerator
from template_library import PromptTemplateLibrary, TemplateCategory

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask 앱 초기화
app = Flask(__name__, 
           template_folder='../../frontend/dist',
           static_folder='../../frontend/dist/assets')
CORS(app)  # CORS 허용

# 전역 인스턴스
generator = ModelOptimizationPromptGenerator()
template_library = PromptTemplateLibrary()

# 사용 통계를 위한 간단한 메모리 저장소
usage_stats = {
    'total_requests': 0,
    'model_usage': {},
    'category_usage': {},
    'recent_requests': []
}


@app.route('/')
def index():
    """메인 페이지 제공"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/models', methods=['GET'])
def get_models():
    """지원되는 모델 목록 반환"""
    models = generator.get_supported_models()
    model_info = {}
    
    for model in models:
        model_info[model] = generator.get_model_info(model)
    
    return jsonify({
        'models': models,
        'model_details': model_info,
        'total_count': len(models)
    })


@app.route('/api/templates/categories', methods=['GET'])
def get_template_categories():
    """템플릿 카테고리 목록 반환"""
    categories = template_library.get_all_categories()
    return jsonify({
        'categories': categories,
        'descriptions': {
            'code_generation': '코드 생성 및 프로그래밍',
            'analysis': '데이터 분석 및 연구',
            'writing': '문서 작성 및 글쓰기',
            'summarization': '내용 요약 및 정리'
        }
    })


@app.route('/api/templates/<category>/<model>', methods=['GET'])
def get_template_info(category: str, model: str):
    """특정 카테고리와 모델의 템플릿 정보 반환"""
    template_data = template_library.get_template(category, model)
    if not template_data:
        return jsonify({
            'error': f"카테고리 '{category}' 또는 모델 '{model}'에 대한 템플릿을 찾을 수 없습니다."
        }), 404
    
    return jsonify({
        'category': category,
        'model': model,
        'variables': template_data.get('variables', []),
        'template_preview': template_data.get('template', '')[:200] + '...'
    })


@app.route('/api/examples/<model>', methods=['GET'])
def get_example_tasks(model: str):
    """특정 모델의 예시 작업들 반환"""
    examples = template_library.get_example_tasks(model)
    if not examples:
        return jsonify({
            'error': f"모델 '{model}'에 대한 예시를 찾을 수 없습니다."
        }), 404
    
    return jsonify({
        'model': model,
        'examples': examples,
        'count': len(examples)
    })


@app.route('/api/optimize', methods=['POST'])
def optimize_prompt():
    """프롬프트 최적화 API"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '요청 데이터가 비어있습니다.'}), 400
        
        # 필수 파라미터 검증
        model = data.get('model', '').strip()
        task = data.get('task', '').strip()
        
        if not model:
            return jsonify({'error': '모델명이 필요합니다.'}), 400
        if not task:
            return jsonify({'error': '작업 내용이 필요합니다.'}), 400
        
        # 프롬프트 최적화 수행
        result = generator.generate_optimized_prompt(task, model)
        
        # 에러 처리
        if 'error' in result:
            return jsonify(result), 400
        
        # 사용 통계 업데이트
        _update_usage_stats(model, 'basic', task)
        
        # 성공 응답
        return jsonify({
            'success': True,
            'data': result,
            'usage_stats': {
                'total_requests': usage_stats['total_requests'],
                'model_popularity': usage_stats['model_usage']
            }
        })
        
    except Exception as e:
        logger.error(f"프롬프트 최적화 중 오류: {str(e)}")
        return jsonify({
            'error': '서버 내부 오류가 발생했습니다.',
            'detail': str(e)
        }), 500


@app.route('/api/optimize/template', methods=['POST'])
def optimize_with_template():
    """템플릿 기반 프롬프트 최적화 API"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '요청 데이터가 비어있습니다.'}), 400
        
        # 필수 파라미터 검증
        model = data.get('model', '').strip()
        category = data.get('category', '').strip()
        variables = data.get('variables', {})
        
        if not model:
            return jsonify({'error': '모델명이 필요합니다.'}), 400
        if not category:
            return jsonify({'error': '템플릿 카테고리가 필요합니다.'}), 400
        if not variables:
            return jsonify({'error': '템플릿 변수가 필요합니다.'}), 400
        
        # 템플릿 적용
        template_prompt = template_library.apply_template(category, model, variables)
        
        # 템플릿 적용 실패 체크
        if template_prompt.startswith('카테고리') or template_prompt.startswith('필수 변수'):
            return jsonify({'error': template_prompt}), 400
        
        # 기본 최적화도 추가 적용
        final_result = generator.generate_optimized_prompt(template_prompt, model)
        
        if 'error' in final_result:
            return jsonify(final_result), 400
        
        # 사용 통계 업데이트
        _update_usage_stats(model, category, str(variables))
        
        # 템플릿 정보 추가
        final_result.update({
            'template_category': category,
            'template_variables': variables,
            'template_applied': True
        })
        
        return jsonify({
            'success': True,
            'data': final_result,
            'template_info': {
                'category': category,
                'variables_used': variables
            }
        })
        
    except Exception as e:
        logger.error(f"템플릿 기반 최적화 중 오류: {str(e)}")
        return jsonify({
            'error': '서버 내부 오류가 발생했습니다.',
            'detail': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_usage_stats():
    """사용 통계 반환"""
    return jsonify({
        'total_requests': usage_stats['total_requests'],
        'model_usage': usage_stats['model_usage'],
        'category_usage': usage_stats['category_usage'],
        'recent_requests_count': len(usage_stats['recent_requests']),
        'top_models': sorted(
            usage_stats['model_usage'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
    })


@app.route('/api/validate', methods=['POST'])
def validate_prompt():
    """프롬프트 유효성 검증 API"""
    try:
        data = request.json
        prompt = data.get('prompt', '').strip()
        model = data.get('model', '').strip()
        
        if not prompt:
            return jsonify({'error': '프롬프트가 필요합니다.'}), 400
        
        # 기본 유효성 검사
        validation_result = {
            'is_valid': True,
            'length': len(prompt),
            'word_count': len(prompt.split()),
            'warnings': [],
            'suggestions': []
        }
        
        # 길이 체크
        model_config = generator.get_model_info(model)
        max_tokens = model_config.get('max_tokens', 4096)
        estimated_tokens = len(prompt.split()) * 1.3  # 대략적인 토큰 추정
        
        if estimated_tokens > max_tokens * 0.8:
            validation_result['warnings'].append(
                f'프롬프트가 너무 길 수 있습니다. (추정: {int(estimated_tokens)} 토큰, 한계: {max_tokens})'
            )
        
        # 기본적인 품질 체크
        if len(prompt) < 10:
            validation_result['warnings'].append('프롬프트가 너무 짧습니다.')
        
        if not any(char in prompt for char in '.!?'):
            validation_result['suggestions'].append('명확한 문장 구조를 위해 구두점을 추가하세요.')
        
        if prompt.isupper():
            validation_result['suggestions'].append('모든 대문자보다는 일반적인 대소문자 사용을 권장합니다.')
        
        return jsonify(validation_result)
        
    except Exception as e:
        logger.error(f"프롬프트 검증 중 오류: {str(e)}")
        return jsonify({
            'error': '서버 내부 오류가 발생했습니다.',
            'detail': str(e)
        }), 500


def _update_usage_stats(model: str, category: str, task: str):
    """사용 통계 업데이트"""
    usage_stats['total_requests'] += 1
    
    # 모델 사용 통계
    if model in usage_stats['model_usage']:
        usage_stats['model_usage'][model] += 1
    else:
        usage_stats['model_usage'][model] = 1
    
    # 카테고리 사용 통계
    if category in usage_stats['category_usage']:
        usage_stats['category_usage'][category] += 1
    else:
        usage_stats['category_usage'][category] = 1
    
    # 최근 요청 저장 (최대 100개)
    recent_request = {
        'timestamp': datetime.now().isoformat(),
        'model': model,
        'category': category,
        'task_preview': task[:50] + '...' if len(task) > 50 else task
    }
    usage_stats['recent_requests'].insert(0, recent_request)
    if len(usage_stats['recent_requests']) > 100:
        usage_stats['recent_requests'] = usage_stats['recent_requests'][:100]


@app.errorhandler(404)
def not_found(error):
    """404 에러 핸들러"""
    return jsonify({'error': '요청된 리소스를 찾을 수 없습니다.'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 에러 핸들러"""
    return jsonify({'error': '서버 내부 오류가 발생했습니다.'}), 500


if __name__ == '__main__':
    # 환경 변수에서 설정 읽기
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"서버 시작 중... 포트: {port}, 디버그: {debug}")
    logger.info(f"지원 모델: {generator.get_supported_models()}")
    logger.info(f"템플릿 카테고리: {template_library.get_all_categories()}")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 