---
title: "Fine-tuning（微调）"
aliases: [微调, 模型微调]
tags: [AI, fine-tuning, training, llm]
related: [llm, prompt-engineering]
---

# Fine-tuning（微调）

## 定义

Fine-tuning（微调）是在已有的通用大模型（如 Llama 3、GPT-4）基础上，使用特定的业务数据集**再次进行训练**，改变模型内部权重的过程。可理解为模型的"二次进修"。

## 要点

- **与 RAG 的区别**：RAG 不改变模型本身，微调改变模型的内部知识
- **适用场景**：
  - 掌握特定的专业领域知识（医学、法律、金融）
  - 固定独特的输出风格或格式
  - 提升在特定任务上的执行表现
- **成本**：需要标注数据、计算资源和 ML 工程经验
- **选择路径**：能用 prompt 解决的用 prompt，能用 RAG 的用 RAG，最后才考虑微调

## 相关来源

- [[Week1/karpathy知识库/raw/articles/AI基本知识]]

## 与其他概念的联系

- [[llm]]：微调是修改 LLM 权重的方法
- [[prompt-engineering]]：微调和 prompt 是两种互补的模型定制手段
