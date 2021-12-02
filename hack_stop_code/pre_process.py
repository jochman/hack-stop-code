from abc import abstractclassmethod


class PreProcess:
    def __init__(self, args) -> None:
        self.args = args

    @abstractclassmethod
    def process(self):
        pass