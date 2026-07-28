---
title: "Embedding（向量嵌入）"
aliases: [向量嵌入, 嵌入]
tags: [AI, embedding, vector]
related: [rag, vector-database, llm]
---

# Embedding（向量嵌入）

## 定义

Embedding 是将人类的文本、图片、音频等高维数据，转换成一串计算机能理解的**高维数字数组（向量）**的技术。核心 magic 在于"语义相近的，向量距离也近"。

## 要点

- 将文字含义转化为空间位置——"猫"和"狗"的向量距离远小于"猫"和"微波炉"
- Embedding 是 RAG 和语义搜索的技术基础
- 质量好的 Embedding 模型能捕捉语义、句法甚至隐含情感
- 不同模态的数据（文本、图片、音频）可以映射到同一向量空间

## 相关来源

- [[raw/articles/AI基本知识.md]]

## 与其他概念的联系

- [[rag]]：Embedding 是 RAG 管线的第一步——将文档转化为可检索的向量
- [[vector-database]]：向量数据库专门用于存储和检索 Embedding
- [[llm]]：LLM 内部也使用 Embedding 层来处理输入文本
