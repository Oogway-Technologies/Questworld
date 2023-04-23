import os
import openai
import networkx as nx
from pathlib import Path
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import BaseMessagePromptTemplate, ChatPromptTemplate
from projects.worldbuilding.utils import get_goal_prompt, get_plan_prompt, get_plan_prompt_clean
from config import Config


def setup_keys():
    # Initialize OpenAI
    if Config.OPENAI_ORGANIZATION is not None and Config.OPENAI_ORGANIZATION != "":
        openai.organization = Config.OPENAI_ORGANIZATION
    openai.api_key = Config.OPENAI_API_KEY


def load_json(filepath):
    import json
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return json.load(infile)
    except Exception as e:
        return None


def save_json(filepath, data):
    import json
    try:
        with open(filepath, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4)
    except Exception as e:
        return None


class Worldbuilding:
    def __init__(self, max_tokens: int = 256, model_name: str = "gpt-3.5-turbo"):
        self.world_graph = nx.Graph()
        self.locations = dict()
        self.main_area = None
        self.areas_data = None
        self.agents_data = None
        self.agents_goals = dict()
        self.agents_plans = dict()
        self.max_tokens = max_tokens
        self.model_name = model_name
        self.global_time = 8
        self.llm = ChatOpenAI(max_tokens=self.max_tokens,
                              model_name=self.model_name)

    def _create_agent_llm_chain(self, prompt: BaseMessagePromptTemplate) -> LLMChain:
        chat_prompt = ChatPromptTemplate.from_messages(
            [prompt])
        chain = LLMChain(llm=self.llm, prompt=chat_prompt, verbose=False)
        return chain

    def _generate_agent_goal(self, agent: str):
        prompt = get_goal_prompt()
        all_agents = ', '.join(list(self.agents_data.keys()))
        llm_chain = self._create_agent_llm_chain(prompt)
        plan = llm_chain.run(
            agent=agent,
            agent_description=self.agents_data[agent],
            source_area='the town of Phandalin',
            destination_area='Town Square',
            people=all_agents
        )
        return plan

    def load_agents_data(self, agents_data_path: str):
        # Load the json file containing the agents data
        path = os.path.expanduser(agents_data_path)
        self.agents_data = load_json(path)

    def load_data(self, areas_data_path: str, agents_data_path: str):
        # Load the json file containing the agents data
        path = os.path.expanduser(areas_data_path)
        self.areas_data = load_json(path)

        # Initialize the world graph
        self.main_area = self.areas_data['main_area']
        for area in self.areas_data['all_areas'].keys():
            self.world_graph.add_node(area)
            self.world_graph.add_edge(area, area)

        # Connect all areas to the main area
        for area in self.areas_data['all_areas'].keys():
            self.world_graph.add_edge(area, self.main_area)

        # Load the agents and assign them to the central area
        self.load_agents_data(agents_data_path)
        for agent in self.agents_data.keys():
            self.locations[agent] = self.main_area

    def generate_agents_plans(self):
        # Try to load the goals from the json file
        path_to_agents_goals = os.path.join(
            Path(__file__).parent.parent.parent, 'projects/worldbuilding/data/agents_goals.json')
        # Check if the file exists
        if os.path.exists(path_to_agents_goals):
            self.agents_goals = load_json(path_to_agents_goals)
        else:
            # Generate the goals for each agent
            for agent in self.agents_data.keys():
                print(f'Generating goal for agent: {agent}')
                self.agents_goals[agent] = self._generate_agent_goal(agent)

            # Save the goal
            save_json(path_to_agents_goals, self.agents_goals)

        # Generate the plans for each agent
        path_to_agents_plans = os.path.join(
            Path(__file__).parent.parent.parent, 'projects/worldbuilding/data/agents_plans.json')
        if os.path.exists(path_to_agents_plans):
            self.agents_plans = load_json(path_to_agents_plans)
        else:
            agents = list()
            for location in self.areas_data['all_areas'].keys():
                for agent in self.agents_data.keys():
                    if self.locations[agent] == location:
                        # If the agent is in one of the current locations, generate a plan for it
                        agents.append(agent)

            plan_prompt = get_plan_prompt()
            plan_prompt_clean = get_plan_prompt_clean()
            all_agents = ', '.join(agents)
            for agent in agents:
                print(f'Generating plan for agent: {agent}')
                agents_descriptions = []
                for agent_name in agents:
                    if agent_name == agent:
                        continue
                    agents_descriptions.append(
                        agent_name + ': ' + self.agents_data[agent_name] + '\n')

                llm_chain = self._create_agent_llm_chain(plan_prompt)
                plan = llm_chain.run(
                    agent=agent,
                    agent_description=self.agents_data[agent],
                    plan=self.agents_goals[agent],
                    location=self.locations[agent],
                    location_description=self.areas_data['all_areas'][self.locations[agent]],
                    time=self.global_time,
                    people=all_agents,
                    people_description='- '.join(agents_descriptions)
                )
                llm_chain = self._create_agent_llm_chain(plan_prompt_clean)
                plan = llm_chain.run(paragraph=plan)
                self.agents_plans[agent] = plan.replace(
                    '"', '').replace("'", '').strip()

            # Save the plans
            save_json(path_to_agents_plans, self.agents_plans)


if __name__ == "__main__":
    setup_keys()

    wb = Worldbuilding()
    path_to_agents = os.path.join(
        Path(__file__).parent.parent.parent, 'projects/worldbuilding/data/agents.json')
    path_to_areas = os.path.join(
        Path(__file__).parent.parent.parent, 'projects/worldbuilding/data/areas.json')
    wb.load_data(path_to_areas, path_to_agents)
    wb.generate_agents_plans()
