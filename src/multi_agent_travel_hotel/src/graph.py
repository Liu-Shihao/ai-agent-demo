from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

"""
https://langchain-ai.github.io/langgraph/agents/multi-agent/#supervisor
pip install langgraph-supervisor
pip install -e .
langgraph dev 
"""

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


def book_hotel(hotel_name: str):
    """Book a hotel"""
    return f"Successfully booked a stay at {hotel_name}."


def book_flight(from_airport: str, to_airport: str):
    """Book a flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}."


flight_assistant = create_react_agent(
    model=llm,
    tools=[book_flight],
    prompt="You are a flight booking assistant",
    name="flight_assistant"
)

hotel_assistant = create_react_agent(
    model=llm,
    tools=[book_hotel],
    prompt="You are a hotel booking assistant",
    name="hotel_assistant"
)

graph = create_supervisor(
    agents=[flight_assistant, hotel_assistant],
    model=llm,
    prompt=(
        "You manage a hotel booking assistant and a"
        "flight booking assistant. Assign work to them."
    )
).compile()



if __name__ == '__main__':

    for chunk in graph.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "book a flight from BOS to JFK and a stay at McKittrick Hotel"
                    }
                ]
            }
    ):
        print(chunk)
        print("\n")
