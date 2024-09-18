"""
Functionality and saved templates for interfacing with prompts.
"""

# External Libraries
from langchain_core.prompts import ChatPromptTemplate

### --- TEMPLATES --- ###
QUERY_GENERATION_SYSTEM_PROMPT = """You are a SQL expert with a strong attention to detail.

Given an input question, output a syntactically correct SQLite query to run, then look at the results of the query and return the answer.

DO NOT call any tool besides SubmitFinalAnswer to submit the final answer.

When generating the query:

Output the SQL query that answers the input question without a tool call.

Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.

If you get an error while executing a query, rewrite the query and try again.

If you get an empty result set, you should try to rewrite the query to get a non-empty result set.
NEVER make stuff up if you don't have enough information to answer the query... just say you don't have enough information.

If you have enough information to answer the input question, simply invoke the appropriate tool to submit the final answer to the user.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database."""


### --- CLASSES --- ###
class SimpleChatPromptTemplate(ChatPromptTemplate):
    """Simple Chat Prompt Template constrained to a single input."""

    def __init__(
        self,
        system_prompt: str | None = None,
        user_input: str | None = None,
    ) -> None:
        """Initialize a Simple Chat Prompt Template."""
        # Define the prompts
        prompts = [("system", system_prompt)] if system_prompt else []
        prompts.append(("human", user_input if user_input else "{messages}"))

        # Pass the prompts to the parent class
        super().__init__(prompts)

        # Check that prompts have only one user input
        if len(self.input_variables) > 1:
            raise ValueError(
                "Simple Chat Prompt Template must have exactly one input variable.",
            )
