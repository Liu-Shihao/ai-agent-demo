# Milvus

https://milvus.io/docs/zh/quickstart.md


# Install Milvus

https://milvus.io/docs/zh/install-overview.md

## 使用 Milvus Lite 在本地运行 Milvus
Milvus Lite 是Milvus 的轻量级版本，Milvus 是一个开源向量数据库，通过向量嵌入和相似性搜索为人工智能应用提供支持。
它可以通过`pip install pymilvus` 简单地部署。

Milvus Lite 目前支持以下环境：

- Ubuntu >= 20.04（x86_64 和 arm64）
- MacOS >= 11.0（苹果硅 M1/M2 和 x86_64）

```bash
pip install -U pymilvus
```

# Connection Milvus
在pymilvus 中，指定一个本地文件名作为 MilvusClient 的 uri 参数将使用 Milvus Lite。


```python
from pymilvus import MilvusClient
client = MilvusClient("./milvus_demo.db")
```
运行上述代码段后，将在当前文件夹下生成名为milvus_demo.db 的数据库文件。