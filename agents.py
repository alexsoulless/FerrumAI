from typing import Sequence
import uuid

from dotenv import find_dotenv, load_dotenv
from langchain_core.language_models import LanguageModelLike
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, tool
from langchain_gigachat.chat_models import GigaChat
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from paths import PATH
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
REQUISITES_FILE = "paths.docx"


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


@tool
def process_with_intarfaceAI(prompt: str):
    """
    Обрабатывает запрос через InterfaceAgent и возвращает ответ.
    Если возникает ошибка — возвращает её описание.
    """
    try:
        print(f"Вызван помощник интерфейса с промптом: {prompt}")
        interface_agent = InterfaceAgent(model)  # теперь model передаётся правильно
        agent_response = interface_agent.invoke(prompt)
        
        if not agent_response:
            return "Ошибка: агент не вернул ответ (возможно, проблема в tools или промпте)"
        
        return agent_response
    
    except Exception as e:
        return f"Ошибка в process_with_interfaceAI: {str(e)}"


@tool
def process_with_smarthomeAI(prompt: str) -> str:
    """
    Обработка запроса умномым домом

    Args:
        prompt (str): оптимизированный промпт

    Returns:
        str: результат обработки запроса
    """
    return f"Запрос обработан с помощью smarthomeAI\nprompt:{prompt}"

@tool
def get_paths(description: str) -> dict:
    """
    Получаем все пути всех разделов приложения с описанием.
    Args:
        description (str): описание раздела

    Returns:
        paths: словарь с путями 'путь' ->  'описание'"
    """
    return PATH


class ManagerAgent(LLMAgent):

    def __init__(self):
        super().__init__(
            model,
            tools=[process_with_intarfaceAI, process_with_smarthomeAI],
            prompt=MANAGER_AI_PROMPT,
        )

class InterfaceAgent(LLMAgent):  # <- исправлено имя (без "e")
    def __init__(self, model):  # <- добавлен model как аргумент
        super().__init__(
            model,
            tools=[get_paths],  # убедитесь, что get_paths работает корректно
            prompt=INTERFACE_AI_PROMPT,
        )

