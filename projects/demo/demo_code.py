class Demo:
    def __init__(self):
        self.text = "Hello World! You said: "

    def get_text(self, input: str) -> str:
        return self.text + input
