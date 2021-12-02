from abc import abstractclassmethod


import requests

class ApiCall:
    def __init__(
        self, url, headers: dict = {}
    ) -> None:
        self.url = url
        self.headers = headers

    @abstractclassmethod
    def call(
        self, method, suffix: str = None, headers = {}, **kwargs
    ) -> requests.Response:
        pass