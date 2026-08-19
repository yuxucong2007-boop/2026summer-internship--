# 测试知识库使用说明

## 文件说明

- `test_knowledge_base.md`：适合人工阅读和检查的知识库原文。
- `test_queries.jsonl`：评估测试集，每行一条问题及其标准相关文档。

## 导入建议

将 `test_knowledge_base.md` 按 `chunk_id` 分成 23 个独立文本块，并写入向量数据库。每条记录建议保存：

```json
{
  "id": "hr_001",
  "text": "知识库正文",
  "metadata": {
    "category": "HR"
  }
}
```

测试时，对每条 `test_queries.jsonl` 中的 `query` 执行检索，保存系统返回的文档 ID：

```json
{
  "query_id": "q001",
  "retrieved_doc_ids": ["hr_001", "fin_004", "hr_003"]
}
```

然后将 `retrieved_doc_ids` 与测试集中的 `relevant_doc_ids` 比较。

## 推荐指标

至少统计：

- `Hit Rate@1`
- `Hit Rate@3`
- `Hit Rate@5`
- `Recall@5`
- `MRR@5`

无答案问题单独统计“误召回率”：知识库中没有答案的问题，系统是否错误地返回了看似相关的文档。

## 评估注意事项

1. 如果实际系统检索的是更细粒度的 chunk，测试集中的标准 ID 也应使用 chunk ID。
2. `relevant_doc_ids` 可以有多个，不能只标记其中一个正确文档。
3. 调整分块、Embedding、Reranker 或 Top-K 时，最好保留一批不参与调参的最终测试问题。
4. 测试集中的标准答案和相关文档最好由业务人员抽查。
5. 检索指标高，不代表最终回答一定正确；还需要单独评估答案准确性和引用是否正确。
