from urllib.parse import urljoin

from api_call import ApiCall
from hack_stop_code.caller.Parser import Parser
from post_process import PostProcess
from pre_process import PreProcess


class Runner:
    def __init__(
            self,
            pre_process: PreProcess,
            parser: Parser,
            post_process: PostProcess
    ) -> None:
        self.pre_process = pre_process
        self.parser = parser
        self.post_process = post_process

    def run(self):
        args = self.pre_process.process()  # changes args inplace
        response = ApiCall()(
            method=self.parser.method,
            url=urljoin(self.parser.base_url, self.parser.suffix),
            headers=self.parser.headers,
            data=self.parser.body,
            verify=not self.parser.insecure,
            proxy=self.parser.proxy,
            params=args.request_args
        )
        processed_data = self.post_process.process(response)
        return processed_data
