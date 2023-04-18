from server.base_handler import BaseHandler
from projects.demo.demo_code import Demo


class Handler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.demo = Demo()

    def serve_request(self, event, context):
        arg = event.get("input", None)
        if arg is None:
            arg = "Nothing"

        # Process the input request
        out_text = self.demo.get_text(arg)
        response = {"response": out_text}

        return response


handler = Handler()


def handler_request(event: dict, context: dict) -> dict:
    return handler.handle_request(event, context)
