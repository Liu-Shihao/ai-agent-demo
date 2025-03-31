import os


from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage

"""
pip install --upgrade --quiet  dashscope langchain-community
"""

os.environ["DASHSCOPE_API_KEY"] = "..."

chatLLM = ChatTongyi(
    model="qwq-32b",
    streaming=False,
)
res = chatLLM.stream([HumanMessage(content="9.9和9.11谁大")], streaming=True)
for r in res:
    print("chat resp:", r)
