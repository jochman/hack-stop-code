import requests

import demistomock as demisto
from CommonServerPython import CommandResults


class PostProcess:
    @staticmethod
    def post_process(response: requests.Response) -> CommandResults:
        # manipulate json if necessary, just make sure to return CommandResults
        json = response.json()
        return CommandResults(outputs_prefix=demisto.getParam('context_key'),
                              outputs=json,
                              raw_response=json)
