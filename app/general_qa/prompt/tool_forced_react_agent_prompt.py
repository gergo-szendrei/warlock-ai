from langchain_core.prompts import PromptTemplate

tool_forced_react_agent_template = """
    {instructions}
    
    TOOLS:
    ------
    
    You have access to the following tools:
    
    {tools}
    
    You MUST always use a tool!
    To use a tool, please use the following format:
    
    ```
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ```
    
    When you have a response to say to the Human, you MUST use the format:
    
    ```
    Thought: Do I need to use a tool? No
    Final Answer: [your response here]
    ```
    
    Begin!
    
    Previous conversation history:
    {chat_history}
    
    New input: {input}
    {agent_scratchpad}
"""

tool_forced_react_agent_prompt = PromptTemplate(
    template=tool_forced_react_agent_template,
    input_variables=[
        "instructions",
        "tools",
        "tool_names",
        "chat_history",
        "agent_scratchpad"
    ]
)
