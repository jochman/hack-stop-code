class ApiCall:
    @staticmethod
    def __call__(method: str,
                 url: str = None,
                 headers=None,
                 data=None,
                 verify: bool = True,
                 proxy: bool = False,
                 **kwargs) -> requests.Response:
        return requests.request(method=method, url=url, data=data, headers=headers)
