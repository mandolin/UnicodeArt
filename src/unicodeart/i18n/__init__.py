"""
多语言支持包 (i18n)

提供基于 JSON 语言文件的多语言消息管理功能。
"""

from .loader import (
    I18nLoader,
    get_i18n,
    set_language,
    _,
    t,
)

__all__ = [
    'I18nLoader',
    'get_i18n',
    'set_language',
    '_',
    't',
]
