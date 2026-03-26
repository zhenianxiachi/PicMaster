import os
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from runtime_bootstrap import prefer_repo_python

prefer_repo_python()

from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from models import db

BASE_DIR = CURRENT_DIR


def resolve_backend_path(value: str) -> str:
    path = Path(value)
    if path.is_absolute():
        return str(path)
    return str((BASE_DIR / path).resolve())

# 加载环境变量
load_dotenv(BASE_DIR / '.env')

# 创建Flask应用
app = Flask(
    __name__,
    instance_path=str((BASE_DIR / 'instance').resolve()),
    instance_relative_config=True,
)
CORS(app)  # 解决跨域问题

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = resolve_backend_path(os.getenv('UPLOAD_FOLDER', 'uploads'))
app.config['TEMP_FOLDER'] = resolve_backend_path(os.getenv('TEMP_FOLDER', 'temp'))
app.config['SERVER_HOST'] = os.getenv('SERVER_HOST', 'localhost')
app.config['SERVER_PORT'] = os.getenv('SERVER_PORT', '5000')
app.config['FRONTEND_URL'] = os.getenv('FRONTEND_URL', 'http://localhost:3000')

app.config['DEEPSEEK_API_KEY'] = os.getenv('DEEPSEEK_API_KEY')
app.config['DEEPSEEK_BASE_URL'] = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
app.config['DEEPSEEK_MODEL'] = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///picmaster.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

# 注册静态文件服务
app.static_folder = app.config['UPLOAD_FOLDER']
app.add_url_rule('/uploads/<path:filename>', 'uploaded_file',
                 build_only=True)
app.url_map.converters['path'] = app.url_map.converters['default']

# 注册路由
from routes import images, portfolios, previews, ai
app.register_blueprint(images.bp, url_prefix='/api/images')
app.register_blueprint(portfolios.bp, url_prefix='/api/portfolios')
app.register_blueprint(previews.bp, url_prefix='/api/previews')
app.register_blueprint(ai.bp, url_prefix='/api/ai')

# 添加静态文件服务
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 主页路由
@app.route('/')
def index():
    return "PicMaster Backend API is running!"

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500

if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    port = int(app.config.get('SERVER_PORT', 5000))
    app.run(debug=debug, host='0.0.0.0', port=port)
