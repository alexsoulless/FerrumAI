from agents import ManagerAgent, InterfaceAgent

manager_agent = ManagerAgent()

def print_agent_response(llm_response: str) -> None:
    print(f"\033[32m🧩 {llm_response}\033[0m")


def get_user_prompt() -> str:
    return input("\nТы: ")


def start_chat(manager_agent):
    while True:
        agent_response = manager_agent.invoke(get_user_prompt())
        print_agent_response(agent_response)

def get_ai_response(promtp):
    return manager_agent.invoke(promtp)


if __name__ == "__main__":
    try:
        start_chat(manager_agent)
    except KeyboardInterrupt:
        print("\nОбщение завершено")
