import requests


class PostProcess:
    @staticmethod
    def post_process(response: requests.Response) -> dict:
        # manipulate the response here and return a dictionary
        # or just return response.json()
        return response.json()
