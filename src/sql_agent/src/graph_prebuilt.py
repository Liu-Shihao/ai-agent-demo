import os

from langchain_community.chat_models import ChatTongyi

"""
pip install pymysql

https://langchain-ai.github.io/langgraph/tutorials/sql-agent/

cd src/sql_agent
pip install -e .
langgraph dev 
"""

os.environ["DASHSCOPE_API_KEY"] = "sk-a91bb251d68743c0a5e2a53a8534162c"

from langchain_community.utilities import SQLDatabase

db_url = "mysql+pymysql://root:Lsh123456!@localhost/user?charset=utf8mb4"
db = SQLDatabase.from_uri(db_url)

llm = ChatTongyi(model="qwen-plus")

from langchain_community.agent_toolkits import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

from langgraph.prebuilt import create_react_agent

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect=db.dialect,
    top_k=5,
)

graph = create_react_agent(
    llm,
    tools,
    prompt=system_prompt,
)

if __name__ == '__main__':
    print(f"Dialect: {db.dialect}")
    print(f"Available tables: {db.get_usable_table_names()}")
    print(f'Sample output: {db.run("SELECT * FROM user_info LIMIT 5;")}')
    """
    Dialect: mysql
    Available tables: ['user_info']
    Sample output: [(1, '张三', 'zhangsan', 22, datetime.datetime(2022, 7, 26, 14, 46, 33))]
    """
