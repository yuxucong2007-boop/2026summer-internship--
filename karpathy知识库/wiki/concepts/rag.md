---
title: "RAG（检索增强生成）"
aliases: [检索增强生成, Retrieval Augmented Generation]
tags: [AI, rag, retrieval]
related: [llm, embedding, vector-database, ai-agent]
---

# RAG（检索增强生成）

## 定义

RAG（Retrieval Augmented Generation）是一种将 LLM 的回答建立在**特定、外部或私有数据集**之上的技术范式，通过检索相关事实来增强生成内容的准确性和时效性。

## 要点

- **解决的问题**：LLM 的两个固有缺陷——幻觉（捏造事实）和知识过时
- **核心流程**：检索（Retrieve）→ 增强（Augment）→ 生成（Generate）
  - **检索**：在向量数据库中搜索与用户查询相关的事实
  - **增强**：将检索到的文档作为上下文附加到 LLM 的提示中
  - **生成**：指示 LLM 严格基于检索到的上下文编写响应
- **主要优势**：防止幻觉，可实时访问私有数据，无需重新训练模型
- **与 MCP 的分工**：RAG 解决"知识从哪里来"，MCP 解决"动作往哪里去"

## 相关来源

- [[raw/articles/AI基本知识.md]]

## 与其他概念的联系

- [[llm]]：RAG 为 LLM 提供外部知识支撑
- [[embedding]]：RAG 依赖 Embedding 将文本转化为可检索的向量
- [[vector-database]]：RAG 依赖向量数据库进行高效语义检索
- [[ai-agent]]：Agent 在需要事实知识时使用 RAG
