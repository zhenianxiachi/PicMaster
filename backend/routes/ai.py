from flask import Blueprint, request, jsonify, current_app
import os
import re
import json

bp = Blueprint('ai', __name__)

FILTER_PARAMS_INFO = {
    'brightness': {
        'name': '亮度',
        'range': (-100, 100),
        'default': 0,
        'keywords': ['亮度', '明暗', '明亮', '暗', '亮', '曝光不足', '曝光过度']
    },
    'contrast': {
        'name': '对比度',
        'range': (0, 200),
        'default': 100,
        'keywords': ['对比度', '对比', '层次', '立体感']
    },
    'saturation': {
        'name': '饱和度',
        'range': (-100, 100),
        'default': 0,
        'keywords': ['饱和度', '鲜艳', '色彩', '颜色', '浓郁', '淡']
    },
    'hue': {
        'name': '色相',
        'range': (0, 360),
        'default': 0,
        'keywords': ['色相', '色调', '偏色']
    },
    'sharpness': {
        'name': '锐化',
        'range': (-50, 50),
        'default': 0,
        'keywords': ['锐化', '清晰', '锐利', '模糊', '柔和', '细节']
    },
    'exposure': {
        'name': '曝光',
        'range': (-100, 100),
        'default': 0,
        'keywords': ['曝光', '明暗', '亮度']
    },
    'highlights': {
        'name': '高光',
        'range': (-100, 100),
        'default': 0,
        'keywords': ['高光', '亮部', '过曝', '天空', '白色']
    },
    'shadows': {
        'name': '阴影',
        'range': (-100, 100),
        'default': 0,
        'keywords': ['阴影', '暗部', '欠曝', '黑色', '暗']
    },
    'temperature': {
        'name': '色温',
        'range': (-50, 50),
        'default': 0,
        'keywords': ['色温', '冷暖', '暖色', '冷色', '黄', '蓝']
    },
    'tint': {
        'name': '色调',
        'range': (-50, 50),
        'default': 0,
        'keywords': ['色调', '绿', '洋红', '紫']
    },
    'vignette': {
        'name': '暗角',
        'range': (0, 100),
        'default': 0,
        'keywords': ['暗角', '边缘', '四周', '聚焦']
    },
    'clarity': {
        'name': '清晰度',
        'range': (-100, 100),
        'default': 0,
        'keywords': ['清晰度', '通透', '朦胧', '雾']
    },
    'blur': {
        'name': '模糊',
        'range': (0, 20),
        'default': 0,
        'keywords': ['模糊', '柔化', '虚化']
    }
}

STYLE_PRESETS = {
    '清新': {'brightness': 5, 'contrast': 105, 'saturation': -10, 'hue': 5, 'sharpness': 10, 'exposure': 5, 'highlights': -10, 'shadows': 10, 'temperature': -5, 'tint': 0, 'vignette': 0, 'clarity': 15, 'blur': 0},
    '复古': {'brightness': -5, 'contrast': 115, 'saturation': -30, 'hue': 20, 'sharpness': -5, 'exposure': -5, 'highlights': -15, 'shadows': 10, 'temperature': 15, 'tint': 5, 'vignette': 25, 'clarity': -10, 'blur': 0},
    '日系': {'brightness': 10, 'contrast': -5, 'saturation': -15, 'hue': -5, 'sharpness': -5, 'exposure': 5, 'highlights': 10, 'shadows': 5, 'temperature': -10, 'tint': -5, 'vignette': 10, 'clarity': -5, 'blur': 0},
    '胶片': {'brightness': 0, 'contrast': 120, 'saturation': 10, 'hue': 5, 'sharpness': 15, 'exposure': 0, 'highlights': -5, 'shadows': 5, 'temperature': 5, 'tint': 5, 'vignette': 20, 'clarity': 10, 'blur': 0},
    '黑白': {'brightness': 5, 'contrast': 120, 'saturation': -100, 'hue': 0, 'sharpness': 10, 'exposure': 0, 'highlights': 0, 'shadows': 0, 'temperature': 0, 'tint': 0, 'vignette': 15, 'clarity': 5, 'blur': 0},
    '暖色调': {'brightness': 0, 'contrast': 100, 'saturation': 0, 'hue': 0, 'sharpness': 0, 'exposure': 0, 'highlights': 0, 'shadows': 0, 'temperature': 20, 'tint': 0, 'vignette': 0, 'clarity': 0, 'blur': 0},
    '冷色调': {'brightness': 0, 'contrast': 100, 'saturation': 0, 'hue': 0, 'sharpness': 0, 'exposure': 0, 'highlights': 0, 'shadows': 0, 'temperature': -20, 'tint': 0, 'vignette': 0, 'clarity': 0, 'blur': 0},
    '高对比': {'brightness': 0, 'contrast': 140, 'saturation': 0, 'hue': 0, 'sharpness': 10, 'exposure': 0, 'highlights': 0, 'shadows': 0, 'temperature': 0, 'tint': 0, 'vignette': 0, 'clarity': 10, 'blur': 0},
    '柔和': {'brightness': 5, 'contrast': 90, 'saturation': -10, 'hue': 0, 'sharpness': -10, 'exposure': 0, 'highlights': -10, 'shadows': 5, 'temperature': 0, 'tint': 0, 'vignette': 5, 'clarity': -10, 'blur': 2},
}

