# from dataclasses import dataclass, asdict
# import json
# import os
# import subprocess
# from typing import Sequence
# import uuid

# from dotenv import find_dotenv, load_dotenv
# from langchain_core.language_models import LanguageModelLike
# from langchain_core.runnables import RunnableConfig
# from langchain_core.tools import BaseTool, tool
# from langchain_gigachat.chat_models import GigaChat
# from langgraph.prebuilt import create_react_agent
# from langgraph.checkpoint.memory import InMemorySaver
from model_configs import (
    MANAGER_AI_PROMPT,
    INTERFACE_AI_PROMPT,
    SMARTHOME_AI_PROMPT,
    AI_MODEL,
)
from agents import ManagerAgent


def print_agent_response(llm_response: str) -> None:
    print(f"\033[35m{llm_response}\033[0m")


def get_user_prompt() -> str:
    return input("\nТы: ")


def start_chat(manager_agent):
    while True:
        agent_response = manager_agent.invoke(get_user_prompt())
        print_agent_response(agent_response)


def get_aswer(agent, prompt):
    return agent.invoke(prompt)


if __name__ == "__main__":
    manager_agent = ManagerAgent()
    start_chat(manager_agent)
