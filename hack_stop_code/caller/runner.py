from urllib.parse import urljoin

from api_call import ApiCall
from hack_stop_code.caller.Parser import Parser
from post_process import PostProcess
from pre_process import PreProcess


class Runner:
    def __init__(self, pre_process: PreProcess, parser: Parser, post_process: PostProcess):
        self.pre_process = pre_process
        self.parser = parser
        self.post_process = post_process

    def run(self):
        args = self.pre_process.get_preprocessed_args()
        raw_response = ApiCall()(
            method=self.parser.method,
            url=urljoin(self.parser.base_url, self.parser.suffix),
            headers=self.parser.headers,
            data=self.parser.body,
            verify=not self.parser.insecure,
            proxy=self.parser.proxy,
            params=args.request_args
        )
        response = self.post_process.post_process(raw_response)
        return response
