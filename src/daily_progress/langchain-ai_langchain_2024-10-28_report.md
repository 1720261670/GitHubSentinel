# langchain-ai/langchain 每日进展 - 2024-10-28

## 新增功能
- langchain: 为多查询检索器添加交集支持 #27670
- community: 为 Cloudflare workers-ai LLM 添加 Cloudflare AI 网关选项 #27671
- community: 添加 Snowflake 模型会话管理，通过密钥文件和外部会话 #27664
- community: 为 Cloudflare Workers AI 添加 ChatModels 封装 #27645
- community: 添加 ObjectBox 作为向量存储 #27644
- community: 添加 `@mozilla/readability` 文档转换器 #27604

## 主要改进
- docs: 修正语法和提高阅读性 #27672
- community: 更新 Replicate LLM 并修复测试 #27655
- community: 添加 Writer 集成 #27646
- core: 修改 RunnableWithMessageHistory 的 get_input_schema 方法，以利用底层 runnable 输入键 #27619

## 修复问题
- "Action Input"在使用 AgentExecutor 时丢失末尾符号 #27673
- Model 在 GraphSparqlQAChain 中在不应该的情况下使用内部知识来回答问题 #27669
- DOC: 改进 LangChain 中工具集成的文档 #27668
- fix the grammar and markdown component #27657
- Multi-agent supervisor 示例在 ChatOllama 中不适用，在尝试使用两个系统消息时会中断。可能是 ChatOllama 中使用两个系统提示存在问题 #27656
- fix typo (missing letter) in elasticsearch_retriever.ipynb #27639
- DOC: 数据解析错误处理（如果重试和数据修复不起作用） #27635
- [AIMessage]tool_calls.0.args 未始终作为有效字典返回 #27632
- community: 使用 sqlalchemy 2.0.36 时出现失败的单元测试 #27627
- Error during FAISS save_local due to __pydantic_private__ attribute #27625
- Cant import any of the HuggingFaceEmbeddings because 'openssl' has no attribute 'ciphers' #27624
- Confluence Loader: 修复 CQL 加载 #27620
- docs: 在持续集成中运行 how-to 指南 #27615
- check broken links #27614
- Various warnings due to Pydantic protected namespaces, such as UserWarning: Field "model_name" in JinaEmbeddings has conflict with protected namespace "model_". #27609
- community: 处理 chatdeepinfra jsondecode 错误 #27603