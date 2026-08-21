---
title: "Harness Engineering（线束工程）"
aliases: [线束工程, AI安全框架, 代理线束]
tags: [AI, harness, safety, engineering]
related: [ai-agent, llm, mcp]
---

# Harness Engineering（线束工程）

## 定义

Harness Engineering 是围绕 LLM 或 AI Agent 构建的**周边基础设施、控制框架和执行环境**，用于保持其可靠性、安全性和高效性。可理解为"安全笼和转向装置"。

## 要点

- **解决的问题**：生产环境中的原始 LLM 可能难以预测，需要外围系统来管控
- **核心组件**：
  - **内存管理**：存储短期和长期对话历史
  - **防护措施与过滤**：检查输入和输出是否存在安全风险
  - **执行沙箱**：在隔离的安全环境中运行 Agent 生成的代码
  - **评估与回退**：检测 Agent 死循环或步骤失败，重新路由或通知人工
- **定位**：AI 系统的"操作系统层"——让 Agent 可靠运行的保障

## 相关来源

- [[Week1-AI工具上手+知识库搭建/karpathy知识库/raw/articles/AI基本知识]]

## 与其他概念的联系

- [[ai-agent]]：Harness 是 Agent 生产化部署的必备基础设施
- [[llm]]：Harness 管理 LLM 的输入输出和行为
- [[mcp]]：MCP 工具调用在 Harness 的沙箱保护下执行
