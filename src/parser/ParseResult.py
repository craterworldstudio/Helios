class ParseResult:

    def __init__(self):
        self.node = None
        self.error = None

    def register(self, result):
        if result.error:
            self.error = result.error

        return result.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self