from langchain_core.prompts import PromptTemplate

tool_forced_no_thought_react_agent_template = """
    {instructions}
    
    TOOLS:
    ------
    
    You have access to the following tools:
    
    {tools}
    
    You MUST always use a tool!
    
    After one tool usage, you MUST respond to the human, and you MUST use the format:
    
    ```
    Final Answer: [your response here]
    ```
    
    Begin!
    
    Previous conversation history:
    {chat_history}
    
    New input: {input}
    {agent_scratchpad}
"""

tool_forced_no_thought_react_agent_prompt = PromptTemplate(
    template=tool_forced_no_thought_react_agent_template,
    input_variables=[
        "instructions",
        "tools",
        "tool_names",
        "chat_history",
        "agent_scratchpad"
    ]
)
