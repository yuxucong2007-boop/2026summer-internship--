---
cssclasses:
  - wide-page
---

# Open WebUI 与 WorkBuddy 功能对比矩阵

> 对标对象：Open WebUI（自托管、多用户 AI 交互与模型管理平台）与腾讯 WorkBuddy（桌面职场 AI 智能体工作台，企业能力含 WorkBuddy Managed Agents，简称 WMA）。  

## 对比矩阵

| 功能模块   | 功能点           | Open WebUI                                    | WorkBuddy                              | 结论                                         |
| ------ | ------------- | --------------------------------------------- | -------------------------------------- | ------------------------------------------ |
| 聊天对话   | 基础对话          | 以 Web 聊天为核心，统一接入多模型，支持附件、联网搜索、工具、语音等          | 以“任务”为核心，可拆解步骤、操作本地文件并交付成果，支持任务并行      | **聊天/跨模型入口：OW 优；办公任务执行：WB 优**              |
| 聊天对话   | 多模型切换/比较      | 支持同题多模型并排比较                                   | 支持手动切换和 Auto 自动选模                      | **同题对比：OW 优；自动选模：WB 方便**                   |
| 聊天对话   | 流式输出          | 明确支持流式响应，API 可二次集成                            | 可见任务进度，WMA 支持长任务；底层流协议未公开              | **协议透明：OW 优；长任务状态：WB 优**                   |
| 对话管理   | 历史记录、检索与整理    | 支持搜索、文件夹、标签、置顶、分叉、分享                          | 任务有独立工作空间，支持分享、归档、恢复，产物可单独分享           | **对话搜索分类：OW 优；任务+交付物一体化：WB 优**             |
| 模型管理   | 模型配置与治理       | 多上游连接、模型预设绑定提示词/知识库/工具/权限，支持导入导出              | 图形化管理模型，Key 存在本机 models.json           | **团队级治理：OW 优；本地轻量配置：WB 优**                 |
| 模型管理   | 模型 API 对接     | 原生接 Ollama、OpenAI、Anthropic、OpenAI 兼容服务，作统一网关 | 支持主流提供商、本地 Ollama、自定义 API              | **统一网关/访问控制：OW 优；桌面 BYOK、Key 不上云：WB 优**    |
| 知识库    | RAG 知识库       | 原生知识库，支持向量/混合检索、重排、可配向量库                      | 可连接 ima、腾讯文档等资料源，WMA 支持企业知识库 RAG       | **自托管、参数可控：OW 强；腾讯生态闭环：WB 顺手**             |
| 知识库    | 文档上传与处理       | 支持多格式上传，可配置多种解析引擎                             | 可读授权本地目录、批量处理并交付 Office 成果             | **解析可配置性：OW 优；本地批处理交付：WB 优**               |
| Prompt | Prompt 模板     | 独立模板库，支持变量和版本管理                               | “灵感”一键复刻案例，自动组合 Prompt+Skill           | **模板复用治理：OW 优；非技术用户：WB 更合适**               |
| 权限管理   | 用户角色与资源权限     | 原生多用户，细粒度资源访问控制，支持 SSO/LDAP/SCIM              | 企业版有管理员、SSO、Agent 可见范围；本地操作需授权         | **细粒度 RBAC：OW 优；本地操作确认：WB 更有针对性**          |
| 开放能力   | API 接口        | OpenAI/Anthropic 兼容 API，Swagger 文档，成熟公开       | WMA 支持 API Key 接入、独立 Session；无通用聊天端点契约 | **通用 API 网关：OW 明显更成熟；企业执行型集成：WMA 更贴近**     |
| 扩展能力   | 工具调用          | 原生 Python Tools、OpenAPI、MCP，工具可绑定模型           | Skill 封装脚本/工作流，连接器支持 MCP、CLI、OAuth     | **标准化工具注册：OW 优；操控桌面/本地文件：WB 强**            |
| 扩展能力   | 函数（Functions） | 提供 Python 函数扩展，内置编辑器                          | 无独立对象，最接近的是 Skill、MCP 工具               | **轻量函数：OW 概念直接；可安装任务能力：WB Skill 更完整**      |
| 扩展能力   | Pipeline      | 独立插件框架，可做请求前后处理、路由、供应商接入                      | 用 Skills 工作流、定时/事件自动化，非同一技术层           | **平台级中间件：OW 优；业务结果编排：WB 优**                |
| 多用户管理  | 成员、组织与会话隔离    | 原生多用户，支持 SSO/LDAP/SCIM、审计分析                   | 企业版按席位管理，支持 SSO、组织同步；WMA 每用户独立 Session | **低成本自托管多租户：OW 优；腾讯企业身份+云端沙箱：WB 企业版强但依赖高** |
| 部署与数据  | 自托管、本地化与数据边界  | Docker/K8s/pip/裸机部署，数据全由组织控制                  | Windows/macOS 桌面端，企业版 SaaS/专享部署        | **完整自托管、避免绑定：OW 优；开箱即用省运维：WB 优**           |


## 主要资料来源

### Open WebUI

- **[OW-1]** [What You Can Do with Open WebUI](https://docs.openwebui.com/features/)
- **[OW-2]** [Chat Features Overview](https://docs.openwebui.com/features/chat-conversations/chat-features/)
- **[OW-3]** [API Endpoints](https://docs.openwebui.com/reference/api-endpoints)

### WorkBuddy

- **[WB-1]** [产品简介](https://cloud.tencent.com/document/product/1831/134384)
- **[WB-2]** [新建任务栏（本地 AI 工作台）](https://cloud.tencent.com/document/product/1831/134391)
- **[WB-3]** [模型配置](https://cloud.tencent.com/document/product/1831/134445)
- **[WB-4]** [数据管理](https://cloud.tencent.com/document/product/1831/134446)
- **[WB-5]** [ima 知识库](https://cloud.tencent.com/document/product/1831/134397)
- **[WB-6]** [灵感](https://cloud.tencent.com/document/product/1831/134394)
- **[WB-7]** [技能](https://cloud.tencent.com/document/product/1831/134432)
- **[WB-8]** [WorkBuddy Managed Agents 产品介绍](https://cloud.tencent.com/document/product/1831/134407)
- **[WB-9]** [WorkBuddy Managed Agents 快速开始](https://cloud.tencent.com/document/product/1831/134527)
- **[WB-10]** [企业管理员](https://cloud.tencent.com/document/product/1831/134412)
- **[WB-11]** [第三方开发集成](https://cloud.tencent.com/document/product/1831/134415)
- **[WB-12]** [连接器](https://cloud.tencent.com/document/product/1831/134525)

