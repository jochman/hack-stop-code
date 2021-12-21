import requests


class ApiCall:
    @staticmethod
    def __call(method: str, url: str = None, headers=None, data=None, **kwargs) -> requests.Response:
        return requests.request(method=method, url=url, data=data, headers=headers)