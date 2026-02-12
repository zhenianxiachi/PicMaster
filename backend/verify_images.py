from models import db, Portfolio, Image
from app import app

# 验证图片是否正确添加到数据库
def verify_images():
    with app.app_context():
        # 获取所有作品集
        portfolios = Portfolio.query.all()
        
        print("验证数据库中的图片记录：")
        total_images = 0
        
        for portfolio in portfolios:
            images = Image.query.filter_by(portfolio_id=portfolio.id).all()
            print(f"\n作品集 {portfolio.name} ({portfolio.id}):")
            print(f"  图片数量: {len(images)}")
            
            for image in images:
                print(f"  - 图片ID: {image.id}, 文件名: {image.filename}")
                print(f"     原图路径: {image.filepath}")
                print(f"     缩略图路径: {image.thumbnail_path}")
                print(f"     排序序号: {image.sort_order}")
                
                # 检查文件是否存在
                import os
                if os.path.exists(image.filepath):
                    print(f"     原图存在")
                else:
                    print(f"     原图不存在")
                    
                if os.path.exists(image.thumbnail_path):
                    print(f"     缩略图存在")
                else:
                    print(f"     缩略图不存在")
            
            total_images += len(images)
        
        print(f"\n总计: {len(portfolios)} 个作品集, {total_images} 张图片")

if __name__ == '__main__':
    verify_images()
