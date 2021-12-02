from abc import abstractclassmethod
import requests

class PostProcess:
    @abstractclassmethod
    def process(self, response: requests.Response) -> dict:
        pass