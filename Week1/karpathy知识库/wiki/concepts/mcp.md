---
title: "MCP 协议（模型上下文协议）"
aliases: [模型上下文协议, Model Context Protocol]
tags: [AI, mcp, protocol, tool-use]
related: [ai-agent, llm, harness-engineering]
---

# MCP 协议（模型上下文协议）

## 定义

MCP（Model Context Protocol）是一个**开放标准**，旨在统一 AI 应用程序如何连接到外部工具、数据库和本地文件系统。可理解为"AI 应用的 USB-C"。

## 要点

- **解决的问题**：在 MCP 出现前，每个 AI 工具或代理框架都需要为每项外部服务编写自定义集成代码
- **标准化为客户端-服务器模型**：
  - **MCP 客户端**：AI 应用程序（如 Claude Desktop、IDE 扩展）
  - **MCP 服务器**：轻量级插件，用于暴露工具和数据（如本地 SQLite 数据库、Slack 集成、文件系统）
- **主要优势**：允许任何 AI Agent 立即连接到任何 MCP 支持的数据源或工具，无需逐一定制集成
- **与 RAG 的分工**：RAG 获取"知识"，MCP 执行"动作"

## 相关来源

- [[Week1/karpathy知识库/raw/articles/AI基本知识]]

## 与其他概念的联系

- [[ai-agent]]：Agent 通过 MCP 协议执行实际操作
- [[llm]]：LLM 通过 MCP 扩展能力边界
- [[harness-engineering]]：MCP 调用在 Harness 的安全沙箱中执行
