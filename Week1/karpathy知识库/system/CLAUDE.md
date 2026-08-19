# CLAUDE.md — LLM Wiki Schema

## 三层架构

```
vault/
├── raw/               # 原始资料（只读，LLM 永不修改）
│   ├── articles/      # 文章/网页剪藏
│   ├── books/         # 书籍章节
│   └── assets/        # 图片/附件
├── wiki/              # LLM 生成的 Wiki（LLM 读写）
│   ├── concepts/      # 概念页面
│   ├── entities/      # 实体页面（人物、组织、项目等）
│   ├── summaries/     # 单篇资料摘要
│   ├── synthesis/     # 综合对比/分析
│   ├── queries/       # 问答产出（可归档的优质答案）
│   ├── index.md       # 内容目录（每次摄入更新）
│   └── log.md         # 操作日志（追加写入）
└── system/            # 配置与模板（LLM 读写）
    ├── CLAUDE.md      # 本文件 — 工作流配置
    └── templates/     # 页面模板
```

## 工作流

### 1. 摄入（Ingest）

当你将新资料放入 `raw/` 目录并告诉我处理后：

1. 读取原始资料内容
2. 与你讨论关键要点，确定重点
3. 在 `wiki/summaries/` 创建摘要页面
4. 更新 `wiki/index.md`
5. 更新或创建 `wiki/concepts/` 和 `wiki/entities/` 中的相关页面
6. 在 `wiki/log.md` 追加记录

### 2. 查询（Query）

当你提问时：

1. 读取 `wiki/index.md` 定位相关页面
2. 深入阅读相关页面
3. 综合回答，引用来源
4. 如果有长期价值的回答，归档到 `wiki/queries/`

### 3. 整理（Lint）

当你要求健康检查时：

1. 检查页面间的矛盾
2. 检查过时的观点
3. 检查孤儿页面（无入链）
4. 检查缺失的交叉引用
5. 建议新的探索方向

## Wiki 页面规范

### 摘要页面（summaries/）

```
---
title: ""
source: "raw/articles/..."
date: 2026-07-27
tags: []
---

# [标题]

## 核心观点

## 关键细节

## 与现有知识的关系

## 个人思考
```

### 概念页面（concepts/）

```
---
title: ""
aliases: []
tags: []
related: []
---

# [概念名称]

## 定义

## 要点

## 相关来源

## 与其他概念的联系
```

### 实体页面（entities/）

```
---
title: ""
type: person|organization|project|etc.
tags: []
related: []
---

# [实体名称]

## 概述

## 相关来源

## 关联
```

## 约定

- 所有文件使用 Markdown 格式
- 页面使用 YAML frontmatter（便于 Dataview 查询）
- Wiki 链接使用 `[[wiki/concepts/xxx]]` 格式
- 引用来源使用 `[[raw/articles/xxx]]` 格式
- 英文名词保留原文，解释使用中文
