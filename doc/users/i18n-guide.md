# 🌐 多语言支持 (i18n)

**说明**: UnicodeArt 支持多语言消息显示，包括错误提示、警告信息和 CLI 帮助文本。

---

## 🚀 快速开始

### 命令行使用

```bash
# 使用中文（默认）
python unicodeart.py -t "Hello" --font "SimSun.ttc" --height 15

# 使用英文
python unicodeart.py -t "Hello" --font "SimSun.ttc" --height 15 --lang en-US
```

---

## 📁 文件结构

```
src/unicodeart/i18n/
├── __init__.py          # 包初始化
├── loader.py            # 语言加载器
├── zh-CN.json           # 中文语言文件
└── en-US.json           # 英文语言文件
```

---

## 🔧 API 使用

### 在代码中使用多语言

```python
from src.unicodeart.i18n import _, t, set_language

# 方式 1: 使用 _() 函数（推荐）
print(_('error.file_not_found', path='test.png'))
# 输出: 图像文件不存在: test.png

# 方式 2: 使用 t() 函数（别名）
print(t('error.file_not_found', path='test.png'))

# 方式 3: 切换语言后使用
set_language('en-US')
print(_('error.file_not_found', path='test.png'))
# 输出: Image file not found: test.png
```

### 支持的键名

#### 错误消息 (`error.*`)
- `file_not_found` - 文件不存在
- `cannot_read_image` - 无法读取图像
- `unsupported_format` - 不支持的格式
- `font_load_failed` - 字体加载失败
- `invalid_parameter` - 无效的参数
- `missing_required_param` - 缺少必需参数
- `conflicting_params` - 参数冲突

#### 警告消息 (`warning.*`)
- `deprecated_feature` - 功能已弃用
- `performance_slow` - 性能较慢
- `wide_char_fallback` - 宽字符回退

#### 信息消息 (`info.*`)
- `processing_start` - 开始处理
- `processing_complete` - 处理完成
- `saving_output` - 保存输出
- `benchmark_start` - 开始基准测试
- `benchmark_complete` - 基准测试完成

#### 成功消息 (`success.*`)
- `file_saved` - 文件保存成功
- `test_passed` - 测试通过
- `installation_success` - 安装成功

#### CLI 帮助文本 (`cli.*`)
- `help_description` - 帮助描述
- `config_help` - 配置帮助
- ... (所有 CLI 参数的帮助文本)

#### 基准测试 (`benchmark.*`)
- `stage_image_load` - 图像加载阶段
- `stage_sampling` - 采样阶段
- `stage_char_prep` - 字符准备阶段
- `stage_matching` - 匹配阶段
- `stage_output` - 输出生成阶段
- `total_time` - 总耗时
- `peak_memory` - 内存峰值
- `output_size` - 输出大小

---

## 🎯 添加新语言

### 步骤 1: 创建语言文件

在 `src/unicodeart/i18n/` 目录下创建新的 JSON 文件，如 `ja-JP.json`：

```json
{
  "meta": {
    "language": "ja-JP",
    "version": "1.0.0",
    "last_updated": "2026-06-09"
  },
  
  "error": {
    "file_not_found": "画像ファイルが見つかりません: {path}",
    ...
  },
  
  ...
}
```

### 步骤 2: 翻译所有键值

参考 [zh-CN.json](src/unicodeart/i18n/zh-CN.json) 或 [en-US.json](src/unicodeart/i18n/en-US.json) 的结构，翻译所有消息。

### 步骤 3: 测试新语言

```bash
python unicodeart.py -t "Test" --font "SimSun.ttc" --height 10 --lang ja-JP
```

---

##  最佳实践

### 1. 使用占位符

在消息中使用 `{param_name}` 格式的占位符，便于动态插入变量：

```python
# ✅ 正确
_('error.file_not_found', path='test.png')

# ❌ 错误（硬编码路径）
_('error.file_not_found_test.png')
```

### 2. 保持键名一致

所有语言文件必须使用相同的键名结构：

```json
// zh-CN.json
{
  "error": {
    "file_not_found": "..."
  }
}

// en-US.json
{
  "error": {
    "file_not_found": "..."  // 键名必须相同
  }
}
```

### 3. 提供默认回退

如果请求的语言不存在，系统会自动回退到默认语言（zh-CN）：

```python
# 如果 fr-FR.json 不存在，会自动使用 zh-CN.json
set_language('fr-FR')  # 回退到 zh-CN
```

---

## 🔍 调试

### 查看当前语言

```python
from src.unicodeart.i18n import get_i18n

i18n = get_i18n()
print(f"Current language: {i18n.get_current_language()}")
```

### 查看支持的语言列表

```python
from src.unicodeart.i18n import get_i18n

i18n = get_i18n()
print(f"Supported languages: {i18n.get_supported_languages()}")
# 输出: ['en-US', 'zh-CN']
```

---

## 📌 注意事项

1. **JSON 格式**: 语言文件必须是有效的 JSON 格式
2. **UTF-8 编码**: 所有语言文件必须使用 UTF-8 编码
3. **键名规范**: 使用点号分隔嵌套键（如 `error.file_not_found`）
4. **占位符语法**: 使用 Python 的 `.format()` 语法（如 `{path}`）

---

*最后更新: 2026-06-09*
