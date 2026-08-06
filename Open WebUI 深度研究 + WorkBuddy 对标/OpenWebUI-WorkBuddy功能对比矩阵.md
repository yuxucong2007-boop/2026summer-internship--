---
cssclasses:
  - wide-page
---

# Open WebUI 与 WorkBuddy 功能对比矩阵


> 调研日期：2026-08-06  
> 对标对象：Open WebUI（自托管、多用户 AI 交互与模型管理平台）与腾讯 WorkBuddy（桌面职场 AI 智能体工作台，企业能力含 WorkBuddy Managed Agents，简称 WMA）。  
> 判断口径：以双方截至调研日可访问的官方文档为主；“未见公开文档”不等于产品绝对不支持，只表示不能从公开资料确认。示例图中的 “WorkBuddy 原生 gRPC stream” 未获官方资料支持，因此不作为结论。

## 对比矩阵

| 功能模块   | 功能点           | Open WebUI                                                                                                             | WorkBuddy                                                                                                                                       | 差异分析（含优劣判断）                                                                                                |
| ------ | ------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 聊天对话   | 基础对话          | 以 Web 聊天为核心，可统一使用 Ollama、OpenAI、Anthropic 及 OpenAI 兼容模型；对话内支持附件、联网搜索、代码执行、工具、语音和图片生成。[OW-1]                            | 以“任务”而非纯聊天为核心；提供默认、Ask、Plan 模式，可自主拆解步骤、操作授权目录中的本地文件并交付文件或应用成果，支持多个独立任务并行。[WB-1][WB-2]                                                           | 两者均可自然语言交互，但产品重心不同。**普通聊天、跨模型统一入口：Open WebUI 更优；复杂办公任务执行和本地产物交付：WorkBuddy 更优。**                            |
| 聊天对话   | 多模型切换/比较      | 支持在同一对话中切换模型并保留上下文，也**==支持多个模型并排响应、直接比较结果==**。[OW-1]                                                                   | 提供内置模型、手动切换和 **==Auto 自动选模==**；每个任务选择一个执行模型。公开文档未说明同一轮由多个模型并排作答。[WB-2][WB-3]                                                                    | **横向对比模型效果：Open WebUI 更强；减少用户选模成本：WorkBuddy 的 Auto 更方便。** WorkBuddy 的“多任务并行”不等同于 Open WebUI 的“多模型同题并排比较”。  |
| 聊天对话   | 流式输出          | 聊天界面明确支持回答生成中的持续展示；兼容 API 同时支持流式与非流式请求，适合客户端二次集成。[OW-2][OW-3]                                                          | 客户端可查看执行中任务及进度，WMA 支持长任务和 Session；但公开文档未披露桌面对话或企业 API 的底层流协议，不能确认其使用 gRPC 或 SSE。[WB-2][WB-8][WB-9]                                              | 用户侧都能看到持续进展。**协议透明度和二次开发确定性：Open WebUI 更优；长任务状态管理：WorkBuddy/WMA 更突出。**                                     |
| 对话管理   | 历史记录、检索与整理    | 支持历史搜索、文件夹/项目、标签、置顶、分享和从任意消息分叉对话；模型还可通过原生工具检索历史。[OW-2]                                                                 | 每个任务维护独立工作空间和上下文；支持任务切换、分享、归档、恢复和永久删除，产物文件可单独分享。公开文档未说明全量对话全文检索、标签或文件夹体系。[WB-2][WB-4]                                                           | **大量对话的搜索和分类：Open WebUI 更优；对话、工作目录和交付物一体化管理：WorkBuddy 更优。**                                                |
| 模型管理   | 模型配置与治理       | 可管理多个上游连接和自定义模型；模型预设可绑定系统提示词、知识库、工具、参数及访问控制；支持模型 JSON 导入、导出、批量同步和 API 管理。[OW-1][OW-3]                                  | 图形界面管理内置及自定义模型，支持添加、编辑、删除；API Key 与配置保存在本机 `workbuddy/models.json`，自定义模型可在对话选择器中直接使用。[WB-3]                                                     | **团队级集中治理、配置即代码和权限绑定：Open WebUI 更优；个人设备上的轻量配置及 Key 本地保存：WorkBuddy 更优。**                                    |
| 模型管理   | 模型 API 对接     | 原生连接 Ollama、OpenAI、Anthropic 和 OpenAI 兼容服务；作为自托管中间层统一向用户与应用暴露模型。[OW-1][OW-3]                                           | 支持 OpenAI、Anthropic、Gemini 等提供商、Ollama 本地部署和自定义 API；默认使用标准 `/chat/completions` 路径，也可开启“自定义协议”直接请求指定 URL。[WB-3]                                  | 两者接入范围都较广。**组织共享、统一网关和模型访问控制：Open WebUI 更优；桌面端 BYOK、本地 Ollama、Key 不上传云端：WorkBuddy 更优。**                    |
| 知识库    | RAG 知识库       | 原生创建知识库；支持向量检索、BM25 + 向量混合检索、重排、Agentic Retrieval、整篇注入，并可选 ChromaDB、PGVector 及多种非核心向量库集成。[OW-1]                        | 桌面端连接 ima、腾讯文档、乐享等资料源，可检索/引用个人与共享知识并把产物回存；WMA 可绑定官方及企业自定义知识库，通过 RAG 检索。[WB-5][WB-9]                                                             | **自托管、检索参数可控、向量库和解析链路选择：Open WebUI 更强；腾讯办公生态授权、引用和成果回存闭环：WorkBuddy 更顺手。**                                  |
| 知识库    | 文档上传与处理       | 对话和知识库均可上传文件、图片与代码；支持聚焦检索或整篇上下文两种模式，并可配置 Tika、Docling、OCR 等多种抽取引擎。[OW-1][OW-2]                                         | 可上传文件或直接读取授权本地目录，处理文档、表格、PPT、图片及批量文件任务；ima 知识库文件可加入任务，任务产物可保存回知识库。[WB-1][WB-2][WB-5]                                                            | **文档解析、切块、检索和向量化的可配置性：Open WebUI 更优；直接修改本地文件、批处理并交付 Office 成果：WorkBuddy 更优。**                              |
| Prompt | Prompt 模板     | Workspace Prompts 提供斜杠命令模板、类型化输入变量和版本管理；模型预设还可封装系统提示词、工具、知识和动态变量。[OW-1][OW-2]                                          | “灵感”提供可收藏的一键复刻案例，自动预填 Prompt 并加载关联 Skill/专家；WMA Agent 支持 System Prompt 和 Manifest。公开文档未显示独立、版本化的个人 Prompt 模板库。[WB-6][WB-9]                      | **Prompt 的独立复用、变量化和版本治理：Open WebUI 更优；按成果案例一键组合 Prompt + Skill + 专家：WorkBuddy 更适合非技术用户。**                  |
| 权限管理   | 用户角色与资源权限     | 原生多用户；支持角色、用户组、按模型/知识库/工具等资源控制访问，并可接入 SSO/OIDC/LDAP、SCIM 2.0 和用户 API Key。[OW-1]                                        | 桌面执行有默认权限与完全访问权限；企业版支持企业创建者、超级管理员/管理员、统一身份/SSO、Agent 可见与管理范围。细粒度能力主要位于付费企业体系。[WB-2][WB-10]                                                      | 权限维度不同：前者管理“平台资源访问”，后者还管理“本机动作是否执行”。**细粒度 RBAC 与自托管身份集成：Open WebUI 更优；本地敏感操作确认和企业办公身份衔接：WorkBuddy 更有针对性。** |
| 开放能力   | API 接口        | 提供 Bearer API Key、OpenAI 兼容 `/api/chat/completions`、Anthropic Messages 兼容接口、模型查询及模型导入/导出/同步 API；开发环境可查看 Swagger。[OW-3] | WMA 文档说明可用企业 API Key 把 Agent 接入自有系统，并通过 API 创建独立 Session；另有组织架构同步 REST 规范。公开文档未给出可直接替代 OpenAI Chat Completions 的通用 WorkBuddy 端点契约。[WB-9][WB-11] | **作为通用模型/聊天 API 网关：Open WebUI 明显更成熟、公开程度更高；作为带沙箱、文件和长任务状态的企业 Agent 服务：WMA 更贴近执行型集成。**                      |
| 扩展能力   | 工具调用（Tools）   | 支持原生 Python Tools、OpenAPI Tool Server、MCP（Streamable HTTP）及服务端工具循环；工具可绑定到模型，也可由聊天 API 通过 `tool_ids` 调用。[OW-1][OW-3]    | Skill 可封装脚本和工作流，执行文件、系统命令及第三方 API；连接器支持 MCP + CLI、Skill + CLI、OAuth/API Key，可查询和写入外部系统。[WB-7][WB-12]                                            | **Web 平台内的标准化工具注册、API 调用和访问控制：Open WebUI 更优；直接操控桌面、本地文件及办公服务：WorkBuddy 更强。**                               |
| 扩展能力   | 函数（Functions） | 提供 Python 代码扩展能力，官方功能页将 Tools & Functions 作为可在聊天中运行、带内置编辑器的扩展机制；也可用过滤器和操作扩展交互。[OW-1]                                   | 未把 “Functions” 作为独立一级对象；最接近的是可创建/导入的 Skill、MCP 工具和 Agent 插件，由 Agent 在任务中调用。[WB-7][WB-9]                                                         | **需要轻量 Python 函数式扩展时 Open WebUI 概念更直接；需要把代码、说明和工作流封装为可安装任务能力时 WorkBuddy Skill 更完整。** 两者对象模型不能一一等同。         |
| 扩展能力   | Pipeline      | Open WebUI Pipelines 是独立的模块化插件框架，可实现过滤、转换、路由、供应商接入及请求/响应自定义逻辑。[OW-1]                                                   | 有 Skills 工作流、定时/事件自动化和 WMA Harness 的 Agent 编排，但公开文档未提供与 Open WebUI Pipelines 对等的全局消息中间件/请求处理管线。[WB-7][WB-8]                                     | **模型请求前后处理、统一路由和平台级中间件：Open WebUI 更优；面向业务结果的多步骤执行与定时任务：WorkBuddy 更优，但不是同一技术层。**                            |
| 多用户管理  | 成员、组织与会话隔离    | 从产品设计上即支持多用户；管理员可管理用户、组、权限、模型访问和用量，并支持 SSO、LDAP、SCIM 及审计/分析能力。[OW-1]                                                   | 个人版以单账号桌面使用为主；企业版按席位管理成员，支持统一身份/SSO、组织架构同步、管理员、日志与用量管理；WMA 为分享链接或 API 调用者创建独立 Session 和文件存储。[WB-9][WB-10][WB-11]                                | **低成本自托管、多租户聊天门户与开放身份协议：Open WebUI 更优；腾讯企业身份、办公渠道、云端 Agent 沙箱和每用户执行环境：WorkBuddy 企业版更强，但采购与平台依赖更高。**        |
| 部署与数据  | 自托管、本地化与数据边界  | 支持 Docker、Kubernetes、pip、裸机部署，可横向扩展；数据库、对象存储、向量库和身份系统均可由组织控制。[OW-1]                                                    | 桌面端支持 Windows/macOS，本地模型和本地 Key；企业版提供 SaaS、专享部署及 WMA 云端沙箱。桌面端不是可由用户自行部署的多用户 Web 服务。[WB-3][WB-8]                                                 | **完整自托管、基础设施可控和避免厂商绑定：Open WebUI 更优；开箱即用的本机执行和托管 Agent Runtime：WorkBuddy 更省运维。**                           |

## 综合结论

1. **Open WebUI 更像 AI 模型与知识能力的统一门户。** 它在多模型并排比较、通用聊天 API、细粒度 RBAC、自托管 RAG、模型配置治理、Pipelines 和多用户门户方面占优。
2. **WorkBuddy 更像能实际操作电脑和业务系统的 AI 同事。** 它在本地文件处理、Office 成果交付、Skill/连接器、办公生态闭环、多步骤任务和云端长任务 Agent Runtime 方面占优。
3. **两者不是完全替代关系。** 如果目标是建设企业内部“统一模型入口/知识问答平台”，优先评估 Open WebUI；如果目标是让 AI 直接执行办公任务并产出文件，优先评估 WorkBuddy。企业也可采用组合架构：Open WebUI 承担统一模型与知识入口，WorkBuddy/WMA 承担端侧或云端任务执行。
4. **关于示例图中的流协议结论。** Open WebUI 的公开接口明确覆盖流式响应；WorkBuddy 公开资料只确认进度展示、长任务和 API Session，没有披露其客户端传输层。因此不建议在正式材料中写“WorkBuddy 原生 gRPC stream”，除非能取得腾讯的接口文档、抓包或厂商书面确认。

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

