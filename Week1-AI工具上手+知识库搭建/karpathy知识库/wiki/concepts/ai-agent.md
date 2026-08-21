---
title: "AI Agent（智能体）"
aliases: [智能体, AI Agent]
tags: [AI, agent, llm]
related: [llm, prompt-engineering, rag, mcp, harness-engineering]
---

# AI Agent（智能体）

## 定义

AI Agent 是一个由 LLM 驱动的**自主系统**，能够**规划、使用工具并采取行动**来实现具体的、多步骤的目标，而不仅仅是回答单个文本提示。

## 要点

- **Agent ≠ LLM**：LLM 只回复文本，Agent 以循环方式运作（感知 → 规划 → 执行 → 反思）
- **感知**：读取用户输入和当前状态
- **规划**：将目标分解为可执行的步骤
- **执行**：使用外部工具（浏览网页、运行代码、调用 API）
- **反思**：评估结果，必要时调整策略
- **典型场景**：自动预订行程、代码开发、数据分析等需要多步骤协作的任务

## 相关来源

- [[Week1-AI工具上手+知识库搭建/karpathy知识库/raw/articles/AI基本知识]]

## 与其他概念的联系

- [[llm]]：Agent 的核心推理引擎
- [[prompt-engineering]]：Agent 的指令由 prompt 驱动
- [[rag]]：Agent 通过 RAG 获取外部事实知识
- [[mcp]]：Agent 通过 MCP 调用外部工具
- [[harness-engineering]]：Agent 的安全和可靠性由 Harness 保障
