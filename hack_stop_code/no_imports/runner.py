from urllib.parse import urljoin


class Runner:
    def __init__(self):
        self.parser = Parser(params=demisto.params(), args=demisto.args())

    def run(self):
        args = self.parser.pre_processor.get_preprocessed_args()
        raw_response = ApiCall()(
            method=self.parser.method,
            url=urljoin(self.parser.base_url, self.parser.suffix),
            headers=self.parser.headers,
            data=self.parser.body,
            verify=not self.parser.insecure,
            proxy=self.parser.proxy,
            params=args.request_args
        )
        return self.parser.post_processor.post_process(raw_response)
