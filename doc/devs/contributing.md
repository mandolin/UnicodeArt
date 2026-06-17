# 🤝 贡献指南

欢迎为 UnicodeArt 项目做出贡献！

---

## 📋 如何贡献

### 1. 报告 Bug

**提交 Issue 时请包含**:
- 🖥️ 操作系统和 Python 版本
- 📝 完整的命令和参数
- ❌ 错误信息（完整堆栈跟踪）
- 📸 截图或示例文件（如有）
- ✅ 预期行为和实际行为

**示例**:
```markdown
**环境**: Windows 11, Python 3.10

**命令**: 
```bash
python unicodeart.py -i test.jpg --height 30
```

**错误**:
```
ValueError: cannot reshape array...
```

**预期**: 正常生成字符画
**实际**: 抛出异常
```

---

### 2. 提出新功能

**提交 Feature Request 时请说明**:
- 💡 功能描述
- 🎯 使用场景
- 🔗 相关 Issue（如有）
- 📊 优先级评估

---

### 3. 提交代码 (Pull Request)

#### 步骤 1: Fork 项目

点击 GitHub 右上角的 "Fork" 按钮

---

#### 步骤 2: 克隆仓库

```bash
git clone https://github.com/your-username/UnicodeArt.git
cd UnicodeArt
```

---

#### 步骤 3: 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b bugfix/issue-number
```

**分支命名**:
- `feature/*`: 新功能
- `bugfix/*`: Bug 修复
- `docs/*`: 文档更新

---

#### 步骤 4: 开发

**遵循代码规范**: [📝 代码规范](coding-standards.md)

**关键检查**:
- [ ] 添加类型提示
- [ ] 编写 Docstring
- [ ] 函数拆分合理（<30 行）
- [ ] 避免硬编码（使用 constants.py）

---

#### 步骤 5: 测试

```bash
# 运行所有测试
pytest

# 生成 HTML 报告
pytest --html=tests/report.html

# 确保所有测试通过
```

**新增功能的测试**:
- [ ] 添加单元测试
- [ ] 测试边界情况
- [ ] 验证性能无明显退化

---

#### 步骤 6: 提交

```bash
git add .
git commit -m "feat(module): add new feature

- Description of changes
- Related issues

Closes #123"
```

**提交信息规范**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

#### 步骤 7: 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

在 GitHub 上创建 Pull Request：
- 📝 清晰描述变更内容
- 🔗 关联相关 Issue
- ✅ 确认 CI 测试通过
- 📸 添加截图（如有 UI 变更）

---

## 🎯 贡献领域

### 高优先级

- 🐛 Bug 修复
- 📚 文档完善
- 🧪 测试覆盖率提升
- ⚡ 性能优化

### 中优先级

- ✨ 新功能实现
- 🔄 代码重构
- 🎨 用户体验改进

### 低优先级

- 🌈 实验性功能
- 🎭 输出格式扩展

---

## 📊 代码审查标准

PR 合并前需满足：

### 必需条件

- [ ] 所有测试通过
- [ ] 代码符合规范（Black 格式化）
- [ ] 文档已更新
- [ ] 无明显的性能退化
- [ ] 至少 1 个 maintainer 批准

### 加分项

- [ ] 添加了新测试
- [ ] 性能有提升
- [ ] 文档详细清晰
- [ ] 向后兼容

---

## 💬 沟通渠道

- **GitHub Issues**: Bug 报告和功能请求
- **GitHub Discussions**: 技术讨论和问题咨询
- **Email**: 敏感问题或安全漏洞报告

---

## 🎓 学习资源

### 新手入门

1. 阅读 [快速入门](../users/quick-start.md)
2. 了解 [架构设计](architecture.md)
3. 查看 [API 参考](api-reference.md)
4. 运行现有测试理解预期行为

---

### 开发准备

```bash
# 安装开发依赖
pip install -r requirements.txt
pip install pytest black

# 运行测试
pytest -v

# 格式化代码
black src/ tests/
```

---

## 🏆 贡献者权益

- ✅ 名字出现在 README 贡献者列表
- ✅ 参与项目决策讨论
- ✅ 获得社区认可

---

## ❓ 常见问题

### Q: 我的 PR 多久会被审查？

A: 通常 1-3 个工作日内会有响应

---

### Q: 如何知道该做什么？

A: 查看 [Issues](https://github.com/your-username/UnicodeArt/issues) 中标记为 `good first issue` 或 `help wanted` 的任务

---

### Q: 我的代码被拒绝了怎么办？

A: 
1. 仔细阅读审查意见
2. 按要求修改后重新提交
3. 如有疑问，在 PR 评论区讨论

---

## 🙏 感谢

感谢所有为 UnicodeArt 做出贡献的开发者！

---

*最后更新: 2026-06-09*
