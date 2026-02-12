# 检查数据库中的作品集数据
from models import db, Portfolio, Image
from app import app

with app.app_context():
    # 查询所有作品集
    portfolios = Portfolio.query.all()
    
    print(f"找到 {len(portfolios)} 个作品集：")
    for portfolio in portfolios:
        print(f"\n作品集 ID: {portfolio.id}")
        print(f"  名称: {portfolio.name}")
        print(f"  客户名称: {portfolio.client_name}")
        print(f"  拍摄日期: {portfolio.shoot_date}")
        print(f"  图片数量: {len(portfolio.images)}")
        print(f"  创建时间: {portfolio.created_at}")
        
        # 打印关联的图片
        print(f"  图片列表:")
        for img in portfolio.images:
            print(f"    - 图片 ID: {img.id}, 文件名: {img.filename}, 路径: {img.filepath}")