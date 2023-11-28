import time
from jarvis.enviroment.base_env import BaseEnviroment
from jarvis.agent.openai_agent import OpenAIAgent

if __name__ == '__main__':
    environment = BaseEnviroment()
    agent = OpenAIAgent(
        config_path="examples/config.json",
        environment=environment
    )
    action = [
        'turn_on_dark_mode',
        'turn_on_light_mode'
    ]

    # environment.init_env()
    for a in action:
        print(a)
        command = agent.action_lib[a]
        print(agent.env.step(command))
        time.sleep(2)
