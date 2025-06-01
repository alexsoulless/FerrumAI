from typing import Sequence
import uuid

from dotenv import find_dotenv, load_dotenv
from langchain_core.language_models import LanguageModelLike
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, tool
from langchain_gigachat.chat_models import GigaChat
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from paths import PATHS
from devices import DEVICES
from model_configs import (
    MANAGER_AI_PROMPT,
    INTERFACE_AI_PROMPT,
    SMARTHOME_AI_PROMPT,
    AI_MODEL,
)

model = GigaChat(
    model=AI_MODEL,
    verify_ssl_certs=False,
)

load_dotenv(find_dotenv())


class LLMAgent:
    def __init__(
        self, model: LanguageModelLike, tools: Sequence[BaseTool], prompt=None
    ):
        self._model = model
        self._agent = create_react_agent(
            model, tools=tools, checkpointer=InMemorySaver(), prompt=prompt
        )
        self._config: RunnableConfig = {"configurable": {"thread_id": uuid.uuid4().hex}}

    def upload_file(self, file):
        file_uploaded_id = self._model.upload_file(file).id_  # type: ignore
        return file_uploaded_id

    def invoke(
        self,
        content: str,
        attachments: list[str] | None = None,
        temperature: float = 0.1,
    ) -> str:
        """Отправляет сообщение в чат"""
        message: dict = {
            "role": "user",
            "content": content,
            **({"attachments": attachments} if attachments else {}),
        }
        return self._agent.invoke(
            {"messages": [message], "temperature": temperature}, config=self._config
        )["messages"][-1].content
        self,
        content: str,
        attachments: list[str] | None = None,
        temperature: float = 0.1,
    ) -> str:
        """Отправляет сообщение в чат"""
        message: dict = {
            "role": "user",
            "content": content,
            **({"attachments": attachments} if attachments else {}),
        }
        return self._agent.invoke(
            {"messages": [message], "temperature": temperature}, config=self._config
        )["messages"][-1].content


@tool
def process_with_intarfaceAI(prompt: str):
    """
    Обрабатывает запрос через InterfaceAgent и возвращает ответ.
    Если возникает ошибка — возвращает её описание.
    """
    try:
        print(f"process_with_intarfaceAI({prompt})")
        interface_agent = InterfaceAgent()
        agent_response = interface_agent.invoke(prompt)

        if not agent_response:
            return (
                "Ошибка: агент не вернул ответ (возможно, проблема в tools или промпте)"
            )

        return agent_response

    except Exception as e:
        return f"Ошибка в process_with_interfaceAI: {str(e)}"


@tool
def process_with_smarthomeAI(prompt: str) -> str:
    """
    Обрабатывает запрос через smarthomeAI и возвращает ответ.
    Если возникает ошибка — возвращает её описание.
    """
    try:
        # print(f"process_with_smarthomeAI({prompt})")
        smhome_agent = SmartHomeAgent()
        agent_response = smhome_agent.invoke(prompt)
        print(f"agent_response: {agent_response}")

        if not agent_response:
            return (
                "Ошибка: агент не вернул ответ (возможно, проблема в tools или промпте)"
            )

        return agent_response

    except Exception as e:
        # print(f"Ошибка в process_with_smarthomeAI: {str(e)}")
        return f"Ошибка в process_with_smarthomeAI: {str(e)}"


class ManagerAgent(LLMAgent):

    def __init__(self):
        super().__init__(
            model,
            tools=[process_with_intarfaceAI, process_with_smarthomeAI],
            prompt=MANAGER_AI_PROMPT,
        )


@tool
def get_paths() -> dict:
    """
    Получаем все пути всех разделов приложения с описанием.

    Returns:
        paths: словарь с путями разделов 'путь' ->  'описание'"
    """
    print("get_paths")
    return PATHS


class InterfaceAgent(LLMAgent):
    def __init__(self):
        super().__init__(
            model,
            tools=[get_paths],
            prompt=INTERFACE_AI_PROMPT,
        )


@tool
def get_devices() -> dict:
    """
    Получаем доступные устройства в умном доме и пути для вызова их функций

    Returns:
        devices: словарь с описанием устройств умного дома в формате
        {"путь": "описание",...}
    """
    print("get_devices")
    return DEVICES


@tool
def perform_device_func(path:str) -> int:
    """
    Вызов функции устройства умного дома

    Args:
        path (str): путь к функции

    Returns:
        int: код ошибки; 0 - успешно, 1 - неудачно
    """
    print(f"Вызвана функция устройства умного дома {path}")
    return 0

class SmartHomeAgent(LLMAgent):
    def __init__(self):
        super().__init__(
            model,
            tools=[get_devices, perform_device_func],
            prompt=SMARTHOME_AI_PROMPT,
        )
