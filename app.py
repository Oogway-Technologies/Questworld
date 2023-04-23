import openai
import argparse
from server.flask_server import ModelServer
from utils.config_utils import setup_keys
from config import Config


parser = argparse.ArgumentParser()
parser.add_argument(
    "--run_server",
    type=str,
    required=False,
    choices=["true", "false"],
    help="Run the app as a server or not.",
)
parser.add_argument(
    "--service_type",
    type=str,
    required=False,
    choices=["demo", "agents"],
    help="Which service to start",
)


def run_app():
    # Your app code here
    print('hello from app')


if __name__ == "__main__":
    setup_keys()

    args = parser.parse_args()
    if args.run_server is not None and args.run_server == "true":
        # Run the server
        if args.service_type is not None:
            if args.service_type == "agents":
                from projects.llm.agents.service.handler import handler_request
            else:
                # Deafult to demo
                from projects.demo.service.handler import handle_request
        else:
            # Deafult to demo
            from projects.demo.service.handler import handle_request

        server = ModelServer(Config.SERVER_PORT, handler_request)
        server.start()
    else:
        # Run the app
        run_app()
