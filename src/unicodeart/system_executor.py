#!/usr/bin/env python3
"""
系统命令执行工具 - 直接调用系统 PowerShell/CMD
避免使用 VSCode 终端 API,防止进程残留

设计原则:
1. 优先 Python 内部执行 (零终端依赖)
2. 必要时使用 subprocess 直接调用系统 Shell
3. 所有命令必须有 timeout 和 cleanup
4. 捕获 stdout/stderr/return_code
"""
import subprocess
import sys
from typing import Dict, Optional, Union
from pathlib import Path


def run_powershell_command(
    command: str,
    timeout: int = 30,
    cwd: Optional[str] = None,
    capture_output: bool = True
) -> Dict[str, Union[str, int, bool]]:
    """
    直接调用系统 PowerShell 执行命令
    
    Args:
        command: PowerShell 命令字符串
        timeout: 超时秒数 (默认 30s)
        cwd: 工作目录 (可选)
        capture_output: 是否捕获输出 (默认 True)
    
    Returns:
        dict: {
            'stdout': str - 标准输出
            'stderr': str - 标准错误
            'return_code': int - 退出码
            'success': bool - 是否成功
            'command': str - 执行的命令
        }
    
    Example:
        >>> result = run_powershell_command("python test.py")
        >>> if result['success']:
        ...     print(result['stdout'])
    """
    # 构建 PowerShell 命令
    ps_command = f'powershell -NoProfile -Command "{command}"'
    
    try:
        result = subprocess.run(
            ps_command,
            shell=True,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'  # 处理编码问题
        )
        
        return {
            'stdout': result.stdout if capture_output else '',
            'stderr': result.stderr if capture_output else '',
            'return_code': result.returncode,
            'success': result.returncode == 0,
            'command': command
        }
        
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Timeout after {timeout}s',
            'return_code': -1,
            'success': False,
            'command': command
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'return_code': -1,
            'success': False,
            'command': command
        }


def run_cmd_command(
    command: str,
    timeout: int = 30,
    cwd: Optional[str] = None,
    capture_output: bool = True
) -> Dict[str, Union[str, int, bool]]:
    """
    直接调用系统 CMD 执行命令
    
    Args:
        command: CMD 命令字符串
        timeout: 超时秒数 (默认 30s)
        cwd: 工作目录 (可选)
        capture_output: 是否捕获输出 (默认 True)
    
    Returns:
        dict: 同 run_powershell_command
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            encoding='gbk' if sys.platform == 'win32' else 'utf-8',
            errors='replace'
        )
        
        return {
            'stdout': result.stdout if capture_output else '',
            'stderr': result.stderr if capture_output else '',
            'return_code': result.returncode,
            'success': result.returncode == 0,
            'command': command
        }
        
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Timeout after {timeout}s',
            'return_code': -1,
            'success': False,
            'command': command
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'return_code': -1,
            'success': False,
            'command': command
        }


def execute_python_script(
    script_path: str,
    args: list = None,
    timeout: int = 60,
    cwd: Optional[str] = None
) -> Dict[str, Union[str, int, bool]]:
    """
    执行 Python 脚本 (使用 subprocess)
    
    Args:
        script_path: 脚本路径
        args: 参数列表 (可选)
        timeout: 超时秒数 (默认 60s)
        cwd: 工作目录 (可选)
    
    Returns:
        dict: 同 run_powershell_command
    
    Example:
        >>> result = execute_python_script('test.py', ['--height', '30'])
    """
    cmd_parts = ['python', script_path]
    if args:
        cmd_parts.extend(args)
    
    command = ' '.join(cmd_parts)
    
    return run_powershell_command(command, timeout=timeout, cwd=cwd)


def cleanup_temp_files(file_patterns: list):
    """
    清理临时文件
    
    Args:
        file_patterns: 文件路径或 glob 模式列表
    
    Example:
        >>> cleanup_temp_files(['test_*.txt', '*.log', 'temp.json'])
    """
    import glob
    
    cleaned = []
    for pattern in file_patterns:
        # 如果是具体路径
        if '*' not in pattern:
            path = Path(pattern)
            if path.exists():
                path.unlink()
                cleaned.append(pattern)
        # 如果是 glob 模式
        else:
            for file_path in glob.glob(pattern):
                Path(file_path).unlink()
                cleaned.append(file_path)
    
    if cleaned:
        print(f"[INFO] 已清理 {len(cleaned)} 个文件")


if __name__ == '__main__':
    # 自测试
    print("=" * 70)
    print(" 系统命令执行工具 - 自测试")
    print("=" * 70)
    
    # 测试 1: PowerShell 命令
    print("\n[测试 1] PowerShell 命令")
    result = run_powershell_command("Write-Host 'Hello from PowerShell'")
    print(f"  Success: {result['success']}")
    print(f"  Output: {result['stdout'].strip()}")
    
    # 测试 2: Python 脚本
    print("\n[测试 2] Python 脚本")
    result = execute_python_script('-c', ['print("Hello from Python")'])
    print(f"  Success: {result['success']}")
    print(f"  Output: {result['stdout'].strip()}")
    
    # 测试 3: 超时测试
    print("\n[测试 3] 超时测试")
    result = run_powershell_command("Start-Sleep -Seconds 5", timeout=2)
    print(f"  Success: {result['success']}")
    print(f"  Error: {result['stderr']}")
    
    print("\n" + "=" * 70)
    print(" ✅ 自测试完成")
    print("=" * 70)
