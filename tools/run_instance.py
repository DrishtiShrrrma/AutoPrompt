import ray
from tools import all_tools
from langchain.agents import initialize_agent, AgentType

ray.init()

# Initialize an agent with the tools from tools.py
agent = initialize_agent(
    tools=all_tools,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

response = agent("Who was Harry Potter")
print(response)
