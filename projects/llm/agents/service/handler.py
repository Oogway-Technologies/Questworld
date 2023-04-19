from server.base_handler import BaseHandler
from projects.llm.agents.builder import build_agent
from projects.llm.agents.utils import create_memory_retriever, create_agent_llm, observe_agent
from projects.llm.agents.conversation import run_conversation


class Handler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.agents = []

    def serve_request(self, event, context):
        agents = event["agents"]
        run_convo = event.get("run_conversation", False)
        initial_observation = event.get("initial_observation", "")

        # Create the agents
        for agent_data in agents:
            agent = build_agent(
                name=agent_data["name"],
                age=agent_data["age"],
                character_class=agent_data["character_class"],
                traits=', '.join(agent_data["traits"]),
                status=agent_data["status"],
                memory_retriever=create_memory_retriever(),
                llm=create_agent_llm(),
                daily_summaries=agent_data["daily_summaries"],
                reflection_threshold=agent_data["reflection_threshold"]
            )
            self.agents.append(
                {
                    "name": agent_data["name"],
                    "agent": agent,
                    "observations": agent_data["observations"],
                    "observation_threshold": agent_data["observation_threshold"]
                }
            )

        if run_convo:
            # Run the conversation
            agents_list = [agent["agent"] for agent in self.agents]
            run_conversation(agents_list, initial_observation)
        else:
            # Run observations
            for agent in self.agents:
                agent_entity = agent["agent"]
                observe_agent(
                    agent_entity, agent["observations"], agent["observation_threshold"])

        # TODO: return summary if asked from input
        # summary = self.agent.get_summary(force_refresh=True)
        response = {"summary": ""}

        return response


handler = Handler()


def handler_request(event: dict, context: dict) -> dict:
    return handler.handle_request(event, context)
