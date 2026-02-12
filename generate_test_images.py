#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成测试图片脚本
用于生成各种类型的测试图片，用于测试PicMaster系统
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random

# 输出目录
output_dir = "test_images"
os.makedirs(output_dir, exist_ok=True)

# 图片尺寸列表
image_sizes = [
    (300, 200),    # 小尺寸
    (800, 600),    # 中尺寸
    (1920, 1080),  # 大尺寸
    (2048, 1365),  # 2:3 比例（摄影常用）
    (1080, 1080)   # 正方形
]

# 颜色列表
colors = [
    (255, 0, 0),      # 红色
    (0, 255, 0),      # 绿色
    (0, 0, 255),      # 蓝色
    (255, 255, 0),    # 黄色
    (255, 0, 255),    # 紫色
    (0, 255, 255),    # 青色
    (255, 165, 0),    # 橙色
    (128, 0, 128),    # 深紫色
    (169, 169, 169),  # 深灰色
    (255, 215, 0)     # 金色
]

# 主题列表
themes = [
    "风景",
    "人像",
    "产品",
    "建筑",
    "美食",
    "动物",
    "植物",
    "抽象",
    "科技",
    "艺术"
]

def generate_solid_color_image(size, color, filename):
    """生成纯色背景图片"""
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # 添加文字说明
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text = f"{size[0]}x{size[1]}"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    # 绘制文字背景
    draw.rectangle(
        [(text_x-10, text_y-5), (text_x+text_width+10, text_y+text_height+5)],
        fill=(255, 255, 255, 128),
        outline=color,
        width=2
    )
    
    # 绘制文字
    draw.text((text_x, text_y), text, fill=color, font=font)
    
    img.save(os.path.join(output_dir, filename), quality=95)
    print(f"生成: {filename}")

def generate_gradient_image(size, start_color, end_color, filename):
    """生成渐变背景图片"""
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    width, height = size
    
    # 生成垂直渐变
    for y in range(height):
        # 计算当前行的颜色
        r = start_color[0] + (end_color[0] - start_color[0]) * y // height
        g = start_color[1] + (end_color[1] - start_color[1]) * y // height
        b = start_color[2] + (end_color[2] - start_color[2]) * y // height
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 添加文字
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text = "渐变背景"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    draw.rectangle(
        [(text_x-10, text_y-5), (text_x+text_width+10, text_y+text_height+5)],
        fill=(255, 255, 255, 128)
    )
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
    
    img.save(os.path.join(output_dir, filename), quality=95)
    print(f"生成: {filename}")

def generate_geometry_image(size, filename):
    """生成几何图形图片"""
    img = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    width, height = size
    
    # 绘制随机几何图形
    for _ in range(5):
        shape_type = random.choice(['rectangle', 'circle', 'line', 'ellipse'])
        color = random.choice(colors)
        
        if shape_type == 'rectangle':
            x1 = random.randint(0, width//2)
            y1 = random.randint(0, height//2)
            x2 = random.randint(width//2, width)
            y2 = random.randint(height//2, height)
            draw.rectangle([(x1, y1), (x2, y2)], fill=color, outline=(0, 0, 0), width=2)
        
        elif shape_type == 'circle':
            x = random.randint(50, width-50)
            y = random.randint(50, height-50)
            radius = random.randint(20, 100)
            draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], fill=color, outline=(0, 0, 0), width=2)
        
        elif shape_type == 'line':
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line([(x1, y1), (x2, y2)], fill=color, width=5)
        
        elif shape_type == 'ellipse':
            x1 = random.randint(0, width//2)
            y1 = random.randint(0, height//2)
            x2 = random.randint(width//2, width)
            y2 = random.randint(height//2, height)
            draw.ellipse([(x1, y1), (x2, y2)], fill=color, outline=(0, 0, 0), width=2)
    
    # 添加文字
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text = "几何图形"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    text_x = 10
    text_y = 10
    
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
    
    img.save(os.path.join(output_dir, filename), quality=95)
    print(f"生成: {filename}")

def generate_theme_image(size, theme, filename):
    """生成主题测试图片"""
    # 生成渐变背景
    start_color = random.choice(colors)
    end_color = random.choice(colors)
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    width, height = size
    
    # 生成渐变
    for y in range(height):
        r = start_color[0] + (end_color[0] - start_color[0]) * y // height
        g = start_color[1] + (end_color[1] - start_color[1]) * y // height
        b = start_color[2] + (end_color[2] - start_color[2]) * y // height
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 添加主题文字
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text = theme
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # 文字描边效果
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx != 0 or dy != 0:
                draw.text((text_x+dx, text_y+dy), text, fill=(0, 0, 0), font=font)
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    # 添加尺寸信息
    try:
        small_font = ImageFont.truetype("arial.ttf", 18)
    except:
        small_font = ImageFont.load_default()
    
    size_text = f"{size[0]}x{size[1]}"
    size_width, size_height = draw.textbbox((0, 0), size_text, font=small_font)[2:4]
    draw.text((width - size_width - 10, height - size_height - 10), size_text, fill=(255, 255, 255), font=small_font)
    
    img.save(os.path.join(output_dir, filename), quality=95)
    print(f"生成: {filename}")

def generate_blur_image(size, filename):
    """生成模糊效果图片"""
    # 先生成清晰图片
    img = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 绘制文字
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    text = "BLUR TEST"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
    
    # 添加模糊效果
    img = img.filter(ImageFilter.GaussianBlur(radius=5))
    
    img.save(os.path.join(output_dir, filename), quality=95)
    print(f"生成: {filename}")

def main():
    """主函数"""
    print("开始生成测试图片...")
    
    # 生成纯色背景图片
    for i, size in enumerate(image_sizes):
        color = colors[i % len(colors)]
        filename = f"solid_{size[0]}x{size[1]}.jpg"
        generate_solid_color_image(size, color, filename)
    
    # 生成渐变背景图片
    for i, size in enumerate(image_sizes[:3]):
        start_color = colors[i % len(colors)]
        end_color = colors[(i+2) % len(colors)]
        filename = f"gradient_{size[0]}x{size[1]}.jpg"
        generate_gradient_image(size, start_color, end_color, filename)
    
    # 生成几何图形图片
    for i, size in enumerate(image_sizes[:3]):
        filename = f"geometry_{size[0]}x{size[1]}.jpg"
        generate_geometry_image(size, filename)
    
    # 生成主题图片
    for i, theme in enumerate(themes[:5]):
        size = image_sizes[i % len(image_sizes)]
        filename = f"theme_{theme}_{size[0]}x{size[1]}.jpg"
        generate_theme_image(size, theme, filename)
    
    # 生成模糊效果图片
    for i, size in enumerate(image_sizes[:2]):
        filename = f"blur_{size[0]}x{size[1]}.jpg"
        generate_blur_image(size, filename)
    
    # 生成PNG格式透明背景图片
    for i in range(2):
        size = image_sizes[i]
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制半透明形状
        draw.rectangle([(50, 50), (size[0]-50, size[1]-50)], fill=(255, 0, 0, 128), outline=(255, 0, 0), width=3)
        
        filename = f"transparent_{size[0]}x{size[1]}.png"
        img.save(os.path.join(output_dir, filename))
        print(f"生成: {filename}")
    
    print(f"\n测试图片生成完成！共生成 {len(os.listdir(output_dir))} 张图片")
    print(f"图片保存在：{os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()
