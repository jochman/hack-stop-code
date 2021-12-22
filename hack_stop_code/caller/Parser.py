from pathlib import Path
from typing import NamedTuple

from hack_stop_code.caller.utils import Constants

DEFAULT_POST_PROCESS = Path('post_process.py').read_text()
DEFAULT_PRE_PROCESS = Path('pre_process.py').read_text()


class Prefixes:
    body_arg = '_body_arg'
    custom_arg = '_custom_arg'
    url_arg = '_url_arg'
    request_arg = '_request_arg'  # todo jochman
    header = 'header'
    authorization = 'authorization'
    configuration = 'configuration'
    pre_process = 'preprocess'
    post_process = 'preprocess'


class CommandArguments(NamedTuple):
    url_args: dict
    custom_args: dict
    request_args: dict
    body_args: dict


class Parser:
    @staticmethod
    def parse_authorization(s: str):
        return s.removeprefix(f"{Prefixes.authorization}:")

    @staticmethod
    def parse_header(s: str):
        if s.startswith(Prefixes.authorization):
            return Parser.parse_authorization(s)
        # todo other auth types

    def __init__(self, params: dict, args: dict):
        self.method = args.get(Constants.method)
        self.context_key = args.get(Constants.context_key)

        pre_process_code = args.get(Constants.pre_process) or DEFAULT_PRE_PROCESS
        post_process_code = args.get(Constants.post_process) or DEFAULT_POST_PROCESS

        self.pre_process_script = exec(pre_process_code, globals())
        self.post_process_script = exec(post_process_code, globals())

        self.parsed_arguments = self.parse_special_args(args)

        self.headers = Parser._extract_headers(args) | Parser._extract_headers(params)

        suffix = args.get(Constants.suffix)
        for k, v in self.parsed_arguments.url_args.items():
            if f'<{k}>' in suffix:
                suffix = suffix.replace(f'<{k}>', v)
        self.suffix = suffix

    @staticmethod
    def parse_special_args(args):
        url_args = {}
        custom_args = {}
        request_args = {}
        body_args = {}

        prefix_to_dict = {f'{Prefixes.url_arg}:': url_args,
                          f'{Prefixes.custom_arg}:': custom_args,
                          f'{Prefixes.request_arg}:': request_args,
                          f'{Prefixes.body_arg}:': body_args}

        for k, v in args.items():
            for prefix, destination in prefix_to_dict.items():
                if k.startswith(prefix):
                    destination[k.removeprefix(prefix)] = v
                    break

        return CommandArguments(url_args=url_args, custom_args=custom_args,
                                request_args=request_args, body_args=body_args)

    @staticmethod
    def _extract_headers(data: dict):
        return {Parser.parse_header(k): v
                for k, v in data.items()
                if k.startswith(f'{Prefixes.header}:')}
