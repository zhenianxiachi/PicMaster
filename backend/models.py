"""
数据库模型定义模块

本模块定义了PicMaster图片编辑管理系统的所有数据库模型，包括：
- User: 用户模型
- Category: 作品集分类模型
- Tag: 标签模型
- Portfolio: 作品集模型
- Image: 图片模型
- FilterPreset: 滤镜预设模型
- ClientFeedback: 客户反馈模型
- Annotation: 标注模型
- PreviewLink: 预览链接模型

作者：zhenianxiachi
创建时间：2026年
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建数据库实例
# SQLAlchemy是Python中最流行的ORM框架，提供了强大的数据库操作能力
db = SQLAlchemy()


class User(db.Model):
    """
    用户模型
    
    存储系统用户信息，包括摄影师、修图师等用户的基本信息。
    支持用户注册、登录认证等功能。
    
    字段说明：
    - id: 用户唯一标识符，主键自增
    - username: 用户名，唯一且不能为空，最大长度50字符
    - password: 密码，存储加密后的密码哈希值，最大长度255字符
    - email: 邮箱地址，唯一且不能为空，用于找回密码和通知
    - created_at: 账户创建时间，自动设置为当前时间
    - updated_at: 账户更新时间，每次更新自动刷新
    
    关系说明：
    - portfolios: 用户创建的所有作品集，一对多关系
    """
    __tablename__ = 'users'
    
    # 主键：用户唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 用户名：用于登录和显示，必须唯一
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # 密码：存储加密后的密码哈希值（使用werkzeug.security进行加密）
    password = db.Column(db.String(255), nullable=False)
    
    # 邮箱：用于找回密码和系统通知
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # 创建时间：账户注册时间，自动设置
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 更新时间：账户信息最后更新时间，自动更新
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系：一个用户可以创建多个作品集
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)


class Category(db.Model):
    """
    作品集分类模型
    
    用于对作品集进行分类管理，如：人像、风景、商业、婚礼等。
    方便用户按类别浏览和管理作品集。
    
    字段说明：
    - id: 分类唯一标识符，主键自增
    - name: 分类名称，唯一且不能为空，如"人像摄影"、"风景摄影"
    - created_at: 分类创建时间
    
    关系说明：
    - portfolios: 该分类下的所有作品集，一对多关系
    """
    __tablename__ = 'categories'
    
    # 主键：分类唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 分类名称：如"人像摄影"、"风景摄影"、"商业摄影"等
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # 创建时间：分类创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系：一个分类下可以有多个作品集
    portfolios = db.relationship('Portfolio', backref='category', lazy=True)


class Tag(db.Model):
    """
    标签模型
    
    用于给作品集添加标签，实现更灵活的分类和搜索功能。
    如："户外"、"室内"、"夜景"、"日系"等标签。
    
    字段说明：
    - id: 标签唯一标识符，主键自增
    - name: 标签名称，唯一且不能为空
    - created_at: 标签创建时间
    """
    __tablename__ = 'tags'
    
    # 主键：标签唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 标签名称：如"户外"、"室内"、"夜景"、"日系"等
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # 创建时间：标签创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 作品集标签关联表（多对多关系的中间表）
# 一个作品集可以有多个标签，一个标签也可以属于多个作品集
portfolio_tags = db.Table('portfolio_tags',
    db.Column('portfolio_id', db.Integer, db.ForeignKey('portfolios.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Portfolio(db.Model):
    """
    作品集模型
    
    核心业务模型，用于管理摄影师的作品集。
    每个作品集包含多张图片，属于某个用户和分类。
    
    字段说明：
    - id: 作品集唯一标识符，主键自增
    - name: 作品集名称，如"张三婚礼跟拍"、"李四写真"
    - client_name: 客户名称，记录是给哪位客户拍摄的作品
    - shoot_date: 拍摄日期，记录作品拍摄时间
    - cover_image: 封面图片路径，用于在列表中展示
    - user_id: 所属用户ID，外键关联users表
    - category_id: 所属分类ID，外键关联categories表
    - created_at: 作品集创建时间
    - updated_at: 作品集更新时间
    
    关系说明：
    - images: 作品集中的所有图片，一对多关系
    - tags: 作品集的标签，多对多关系
    """
    __tablename__ = 'portfolios'
    
    # 主键：作品集唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 作品名称：如"张三婚礼跟拍"、"李四写真"等
    name = db.Column(db.String(100), nullable=False)
    
    # 客户名称：记录是给哪位客户拍摄的作品
    client_name = db.Column(db.String(50), nullable=False)
    
    # 拍摄日期：记录作品拍摄时间，方便按时间归档
    shoot_date = db.Column(db.Date, nullable=False)
    
    # 封面图片：作品集的封面图片路径，用于在列表中展示
    cover_image = db.Column(db.String(255))
    
    # 外键：所属用户，关联users表
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 外键：所属分类，关联categories表
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # 创建时间：作品集创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 更新时间：作品集最后更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系：一个作品集包含多张图片，按sort_order排序
    images = db.relationship('Image', backref='portfolio', lazy=True, order_by='Image.sort_order')
    
    # 关系：一个作品集可以有多个标签，多对多关系
    tags = db.relationship('Tag', secondary=portfolio_tags, lazy='subquery',
                          backref=db.backref('portfolios', lazy=True))


class Image(db.Model):
    """
    图片模型
    
    存储作品集中的图片信息，包括原图路径、缩略图路径等。
    支持图片排序、标注等功能。
    
    字段说明：
    - id: 图片唯一标识符，主键自增
    - filename: 图片文件名
    - filepath: 图片存储路径（原图）
    - thumbnail_path: 缩略图路径，用于快速加载预览
    - sort_order: 排序顺序，数字越小越靠前
    - portfolio_id: 所属作品集ID，外键关联portfolios表
    - created_at: 图片上传时间
    - updated_at: 图片更新时间
    
    关系说明：
    - annotations: 图片上的标注，一对多关系
    """
    __tablename__ = 'images'
    
    # 主键：图片唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 文件名：图片的原始文件名
    filename = db.Column(db.String(255), nullable=False)
    
    # 文件路径：图片在服务器上的存储路径（原图）
    filepath = db.Column(db.String(255), nullable=False)
    
    # 缩略图路径：用于快速加载预览的小图
    thumbnail_path = db.Column(db.String(255))
    
    # 排序顺序：数字越小越靠前，用于自定义图片顺序
    sort_order = db.Column(db.Integer, default=0)
    
    # 外键：所属作品集，关联portfolios表
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    
    # 创建时间：图片上传时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 更新时间：图片信息更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系：一张图片可以有多个标注
    annotations = db.relationship('Annotation', backref='image', lazy=True)


class FilterPreset(db.Model):
    """
    滤镜预设模型
    
    存储用户保存的滤镜参数预设，方便快速应用常用滤镜效果。
    支持公开分享和私有预设。
    
    字段说明：
    - id: 预设唯一标识符，主键自增
    - name: 预设名称，如"日系清新"、"复古胶片"
    - description: 预设描述，说明滤镜效果
    - params: 滤镜参数，JSON格式存储所有滤镜参数
    - user_id: 创建者用户ID，外键关联users表
    - is_public: 是否公开，公开的预设可以被其他用户使用
    - created_at: 预设创建时间
    - updated_at: 预设更新时间
    """
    __tablename__ = 'filter_presets'
    
    # 主键：预设唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 预设名称：如"日系清新"、"复古胶片"、"电影感"等
    name = db.Column(db.String(50), nullable=False)
    
    # 预设描述：详细说明滤镜效果和使用场景
    description = db.Column(db.Text)
    
    # 滤镜参数：JSON格式存储所有滤镜参数
    # 包括：亮度、对比度、饱和度、色相、锐化、曝光等
    params = db.Column(db.JSON, nullable=False)
    
    # 外键：创建者用户，关联users表
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # 是否公开：True表示所有用户都可以使用，False表示仅创建者可用
    is_public = db.Column(db.Boolean, default=False)
    
    # 创建时间：预设创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 更新时间：预设更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ClientFeedback(db.Model):
    """
    客户反馈模型
    
    存储客户对作品集的反馈意见，方便摄影师根据反馈进行修改。
    支持客户通过预览链接提交反馈。
    
    字段说明：
    - id: 反馈唯一标识符，主键自增
    - portfolio_id: 作品集ID，外键关联portfolios表
    - client_name: 客户名称
    - feedback_content: 反馈内容
    - created_at: 反馈提交时间
    """
    __tablename__ = 'client_feedback'
    
    # 主键：反馈唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键：关联的作品集
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    
    # 客户名称：提交反馈的客户姓名
    client_name = db.Column(db.String(50), nullable=False)
    
    # 反馈内容：客户对作品集的意见和建议
    feedback_content = db.Column(db.Text)
    
    # 创建时间：反馈提交时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Annotation(db.Model):
    """
    标注模型
    
    存储图片上的标注信息，用于标记需要修改的区域。
    支持在图片上绘制标注、添加文字说明等功能。
    
    字段说明：
    - id: 标注唯一标识符，主键自增
    - image_id: 图片ID，外键关联images表
    - annotation_data: 标注数据，JSON格式存储坐标、形状、文字等
    - created_at: 标注创建时间
    """
    __tablename__ = 'annotations'
    
    # 主键：标注唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键：关联的图片
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    
    # 标注数据：JSON格式存储标注信息
    # 包括：坐标位置、形状类型、文字说明、颜色等
    annotation_data = db.Column(db.Text, nullable=False)
    
    # 创建时间：标注创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PreviewLink(db.Model):
    """
    预览链接模型
    
    生成作品集的预览链接，方便分享给客户查看。
    支持设置过期时间，确保安全性。
    
    字段说明：
    - id: 链接唯一标识符，主键自增
    - portfolio_id: 作品集ID，外键关联portfolios表
    - token: 访问令牌，用于验证链接有效性
    - expire_time: 过期时间，过期后链接失效
    - created_at: 链接创建时间
    - is_valid: 链接是否有效，可用于手动禁用链接
    """
    __tablename__ = 'preview_links'
    
    # 主键：链接唯一标识符
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键：关联的作品集
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    
    # 访问令牌：用于验证链接有效性，唯一且随机生成
    token = db.Column(db.String(100), unique=True, nullable=False)
    
    # 过期时间：链接过期后无法访问
    expire_time = db.Column(db.DateTime, nullable=False)
    
    # 创建时间：链接创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 是否有效：可用于手动禁用链接
    is_valid = db.Column(db.Boolean, default=True)
