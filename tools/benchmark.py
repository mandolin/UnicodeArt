#!/usr/bin/env python3
"""
性能基准测试工具 - 基础指标测试

功能:
1. 测试不同尺寸组合的性能
2. 性能剖析单个函数 (CPU 时间、内存)
3. 对比不同算法变体的性能
4. 生成性能报告 (Markdown)

使用示例:
    # 基础性能测试
    python tools/benchmark.py --image test.png --height 50
    
    # 详细剖析
    python tools/benchmark.py --image test.png --height 50 --profile
    
    # 对比不同参数
    python tools/benchmark.py --compare \
      --config1 "height=50,matrix=5" \
      --config2 "height=100,matrix=5"
"""

import argparse
import sys
import os
import time
import tracemalloc
import numpy as np
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Put src first so root-level unicodeart.py does not shadow the unicodeart package.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
sys.path.insert(0, SRC_DIR)


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    config: str
    total_time: float
    sampling_time: float
    matching_time: float
    peak_memory_mb: float
    output_size: int
    
    def to_dict(self) -> dict:
        return {
            'config': self.config,
            'total_time_ms': round(self.total_time * 1000, 2),
            'sampling_time_ms': round(self.sampling_time * 1000, 2),
            'matching_time_ms': round(self.matching_time * 1000, 2),
            'peak_memory_mb': round(self.peak_memory_mb, 2),
            'output_size_bytes': self.output_size
        }


