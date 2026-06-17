#!/usr/bin/env python3
"""
算法可视化工具 - 生成图像+HTML 报告

功能:
1. 可视化采样网格 overlay
2. 生成字符矩阵热力图
3. 可视化匹配过程 (得分对比)
4. 生成逐步执行报告 (HTML/Markdown)

使用示例:
    python tools/visualizer.py --image test.png --height 50 --output-dir viz_output
"""

import argparse
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json


class AlgorithmVisualizer:
    """算法可视化工具类"""
    
    def __init__(self, output_dir='viz_output'):
        """初始化工具
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def visualize_sampling_grid(self, image, sampling_array, save_path=None):
        """可视化采样网格 overlay
        
        Args:
            image: 原始图像 (numpy array)
            sampling_array: 采样数组
            save_path: 保存路径 (可选)
        
        Returns:
            str: 生成的文件路径
        """
        # 转换为彩色图像
        if len(image.shape) == 2:
            color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            color_image = image.copy()
        
        # 计算网格尺寸
        output_height, output_width = sampling_array.shape[:2]
        block_h = image.shape[0] // output_height
        block_w = image.shape[1] // output_width
        
        # 绘制网格线
        for y in range(0, image.shape[0], block_h):
            cv2.line(color_image, (0, y), (image.shape[1], y), (0, 255, 0), 1)
        
        for x in range(0, image.shape[1], block_w):
            cv2.line(color_image, (x, 0), (x, image.shape[0]), (0, 255, 0), 1)
        
        # 保存图像
        if save_path is None:
            save_path = self.output_dir / 'sampling_grid.png'
        
        cv2.imwrite(str(save_path), color_image)
        return str(save_path)
    
    def visualize_character_matrix(self, char_data, wide_char_data, save_path=None):
        """生成字符矩阵热力图
        
        Args:
            char_data: 普通字符数据列表
            wide_char_data: 宽字符数据列表
            save_path: 保存路径 (可选)
        
        Returns:
            str: 生成的文件路径
        """
        import matplotlib.pyplot as plt
        
        # 创建子图
        fig, axes = plt.subplots(2, 5, figsize=(15, 6))
        
        # 绘制前 5 个普通字符
        for i in range(min(5, len(char_data))):
            char_info = char_data[i]
            matrix = char_info['matrix']
            axes[0, i].imshow(matrix, cmap='gray')
            axes[0, i].set_title(f"'{char_info['character']}'")
            axes[0, i].axis('off')
        
        # 绘制前 5 个宽字符
        for i in range(min(5, len(wide_char_data))):
            char_info = wide_char_data[i]
            matrix = char_info['matrix']
            axes[1, i].imshow(matrix, cmap='gray')
            axes[1, i].set_title(f"'{char_info['character']}' (wide)")
            axes[1, i].axis('off')
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = self.output_dir / 'character_matrices.png'
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(save_path)
    
    def visualize_matching_process(self, rectangle, char_data, matched_char, 
                                   top_k=5, save_path=None):
        """可视化单个匹配过程 (得分对比)
        
        Args:
            rectangle: 采样块矩阵
            char_data: 字符数据列表
            matched_char: 匹配的字符信息
            top_k: 显示前 K 个候选
            save_path: 保存路径 (可选)
        
        Returns:
            str: 生成的文件路径
        """
        import matplotlib.pyplot as plt
        
        # 计算所有字符的得分
        scores = []
        for char_info in char_data:
            diff = np.abs(rectangle - char_info['matrix'])
            score = np.sum(diff)
            scores.append({
                'char': char_info['character'],
                'score': score,
                'is_matched': char_info == matched_char
            })
        
        # 按得分排序
        scores.sort(key=lambda x: x['score'])
        top_candidates = scores[:top_k]
        
        # 创建图表
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # 左侧: 采样块
        axes[0].imshow(rectangle, cmap='gray')
        axes[0].set_title('Sampling Block')
        axes[0].axis('off')
        
        # 右侧: 得分柱状图
        chars = [c['char'] for c in top_candidates]
        scores_list = [c['score'] for c in top_candidates]
        colors = ['green' if c['is_matched'] else 'blue' for c in top_candidates]
        
        bars = axes[1].barh(chars, scores_list, color=colors)
        axes[1].set_xlabel('SAD Score (lower is better)')
        axes[1].set_title(f'Top {top_k} Candidates')
        axes[1].invert_yaxis()
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = self.output_dir / 'matching_process.png'
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(save_path)
    
    def generate_step_by_step_report(self, input_data, output_dir=None):
        """生成完整的逐步执行报告 (HTML)
        
        Args:
            input_data: 输入数据字典，包含:
                - image: 原始图像
                - sampling_array: 采样数组
                - char_data: 字符数据
                - wide_char_data: 宽字符数据
                - output_string: 最终输出
            output_dir: 输出目录 (可选)
        
        Returns:
            str: HTML 报告路径
        """
        if output_dir is None:
            output_dir = self.output_dir
        
        report_path = output_dir / 'report.html'
        
        # 生成可视化图像
        grid_path = self.visualize_sampling_grid(
            input_data['image'], 
            input_data['sampling_array']
        )
        
        matrix_path = self.visualize_character_matrix(
            input_data['char_data'],
            input_data['wide_char_data']
        )
        
        # 生成 HTML 报告
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UnicodeArt 算法可视化报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
        .section {{ margin: 30px 0; }}
        .image-container {{ text-align: center; margin: 20px 0; }}
        img {{ max-width: 100%; height: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .output {{ background: #f5f5f5; padding: 20px; border-radius: 5px; 
                   font-family: monospace; white-space: pre-wrap; }}
        .stats {{ display: flex; gap: 20px; }}
        .stat-box {{ background: #e3f2fd; padding: 15px; border-radius: 5px; flex: 1; }}
        .stat-label {{ font-size: 12px; color: #666; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #1976d2; }}
    </style>
</head>
<body>
    <h1>🎨 UnicodeArt 算法可视化报告</h1>
    
    <div class="section">
        <h2> 统计信息</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">图像尺寸</div>
                <div class="stat-value">{input_data['image'].shape[1]}×{input_data['image'].shape[0]}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">输出尺寸</div>
                <div class="stat-value">{input_data['sampling_array'].shape[1]}×{input_data['sampling_array'].shape[0]}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">字符集大小</div>
                <div class="stat-value">{len(input_data['char_data']) + len(input_data['wide_char_data'])}</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2> 采样网格可视化</h2>
        <div class="image-container">
            <img src="{Path(grid_path).name}" alt="Sampling Grid">
        </div>
        <p><strong>说明:</strong> 绿色线条表示采样块的边界。每个块将被缩放并匹配到最相似的字符。</p>
    </div>
    
    <div class="section">
        <h2>🔤 字符矩阵热力图</h2>
        <div class="image-container">
            <img src="{Path(matrix_path).name}" alt="Character Matrices">
        </div>
        <p><strong>说明:</strong> 上方为普通字符，下方为宽字符。颜色越深表示像素值越低 (黑色)。</p>
    </div>
    
    <div class="section">
        <h2>✨ 最终输出</h2>
        <div class="output">{input_data['output_string']}</div>
    </div>
    
    <div class="section">
        <h2> 算法流程</h2>
        <ol>
            <li><strong>图像预处理:</strong> 灰度化、尺寸调整</li>
            <li><strong>网格划分:</strong> 根据输出尺寸计算采样块大小</li>
            <li><strong>采样矩阵生成:</strong> 对每个块进行缩放和归一化</li>
            <li><strong>字符匹配:</strong> 与预计算字符矩阵比较 (SAD)</li>
            <li><strong>输出组装:</strong> 拼接字符，处理宽字符跳过逻辑</li>
        </ol>
    </div>
    
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
        <p>生成时间: {Path(__file__).parent.parent.name} | UnicodeArt 算法可视化工具 v1.0</p>
    </footer>
</body>
</html>
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML 报告已生成: {report_path}")
        return str(report_path)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='UnicodeArt 算法可视化工具')
    parser.add_argument('--image', required=True, help='输入图像路径')
    parser.add_argument('--height', type=int, default=50, help='输出高度')
    parser.add_argument('--width', type=int, default=None, help='输出宽度 (可选)')
    parser.add_argument('--font', default=r'C:\Windows\Fonts\SimSun.ttc', 
                       help='字体路径')
    parser.add_argument('--output-dir', default='viz_output', 
                       help='输出目录')
    parser.add_argument('--no-report', action='store_true', 
                       help='不生成 HTML 报告')
    
    args = parser.parse_args()
    
    # 导入核心模块
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
    from unicodeart.unicodeart_util import (
        get_sampling_array, get_char_data, get_final_output
    )
    
    # ✅ 修正: 直接使用 cv2.imread 加载图像
    print("📷 加载图像...")
    if not Path(args.image).exists():
        print(f"❌ 错误: 文件不存在 - {args.image}")
        exit(1)
    
    baseimg = cv2.imread(str(args.image), cv2.IMREAD_GRAYSCALE)
    if baseimg is None:
        print(f"❌ 错误: 无法读取图像 - {args.image}")
        exit(1)
    
    # 生成采样数组
    print("🔲 生成采样数组...")
    sampling_array = get_sampling_array(
        baseimg,
        height=args.height,
        width=args.width,
        matrix_size=5
    )
    
    # 预计算字符矩阵
    print("🔤 预计算字符矩阵...")
    char_data, wide_char_data = get_char_data(
        None,  # 使用默认字符集
        args.font,
        matrix_size=5,
        vertical_horizontal_ratio=2.0
    )
    
    # 生成最终输出
    print("✨ 生成字符画...")
    output_string = get_final_output(
        sampling_array,
        char_data,
        wide_char_data,
        output_path=None,
        wide_sum_ratio=2.0
    )
    
    # 创建可视化器
    visualizer = AlgorithmVisualizer(args.output_dir)
    
    # 准备输入数据
    input_data = {
        'image': baseimg,
        'sampling_array': sampling_array,
        'char_data': char_data,
        'wide_char_data': wide_char_data,
        'output_string': output_string
    }
    
    # 生成报告
    if not args.no_report:
        print("📊 生成可视化报告...")
        report_path = visualizer.generate_step_by_step_report(input_data)
        print(f"\n✅ 完成! 报告路径: {report_path}")
    else:
        print("\n✅ 完成!")


if __name__ == '__main__':
    main()
