import requests

from ..CommonServerPython import CommandResults

'''
{
  "ip": "1.1.1.1",
  "hostname": "one.one.one.one",
  "anycast": true,
  "city": "Miami",
  "region": "Florida",
  "country": "US",
  "loc": "25.7867,-80.1800",
  "org": "AS13335 Cloudflare, Inc.",
  "postal": "33132",
  "timezone": "America/New_York",
  "readme": "https://ipinfo.io/missingauth"
}
'''


class PostProcess:
    @staticmethod
    def post_process(response: requests.Response) -> dict:
        json = response.json()

        command_result = CommandResults(
            outputs_prefix='demo',  # todo
            outputs={k: v for k, v in json.items() if k in {'ip', 'hostname', 'loc', 'country'}},
            raw_response=json,
        )
        # manipulate the response here and return a dictionary
        # or just return response.json()
        return response.json()
