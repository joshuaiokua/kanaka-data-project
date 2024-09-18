"""
Functionality and saved templates for interfacing with prompts.
"""

# External Libraries
from langchain_core.prompts import ChatPromptTemplate

### --- TEMPLATES --- ###


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
        prompts.append(("human", user_input if user_input else "{user_input}"))

        # Pass the prompts to the parent class
        super().__init__(prompts)

        # Check that prompts have only one user input
        if len(self.input_variables) > 1:
            raise ValueError(
                "Simple Chat Prompt Template must have exactly one input variable.",
            )
