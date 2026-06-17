#  文档翻译工作流

**说明**: 本文档指导如何为 UnicodeArt 项目创建和维护多语言文档。

---

## 🎯 翻译范围

### **已完成翻译**
- ✅ [README.md](../README.md) → [README_EN.md](../README_EN.md)
- ✅ [i18n-guide.md](users/i18n-guide.md) - 本身就是多语言文档

### **待翻译的核心文档**

#### **用户文档** (P0 - 高优先级)
- [ ] `doc/users/installation.md` → `installation.en.md`
- [ ] `doc/users/quick-start.md` → `quick-start.en.md`
- [ ] `doc/users/features.md` → `features.en.md`
- [ ] `doc/users/faq.md` → `faq.en.md`

#### **开发者文档** (P1 - 中优先级)
- [ ] `doc/devs/architecture.md` → `architecture.en.md`
- [ ] `doc/devs/api-reference.md` → `api-reference.en.md`
- [ ] `doc/devs/contributing.md` → `contributing.en.md`

#### **算法文档** (P2 - 低优先级，可选)
- [ ] `doc/algorithms/README.md` → `README.en.md`
- [ ] `doc/algorithms/image-to-art.md` → `image-to-art.en.md`
- [ ] `doc/algorithms/text-to-art.md` → `text-to-art.en.md`
- [ ] `doc/algorithms/character-matching.md` → `character-matching.en.md`
- [ ] `doc/algorithms/wide-character-handling.md` → `wide-character-handling.en.md`
- [ ] `doc/algorithms/performance-notes.md` → `performance-notes.en.md`

---

## 🔧 翻译工具推荐

### **AI 辅助翻译（推荐）**
1. **DeepL Translator**: https://www.deepl.com/translator
   - 优势: 技术文档翻译质量高
   - 支持: 中文 ↔ 英文
   
2. **Google Translate**: https://translate.google.com/
   - 优势: 免费，支持多种语言
   - 注意: 需要人工校对技术术语

3. **Claude/GPT**: 
   - 优势: 可以保持 Markdown 格式
   - 提示词示例: "请将以下 Markdown 文档从中文翻译成英文，保持所有代码块、链接和格式不变"

### **人工校对要点**
1. **技术术语**: 确保术语一致性（如 "ASCII art", "wide character", "sampling"）
2. **代码示例**: 保持代码不变，仅翻译注释
3. **链接**: 检查所有内部链接是否正确
4. **格式**: 确保 Markdown 格式完整保留

---

## 📝 翻译步骤

### **步骤 1: 复制原文档**
```bash
cp doc/users/installation.md doc/users/installation.en.md
```

### **步骤 2: 翻译内容**
使用 AI 工具或手动翻译，注意：
- 保留所有代码块（```bash, ```python 等）
- 保留所有链接（[文本](链接)）
- 保留所有图片引用
- 仅翻译纯文本内容

### **步骤 3: 添加语言切换链接**
在文档顶部添加：

```markdown
#  安装指南 / Installation Guide

> 🌐 Language / 语言: [🇨🇳 中文](installation.md) | [🇺🇸 English](installation.en.md)

---

## 安装步骤 / Installation Steps
...
```

### **步骤 4: 更新索引文件**
在 `doc/users/README.md` 中添加英文版链接：

```markdown
- [📦 安装指南](installation.md) ([English](installation.en.md))
```

### **步骤 5: 测试链接**
- 检查所有内部链接是否有效
- 检查语言切换链接是否正确
- 验证代码示例是否可运行

---

## 🎨 命名规范

### **文件命名**
- 中文版: `filename.md`
- 英文版: `filename.en.md`

**示例**:
- `installation.md` / `installation.en.md`
- `quick-start.md` / `quick-start.en.md`

### **目录结构**
保持与中文版相同的目录结构：

```
doc/
├── users/
│   ├── installation.md
│   ├── installation.en.md
│   ├── quick-start.md
│   ├── quick-start.en.md
│   └── ...
├── devs/
│   ├── architecture.md
│   ├── architecture.en.md
│   └── ...
└── algorithms/
    ├── README.md
    ├── README.en.md
    └── ...
```

---

## ✅ 质量检查清单

### **翻译前**
- [ ] 确认中文文档是最新版本
- [ ] 备份原文档
- [ ] 准备翻译工具

### **翻译中**
- [ ] 保留所有代码块不变
- [ ] 保留所有链接不变
- [ ] 保留所有图片引用不变
- [ ] 仅翻译纯文本内容
- [ ] 保持 Markdown 格式完整

### **翻译后**
- [ ] 校对技术术语
- [ ] 检查所有链接有效性
- [ ] 测试代码示例
- [ ] 添加语言切换链接
- [ ] 更新索引文件
- [ ] 提交 PR 进行审查

---

## 🤖 AI 翻译提示词模板

### **通用提示词**
```
请将以下 Markdown 文档从中文翻译成英文。

要求：
1. 保持所有代码块（```bash, ```python, ```json 等）完全不变
2. 保持所有链接（[文本](URL)）完全不变
3. 保持所有图片引用（![alt](url)）完全不变
4. 保持所有表格格式不变
5. 仅翻译纯文本内容
6. 技术术语使用标准英文表达
7. 保持 Markdown 标题层级（#, ##, ### 等）不变

以下是需要翻译的内容：
[粘贴 Markdown 内容]
```

### **代码注释翻译**
```
请翻译以下 Python 代码中的中文注释为英文，保持代码本身不变：

[粘贴代码]
```

---

## 📌 注意事项

1. **同步更新**: 当中文文档更新时，需要同步更新英文版本
2. **术语一致**: 建立术语表，确保翻译一致性
3. **版本控制**: 使用 Git 跟踪翻译进度
4. **审查流程**: 翻译完成后需要人工审查
5. **自动化**: 未来可以考虑使用 GitHub Actions 自动检测未同步的文档

---

## 🚀 快速开始

要开始翻译工作，请：

1. 选择要翻译的文档（建议从用户文档开始）
2. 复制文件并添加 `.en.md` 后缀
3. 使用 AI 工具进行初翻
4. 人工校对技术术语
5. 添加语言切换链接
6. 更新索引文件
7. 提交 PR

---

*最后更新: 2026-06-09*  
*维护者: UnicodeArt Team*
