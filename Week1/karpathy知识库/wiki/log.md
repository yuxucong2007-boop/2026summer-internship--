---
updated: 2026-07-28
---

# Wiki 操作日志

> 按时间顺序记录所有操作：资料摄入、查询、整理。
> 每条记录以 `## [日期] 操作类型 | 标题` 格式开头。

## [2026-07-27] init | 初始化 Wiki 结构

- 创建三层架构：`raw/` → `wiki/` → `system/`
- 创建 `wiki/index.md` 和 `wiki/log.md`
- 创建 `system/CLAUDE.md` 工作流配置

## [2026-07-27] cleanup | 删除已移除文章的相关条目

- 原始文章 `Koszul Binomial Edge Ideals` 和 `企业AI工作空间与专业智能体平台产品规划书` 已被删除
- 移除所有相关的概念页、实体页、摘要页
- 更新 index 和 log 以反映当前状态

## [2026-07-28] ingest | AI基本知识 —— 大规模摄入

- 原始资料：`raw/articles/AI基本知识.md`（AI 大模型生态 10 大核心概念）
- 新建摘要：[[Week1/karpathy知识库/wiki/summaries/ai基本知识]]
- 新建概念页（10 个）：
  - [[llm]]
  - [[prompt-engineering]]
  - [[ai-agent]]
  - [[rag]]
  - [[mcp]]
  - [[harness-engineering]]
  - [[embedding]]
  - [[vector-database]]
  - [[fine-tuning]]
  - [[幻觉-hallucination]]
- 新建综合页：[[ai-ecology]]（AI 技术栈四层架构全景）
- 更新 `wiki/index.md` 反映所有新页面