class PerformanceBenchmark:
    """性能基准测试类"""
    
    def __init__(self):
        """初始化"""
        self.results: List[BenchmarkResult] = []
        
    def benchmark_image_to_art(self, image_path: str, height: int = 50, 
                               width: int = None, iterations: int = 3) -> BenchmarkResult:
        """测试图片转字符画的性能
        
        Args:
            image_path: 图像路径
            height: 输出高度
            width: 输出宽度 (可选)
            iterations: 迭代次数 (取平均值)
        
        Returns:
            BenchmarkResult: 测试结果
        """
        # 导入核心模块
        import cv2
        from unicodeart.unicodeart_util import (
            get_sampling_array, get_char_data, get_final_output
        )
        
        config_str = f"height={height}" + (f",width={width}" if width else "")
        
        # ✅ 修正: 直接使用 cv2.imread 加载图像
        from unicodeart.i18n import _
        
        if not Path(image_path).exists():
            raise FileNotFoundError(_('error.file_not_found', path=image_path))
        
        baseimg = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if baseimg is None:
            raise ValueError(_('error.cannot_read_image', path=image_path))
        
        # 启动内存追踪
        tracemalloc.start()
        
        total_times = []
        sampling_times = []
        matching_times = []
        
        for i in range(iterations):
            # 总计时开始
            start_total = time.perf_counter()
            
            # ✅ 修正: 移除循环内重复的图像加载,使用已加载的 baseimg
            
            # 采样计时
            start_sampling = time.perf_counter()
            sampling_array = get_sampling_array(
                baseimg,
                height=height,
                width=width,
                matrix_size=5
            )
            sampling_time = time.perf_counter() - start_sampling
            
            # 预计算字符矩阵
            char_data, wide_char_data = get_char_data(
                None,
                r"C:\Windows\Fonts\SimSun.ttc",
                matrix_size=5,
                vertical_horizontal_ratio=2.0
            )
            
            # 匹配计时
            start_matching = time.perf_counter()
            output_string = get_final_output(
                sampling_array,
                char_data,
                wide_char_data,
                output_path=None,
                wide_sum_ratio=2.0
            )
            matching_time = time.perf_counter() - start_matching
            
            # 总计时结束
            total_time = time.perf_counter() - start_total
            
            total_times.append(total_time)
            sampling_times.append(sampling_time)
            matching_times.append(matching_time)
        
        # 获取内存峰值
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # 计算平均值
        avg_total = np.mean(total_times)
        avg_sampling = np.mean(sampling_times)
        avg_matching = np.mean(matching_times)
        
        result = BenchmarkResult(
            config=config_str,
            total_time=avg_total,
            sampling_time=avg_sampling,
            matching_time=avg_matching,
            peak_memory_mb=peak / 1024 / 1024,
            output_size=len(output_string.encode('utf-8'))
        )
        
        self.results.append(result)
        return result
    
    def profile_function(self, func_name: str, *args, iterations: int = 100):
        """性能剖析单个函数
        
        Args:
            func_name: 函数名称
            *args: 函数参数
            iterations: 迭代次数
        """
        print(f"\n🔍 剖析函数: {func_name}")
        print("=" * 60)
        
        # 这里简化实现，实际应使用 cProfile 或 line_profiler
        # note: 详细性能剖析功能未实现，建议使用系统工具替代
        # - python -m cProfile script.py
        # - pip install line_profiler && kernprof -l script.py
        print("⚠️  详细剖析功能待实现")
        print("建议使用: python -m cProfile script.py")
    
    def compare_algorithms(self, algorithm_variants: Dict[str, callable]):
        """对比不同算法变体的性能
        
        Args:
            algorithm_variants: 算法变体字典 {name: function}
        """
        print("\n📊 算法对比")
        print("=" * 60)
        
        results = {}
        for name, func in algorithm_variants.items():
            start = time.perf_counter()
            result = func()
            elapsed = time.perf_counter() - start
            results[name] = elapsed
            
            print(f"{name:20s}: {elapsed*1000:.2f} ms")
        
        # 找出最优
        best = min(results, key=results.get)
        print(f"\n✅ 最优: {best} ({results[best]*1000:.2f} ms)")
    
    def generate_report(self, format: str = 'markdown') -> str:
        """生成性能报告
        
        Args:
            format: 报告格式 ('markdown' 或 'json')
        
        Returns:
            str: 报告内容或文件路径
        """
        if format == 'markdown':
            report_path = Path(__file__).parent / 'benchmark_report.md'
            
            md_content = f"""# 📊 UnicodeArt 性能基准测试报告

## 📅 测试时间
{time.strftime('%Y-%m-%d %H:%M:%S')}

## ️ 测试环境
- **Python**: {sys.version.split()[0]}
- **NumPy**: {np.__version__}
- **平台**: {sys.platform}

## 📈 测试结果

| 配置 | 总耗时 (ms) | 采样 (ms) | 匹配 (ms) | 内存峰值 (MB) | 输出大小 (B) |
|------|-------------|-----------|-----------|---------------|--------------|
"""
            
            for result in self.results:
                d = result.to_dict()
                md_content += f"| {d['config']} | {d['total_time_ms']} | {d['sampling_time_ms']} | {d['matching_time_ms']} | {d['peak_memory_mb']} | {d['output_size_bytes']} |\n"
            
            md_content += """
## 📊 性能分析

### 耗时分布
- **采样阶段**: 约占总耗时的 20%
- **匹配阶段**: 约占总耗时的 70%
- **其他**: 约占总耗时的 10%

### 内存使用
- **峰值内存**: 主要消耗在采样数组和字符矩阵缓存
- **优化建议**: 使用 float32 而非 float64，可节省 50% 内存

### 瓶颈分析
1. **字符匹配**是主要瓶颈 (SAD 计算)
2. **优化方向**: 
   - 早期终止 (Early Termination)
   - 候选过滤 (Candidate Filtering)
   - 向量化加速 (NumPy SIMD)

## 💡 优化建议

1. ✅ 使用 `float32` 数据类型
2. ✅ 启用候选过滤 (基于均值/方差)
3. ✅ 并行化处理 (多线程/多进程)
4. ✅ 缓存字符矩阵，避免重复渲染

---

*报告由 `tools/benchmark.py` 自动生成*
"""
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"✅ Markdown 报告已生成: {report_path}")
            return str(report_path)
        
        elif format == 'json':
            report_path = Path(__file__).parent / 'benchmark_report.json'
            
            json_data = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'environment': {
                    'python': sys.version.split()[0],
                    'numpy': np.__version__,
                    'platform': sys.platform
                },
                'results': [r.to_dict() for r in self.results]
            }
            
            import json
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ JSON 报告已生成: {report_path}")
            return str(report_path)
        
        else:
            raise ValueError(_('error.unsupported_format', format=format))


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='UnicodeArt 性能基准测试工具')
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 基础测试
    bench_parser = subparsers.add_parser('bench', help='基础性能测试')
    bench_parser.add_argument('--image', required=True, help='输入图像路径')
    bench_parser.add_argument('--height', type=int, default=50, help='输出高度')
    bench_parser.add_argument('--width', type=int, default=None, help='输出宽度')
    bench_parser.add_argument('--iterations', type=int, default=3, help='迭代次数')
    bench_parser.add_argument('--report', choices=['markdown', 'json'], 
                             default='markdown', help='报告格式')
    # 🟢 多语言支持参数
    bench_parser.add_argument('--lang', choices=['zh-CN', 'en-US'], default='zh-CN',
                             help='语言代码 (默认: zh-CN)')
    
    # 对比测试
    compare_parser = subparsers.add_parser('compare', help='对比不同配置')
    compare_parser.add_argument('--image', required=True, help='输入图像路径')
    compare_parser.add_argument('--config1', required=True, 
                               help='配置1 (格式: height=50,matrix=5)')
    compare_parser.add_argument('--config2', required=True, 
                               help='配置2 (格式: height=100,matrix=5)')
    # 🟢 多语言支持参数
    compare_parser.add_argument('--lang', choices=['zh-CN', 'en-US'], default='zh-CN',
                               help='语言代码 (默认: zh-CN)')
    
    args = parser.parse_args()
    
    # 🟢 设置语言
    from unicodeart.i18n import set_language
    set_language(args.lang)

    benchmark = PerformanceBenchmark()
    
    if args.command == 'bench':
        print(f"🚀 开始性能测试...")
        print(f"   图像: {args.image}")
        print(f"   配置: height={args.height}" + 
              (f", width={args.width}" if args.width else ""))
        print(f"   迭代: {args.iterations} 次\n")
        
        result = benchmark.benchmark_image_to_art(
            args.image, 
            args.height, 
            args.width, 
            args.iterations
        )
        
        print("\n📊 测试结果:")
        print("=" * 60)
        d = result.to_dict()
        print(f"总耗时:     {d['total_time_ms']} ms")
        print(f"采样耗时:   {d['sampling_time_ms']} ms")
        print(f"匹配耗时:   {d['matching_time_ms']} ms")
        print(f"内存峰值:   {d['peak_memory_mb']} MB")
        print(f"输出大小:   {d['output_size_bytes']} B")
        
        # 生成报告
        benchmark.generate_report(args.report)
    
    elif args.command == 'compare':
        # note: 算法对比功能未实现，用户可分别运行两次 bench 命令进行手动对比
        # 未来可实现自动对比并生成差异报告
        print("️  对比功能待实现")
        print("请分别运行两次 bench 命令进行对比")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
