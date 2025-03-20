import os

from langchain_community.tools.tavily_search import TavilySearchResults
"""
https://python.langchain.com/docs/integrations/tools/tavily_search/
"""
os.environ["TAVILY_API_KEY"] = "..."

tool = TavilySearchResults(max_results=2)
tools = [tool]
result = tool.invoke("What's a 'node' in LangGraph?")
print(result)
"""
[{'title': 'What Is LangGraph and How to Use It? - DataCamp', 'url': 'https://www.datacamp.com/tutorial/langgraph-tutorial', 
'content': 'To install LangGraph, you can use pip:\npip install -U langgraph\nBasic Concepts\nNodes: Nodes represent units of work within your LangGraph. 
They are typically Python functions that perform a specific task, such as: [...] 
Imagine your application as a directed graph. In LangGraph, each node represents an LLM agent, and the edges are the communication channels between these agents. 
This structure allows for clear and manageable workflows, where each agent performs specific tasks and passes information to other agents as needed.\n
State management', 'score': 0.8401668685121951}, 
{'title': "Beginner's Guide to LangGraph: Understanding State, Nodes, and ...", 'url': 'https://medium.com/@kbdhunga/beginners-guide-to-langgraph-understanding-state-nodes-and-edges-part-1-897e6114fa48', 
'content': 'A Simple Graph\nNodes: Nodes are the fundamental building blocks of a graph. 
Each node represents a specific function or operation that processes the current state. Nodes can perform computations, modify the state, 
or generate outputs based on the input they receive. They are typically defined as Python functions or classes that take the current state as input and return an updated state.\n\n--\n\n--\n
1', 'score': 0.8110280065853658}]

"""