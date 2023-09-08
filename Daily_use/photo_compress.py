# !/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'tianyi'
__date__ = '2023/9/8 15:17 '
__file__ = 'photo_compress.py'

import argparse
from PIL import Image
import os
import shutil


def compress_image(input_image_path, output_image_path, target_size):
    # 复制输入图像到输出图像路径
    shutil.copyfile(input_image_path, output_image_path)

    # 打开输出图像
    image = Image.open(output_image_path)

    # 将目标文件大小参数解析为字节数
    target_size = target_size.lower()
    if target_size[-1] == 'k':
        target_size = int(float(target_size[:-1]) * 1024)
    elif target_size[-1] == 'm':
        target_size = int(float(target_size[:-1]) * 1024 * 1024)
    elif target_size[-1] == 'g':
        target_size = int(float(target_size[:-1]) * 1024 * 1024 * 1024)

    # 压缩图像，调整压缩质量以逼近目标文件大小
    quality = 85  # 初始压缩质量
    while True:
        image.save(output_image_path, optimize=True, quality=quality)
        file_size = os.path.getsize(output_image_path)
        if file_size <= target_size:
            break
        quality -= 5  # 每次降低压缩质量 5
        if quality <= 0:
            break


# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='Image Compression')

# 添加输入文件参数
parser.add_argument('-file', dest='input_file', required=True, help='Input image file path')

# 添加目标文件大小参数
parser.add_argument('-size', dest='target_size', required=True, help='Target file size (e.g., 1k, 1m, 1g)')

# 解析命令行参数
args = parser.parse_args()

# 输入图像路径
input_image_path_real = args.input_file

# 输出图像路径（在输入图像路径的基础上添加后缀）
output_dir = os.path.dirname(input_image_path_real)
output_image_name = os.path.splitext(os.path.basename(input_image_path_real))[0] + '_compressed.jpg'
output_image_path_real = os.path.join(output_dir, output_image_name)

# 目标文件大小参数
target_size_real = args.target_size

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 调用函数进行图像压缩
compress_image(input_image_path_real, output_image_path_real, target_size_real)
