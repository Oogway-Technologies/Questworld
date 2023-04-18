from server.base_handler import BaseHandler
from projects.llm.agents.builder import build_agent
from projects.llm.agents.utils import create_memory_retriever, create_agent_llm


class Handler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.memory_retriever = None
        self.agent = build_agent(
            name="Bruce",
            age=25,
            traits="intelligent, idealist, realist",
            status="fighting crime",
            memory_retriever=create_memory_retriever(),
            llm=create_agent_llm(),
            daily_summaries=[
                "Bruce started fighting crime as a masked vigilante one year ago. Today he is patroling the streets choosing his target to bring to justice."],
            reflection_threshold=5
        )

    def serve_request(self, event, context):
        memories = event["memories"]

        # Add memories
        for memory in memories:
            self.agent.add_memory(memory)

        # TODO: replace with the agent's code
        summary = self.agent.get_summary(force_refresh=True)
        response = {"summary": summary}

        return response


handler = Handler()


def handler_request(event: dict, context: dict) -> dict:
    return handler.handle_request(event, context)
