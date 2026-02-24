


class ClientNotFound(Exception):
    def __init__(self, id: int) -> None:
        self.id = id