from . import PreProcess, PostProcess, ApiCall

class Runner:
    def __init__(
        self,
        pre_process: PreProcess,
        api_call: ApiCall,
        post_process: PostProcess,
    ) -> None:
        self.pre_process = pre_process
        self.api_call = api_call
        self.post_process = post_process

    def run(self, args):
        args = self.pre_process.process(args)
        response = self.api_call.call(**args)
        processed_data = self.post_process.process(response)
        return processed_data