def parse_intent_rule_based(text):
    result = {
        'brightness': 0,
        'contrast': 100,
        'saturation': 0,
        'hue': 0,
        'sharpness': 0,
        'exposure': 0,
        'highlights': 0,
        'shadows': 0,
        'temperature': 0,
        'tint': 0,
        'vignette': 0,
        'clarity': 0,
        'blur': 0,
        'explanation': ''
    }
    
    explanations = []
    text_lower = text.lower()
    
    for style_name, preset in STYLE_PRESETS.items():
        if style_name in text:
            for key, value in preset.items():
                result[key] = value
            explanations.append(f"应用了{style_name}风格")
            return result, explanations[0]
    
    direction_patterns = {
        '增加': 1, '提高': 1, '加强': 1, '提升': 1, '加': 1, '更': 1,
        '减少': -1, '降低': -1, '减弱': -1, '降': -1, '减': -1,
        '稍微': 0.3, '一点': 0.3, '略微': 0.3,
        '很多': 1.5, '大幅': 1.5, '明显': 1,
    }
    
    degree_patterns = {
        '非常': 1.5, '很': 1.2, '比较': 0.8, '稍微': 0.3, '一点': 0.3
    }
    
    for param_key, param_info in FILTER_PARAMS_INFO.items():
        for keyword in param_info['keywords']:
            if keyword in text:
                direction = 0
                magnitude = 30
                
                for dir_word, dir_value in direction_patterns.items():
                    if dir_word in text:
                        if dir_value in [0.3]:
                            magnitude = 15
                            direction = 1
                        else:
                            direction = dir_value
                        break
                
                if direction == 0:
                    if '增加' in text or '提高' in text or '加强' in text:
                        direction = 1
                    elif '减少' in text or '降低' in text or '减弱' in text:
                        direction = -1
                    else:
                        direction = 1
                
                for deg_word, deg_value in degree_patterns.items():
                    if deg_word in text:
                        magnitude *= deg_value
                        break
                
                min_val, max_val = param_info['range']
                default_val = param_info['default']
                
                if param_key == 'contrast':
                    new_value = default_val + direction * magnitude
                else:
                    new_value = direction * magnitude
                
                new_value = max(min_val, min(max_val, new_value))
                result[param_key] = new_value
                explanations.append(f"{param_info['name']}调整为{new_value}")
                break
    
    if '更亮' in text or '太暗' in text:
        result['brightness'] = 30
        result['exposure'] = 20
        explanations.append('提高亮度和曝光')
    elif '更暗' in text or '太亮' in text:
        result['brightness'] = -30
        result['exposure'] = -20
        explanations.append('降低亮度和曝光')
    
    if '更鲜艳' in text or '色彩不够' in text:
        result['saturation'] = 30
        explanations.append('提高饱和度')
    elif '太鲜艳' in text or '颜色太浓' in text:
        result['saturation'] = -30
        explanations.append('降低饱和度')
    
    if '更清晰' in text or '不够清晰' in text:
        result['sharpness'] = 20
        result['clarity'] = 20
        explanations.append('提高锐化和清晰度')
    elif '更柔和' in text or '太锐' in text:
        result['sharpness'] = -20
        result['clarity'] = -20
        explanations.append('降低锐化和清晰度')
    
    if '暖一点' in text or '偏冷' in text:
        result['temperature'] = 20
        explanations.append('提高色温(偏暖)')
    elif '冷一点' in text or '偏暖' in text:
        result['temperature'] = -20
        explanations.append('降低色温(偏冷)')
    
    if '电影感' in text or '大片感' in text:
        result['contrast'] = 120
        result['vignette'] = 25
        result['clarity'] = 15
        explanations.append('应用电影风格: 提高对比度、添加暗角、增强清晰度')
    
    if '人像' in text:
        result['sharpness'] = -5
        result['clarity'] = -10
        result['brightness'] = 5
        explanations.append('应用人像优化: 柔化皮肤、提亮')
    
    if '风景' in text:
        result['sharpness'] = 15
        result['clarity'] = 20
        result['saturation'] = 15
        explanations.append('应用风景优化: 增强细节和色彩')
    
    result['explanation'] = '，'.join(explanations) if explanations else '根据您的描述进行了调整'
    
    return result, result['explanation']


