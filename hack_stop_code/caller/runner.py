from requests import request

from . import PreProcess, PostProcess


class Runner:
    def __init__(
            self,
            pre_process: PreProcess,
            post_process: PostProcess,
    ) -> None:
        self.pre_process = pre_process
        self.api_call = api_call
        self.post_process = post_process

    def run(self, args):
        args = self.pre_process.process(args)
        # response = self.api_call.call(**args)
        response = request(**args)
        processed_data = self.post_process.process(response)
        return processed_data
