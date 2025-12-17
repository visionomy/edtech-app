class ClientBase:

    def __init__(self, model_name=None):
        self._model_name = model_name

    def request(self, content, temperature=None, output_schema=None):
        raise NotImplementedError
