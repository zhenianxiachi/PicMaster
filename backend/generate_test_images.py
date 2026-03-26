from models import db, Portfolio, Image
from app import app
import os
import uuid
import requests

# 生成测试图片的函数
def generate_test_images():
    with app.app_context():
        # 获取所有作品集
        portfolios = Portfolio.query.all()
        
        # 检查每个作品集的图片数量
        for portfolio in portfolios:
            current_image_count = len(portfolio.images)
            print(f"作品集 {portfolio.name} 当前有 {current_image_count} 张图片")
            
            # 如果图片数量少于5张，添加随机图片
            if current_image_count < 5:
                # 获取上传目录
                upload_folder = app.config['UPLOAD_FOLDER']
                
                # 生成随机图片
                for i in range(5 - current_image_count):
                    # 生成唯一文件名
                    unique_filename = f"{uuid.uuid4().hex}_random_image_{i + current_image_count + 1}.jpg"
                    
                    # 确保上传目录存在
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # 生成随机图片路径
                    filepath = os.path.join(upload_folder, unique_filename)
                    thumbnail_path = os.path.join(upload_folder, f"thumb_{unique_filename}")
                    
                    # 从picsum.photos获取随机图片
                    response = requests.get(f"https://picsum.photos/800/600")
                    if response.status_code == 200:
                        # 获取图片内容
                        image_content = response.content
                        
                        # 保存原图
                        with open(filepath, 'wb') as f:
                            f.write(image_content)
                        
                        # 保存缩略图（这里简化处理，直接复制原图）
                        with open(thumbnail_path, 'wb') as f:
                            f.write(image_content)
                        
                        # 获取当前最大排序序号
                        max_sort = db.session.query(db.func.max(Image.sort_order)).filter_by(portfolio_id=portfolio.id).scalar() or 0
                        
                        # 创建图片记录
                        new_image = Image(
                            filename=unique_filename,
                            filepath=filepath,
                            thumbnail_path=thumbnail_path,
                            sort_order=max_sort + 1,
                            portfolio_id=portfolio.id
                        )
                        db.session.add(new_image)
                        print(f"已添加随机图片 {unique_filename} 到作品集 {portfolio.name}")
        
        # 提交所有更改
        db.session.commit()
        print("随机图片生成完成！")

if __name__ == '__main__':
    generate_test_images()
