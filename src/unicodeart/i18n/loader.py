"""
多语言支持模块 (i18n)

提供基于 JSON 语言文件的多语言消息管理功能。
支持语言切换、键值查找和默认语言回退。
"""

import json
import os
from typing import Dict, Any, Optional


class I18nLoader:
    """多语言加载器
    
    负责加载和管理多语言消息文件。
    
    Attributes:
        current_lang: 当前使用的语言代码 (如 'zh-CN', 'en-US')
        messages: 当前语言的消息字典
        default_lang: 默认语言代码
        lang_dir: 语言文件目录路径
    """
    
    def __init__(self, default_lang: str = 'zh-CN'):
        """初始化多语言加载器
        
        Args:
            default_lang: 默认语言代码，默认为 'zh-CN'
        """
        self.default_lang = default_lang
        self.current_lang = default_lang
        self.messages: Dict[str, Any] = {}
        
        # 确定语言文件目录路径（loader.py 所在目录即为 i18n 目录）
        self.lang_dir = os.path.dirname(__file__)
        
        # 加载默认语言
        self._load_language(default_lang)
    
    def _load_language(self, lang_code: str) -> bool:
        """加载指定语言的配置文件
        
        Args:
            lang_code: 语言代码 (如 'zh-CN', 'en-US')
            
        Returns:
            bool: 是否成功加载
            
        Raises:
            FileNotFoundError: 语言文件不存在
            json.JSONDecodeError: JSON 格式错误
        """
        lang_file = os.path.join(self.lang_dir, f'{lang_code}.json')
        
        if not os.path.exists(lang_file):
            # 如果请求的语言不存在，尝试回退到默认语言
            if lang_code != self.default_lang:
                return self._load_language(self.default_lang)
            raise FileNotFoundError(f"Language file not found: {lang_file}")
        
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)
                self.current_lang = lang_code
                return True
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in language file {lang_file}: {e.msg}",
                e.doc, e.pos
            )
    
    def set_language(self, lang_code: str) -> bool:
        """设置当前语言
        
        Args:
            lang_code: 语言代码 (如 'zh-CN', 'en-US')
            
        Returns:
            bool: 是否成功切换语言
        """
        try:
            return self._load_language(lang_code)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def get(self, key: str, **kwargs) -> str:
        """获取翻译消息
        
        Args:
            key: 消息键，支持嵌套键用点号分隔 (如 'error.file_not_found')
            **kwargs: 用于格式化消息的参数
            
        Returns:
            str: 翻译后的消息字符串
            
        Example:
            >>> i18n.get('error.file_not_found', path='test.png')
            '图像文件不存在: test.png'
        """
        # 解析嵌套键
        keys = key.split('.')
        value = self.messages
        
        try:
            for k in keys:
                value = value[k]
        except KeyError:
            # 如果键不存在，返回键本身作为后备
            return key
        
        # 如果有参数，进行格式化
        if kwargs and isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                # 如果格式化失败，返回原始字符串
                return value
        
        return value
    
    def t(self, key: str, **kwargs) -> str:
        """get() 方法的别名，提供更简洁的调用方式
        
        Args:
            key: 消息键
            **kwargs: 格式化参数
            
        Returns:
            str: 翻译后的消息
        """
        return self.get(key, **kwargs)
    
    def get_current_language(self) -> str:
        """获取当前语言代码
        
        Returns:
            str: 当前语言代码
        """
        return self.current_lang
    
    def get_supported_languages(self) -> list:
        """获取支持的语言列表
        
        Returns:
            list: 支持的语言代码列表
        """
        languages = []
        if os.path.exists(self.lang_dir):
            for filename in os.listdir(self.lang_dir):
                if filename.endswith('.json'):
                    lang_code = filename[:-5]  # 移除 .json 后缀
                    languages.append(lang_code)
        return sorted(languages)


# 全局单例实例
_i18n_instance: Optional[I18nLoader] = None


def get_i18n() -> I18nLoader:
    """获取全局多语言加载器实例
    
    Returns:
        I18nLoader: 多语言加载器实例
    """
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18nLoader()
    return _i18n_instance


def set_language(lang_code: str) -> bool:
    """设置全局语言
    
    Args:
        lang_code: 语言代码
        
    Returns:
        bool: 是否成功切换
    """
    return get_i18n().set_language(lang_code)


def _(key: str, **kwargs) -> str:
    """便捷函数：获取翻译消息
    
    Args:
        key: 消息键
        **kwargs: 格式化参数
        
    Returns:
        str: 翻译后的消息
        
    Example:
        >>> from src.unicodeart.i18n.loader import _
        >>> print(_('error.file_not_found', path='test.png'))
        图像文件不存在: test.png
    """
    return get_i18n().get(key, **kwargs)


def t(key: str, **kwargs) -> str:
    """_() 函数的别名"""
    return _(key, **kwargs)
