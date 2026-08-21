---
title: "LLM（大语言模型）"
aliases: [大语言模型, Large Language Model]
tags: [AI, LLM, foundation]
related: [prompt-engineering, ai-agent, rag, 幻觉-hallucination]
---

# LLM（大语言模型）

## 定义

大型语言模型（Large Language Model）是一种基于海量文本数据训练的深度学习模型，核心能力是**预测序列中的下一个词**。它是现代 AI 的"大脑"或基础引擎。

## 要点

- **本质是概率预测机**，而非知识数据库——它计算"在当前上下文后最可能出现哪个词"
- **追求流畅度而非绝对真理**：训练目标是生成符合人类表达习惯的内容
- **有损压缩**：将数 TB 文本知识压缩进模型参数中，导致无法做到无损精确提取
- **核心能力**：自然语言理解与生成、复杂推理、代码编写、非结构化文本处理

## 相关来源

- [[Week1-AI工具上手+知识库搭建/karpathy知识库/raw/articles/AI基本知识]]

## 与其他概念的联系

- [[prompt-engineering]]：通过提示词引导 LLM 的输出
- [[ai-agent]]：LLM 是 Agent 的推理引擎，Agent = LLM + 规划 + 工具
- [[rag]]：RAG 为 LLM 提供外部知识，弥补其知识截止和幻觉问题
- [[幻觉-hallucination]]：LLM 的底层架构决定了幻觉是内在特性而非 Bug