def parse_intent_with_openai(text, api_key=None):
    try:
        import openai
        
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            return None, "未配置OpenAI API密钥"
        
        client = openai.OpenAI(api_key=api_key)
        
        system_prompt = """你是一个专业的图片编辑助手。用户会描述他们想要的图片效果，你需要将描述转换为具体的滤镜参数。

可用的参数及其范围：
- brightness (亮度): -100 到 100，默认0
- contrast (对比度): 0 到 200，默认100
- saturation (饱和度): -100 到 100，默认0
- hue (色相): 0 到 360，默认0
- sharpness (锐化): -50 到 50，默认0
- exposure (曝光): -100 到 100，默认0
- highlights (高光): -100 到 100，默认0
- shadows (阴影): -100 到 100，默认0
- temperature (色温): -50 到 50，默认0（正值偏暖，负值偏冷）
- tint (色调): -50 到 50，默认0
- vignette (暗角): 0 到 100，默认0
- clarity (清晰度): -100 到 100，默认0
- blur (模糊): 0 到 20，默认0

请返回JSON格式，包含所有参数值和一个简短的中文说明。例如：
{"brightness": 10, "contrast": 110, "saturation": -10, ..., "explanation": "提高了亮度和对比度，降低了饱和度"}"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        try:
            result = json.loads(content)
            return result, result.get('explanation', 'AI已根据您的描述调整参数')
        except json.JSONDecodeError:
            return None, "AI响应解析失败"
            
    except ImportError:
        return None, "OpenAI库未安装"
    except Exception as e:
        return None, f"AI服务错误: {str(e)}"


@bp.route('/parse-intent', methods=['POST'])
def parse_intent():
    data = request.get_json()
    text = data.get('text', '')
    current_params = data.get('current_params', {})
    use_ai = data.get('use_ai', False)
    
    if not text:
        return jsonify({'error': '请输入修改意见'}), 400
    
    explanation = ""
    
    if use_ai:
        api_key = current_app.config.get('OPENAI_API_KEY')
        result, explanation = parse_intent_with_openai(text, api_key)
        
        if result is None:
            result, explanation = parse_intent_rule_based(text)
            explanation = f"(规则解析) {explanation}"
    else:
        result, explanation = parse_intent_rule_based(text)
    
    if current_params:
        for key in result:
            if key not in ['explanation'] and key in current_params:
                if key == 'contrast':
                    result[key] = current_params.get(key, 100) + result.get(key, 0)
                else:
                    result[key] = current_params.get(key, 0) + result.get(key, 0)
    
    for param_key, param_info in FILTER_PARAMS_INFO.items():
        if param_key in result:
            min_val, max_val = param_info['range']
            result[param_key] = max(min_val, min(max_val, result[param_key]))
    
    return jsonify({
        'params': result,
        'explanation': explanation
    })


@bp.route('/presets', methods=['GET'])
def get_presets():
    return jsonify({
        'presets': STYLE_PRESETS
    })
