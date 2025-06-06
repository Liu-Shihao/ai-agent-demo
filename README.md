# LangGraph For Multi-Agent
使用LangGraph构建多Agent应用程序

## Setup
```bash
conda create -n langgraph python=3.12

conda activate langgraph

pip install requirements.txt

pip install -e .

langgraph dev
```

## Agent Chat UI
```bash
cd src/agent-chat-ui

pnpm install

pnpm dev
```
The app will be available at `http://localhost:5173`.


# Langgraph

## Multi-Agent

- [Multi-agent](https://langchain-ai.github.io/langgraph/how-tos/#multi-agent)
- [Multi-Agent Systems](https://langchain-ai.github.io/langgraph/tutorials/#multi-agent-systems)


# Ollama 
https://ollama.com/
https://ollama.com/library/nomic-embed-text
发现DeepSeek没有提供embedding的api，所以使用本地 Ollama 来提供embedding服务。
使用Ollama也可以本地部署Deepseek Model，不需要调用Deepseek API，不需要充值。

```bash
## 下载embdding模型
ollama pull nomic-embed-text
```

