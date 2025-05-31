from agents import ManagerAgent, InterfaceAgent


def print_agent_response(llm_response: str) -> None:
    print(f"\033[35m{llm_response}\033[0m")


def get_user_prompt() -> str:
    return input("\nТы: ")


def start_chat(manager_agent):
    while True:
        agent_response = manager_agent.invoke(get_user_prompt())
        print_agent_response(f"{manager_agent.__repr__()}:{agent_response}")


if __name__ == "__main__":
    manager_agent = ManagerAgent()
    start_chat(manager_agent)
