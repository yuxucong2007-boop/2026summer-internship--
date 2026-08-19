---
title: "向量数据库（Vector Database）"
aliases: [向量数据库, Vector DB, 矢量数据库]
tags: [AI, database, vector, retrieval]
related: [embedding, rag]
---

# 向量数据库（Vector Database）

## 定义

向量数据库是专门用来**存储和高效检索 Embedding（向量）数据**的特殊数据库（如 Milvus, Pinecone, Chroma 等），擅长做**语义相似度搜索**（KNN/ANN 检索）。

## 要点

- **与关系型数据库的区别**：MySQL 擅长"完全匹配"，向量数据库擅长"语义近似匹配"
- **核心能力**：当你拥有数百万份文档时，向量数据库能让 AI 快速找到最相关的内容
- **典型产品**：Milvus（开源）、Pinecone（云服务）、Chroma（轻量嵌入式）、Weaviate、Qdrant
- **工作原理**：使用近似最近邻（ANN）算法在大规模向量空间中高效搜索

## 相关来源

- [[Week1/karpathy知识库/raw/articles/AI基本知识]]

## 与其他概念的联系

- [[embedding]]：向量数据库存储的内容就是 Embedding 生成的向量
- [[rag]]：向量数据库是 RAG 架构中"检索"步骤的核心基础设施
