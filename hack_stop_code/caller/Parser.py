from enum import Enum, auto
from pathlib import Path
from typing import NamedTuple

from hack_stop_code.caller.CommonServerPython import argToBoolean
from hack_stop_code.caller.utils import Constants

DEFAULT_POST_PROCESS = Path('post_process.py').read_text()
DEFAULT_PRE_PROCESS = Path('pre_process.py').read_text()


class Prefixes:
    bearer = 'bearer'

    body_arg = '_body_arg'
    custom_arg = '_custom_arg'
    path_param = '_path_param'
    request_arg = '_request_arg'

    header = '_header'
    authorization = 'authorization'
    configuration = 'configuration'
    pre_process = 'preprocess'
    post_process = 'preprocess'


class ParsedArguments(NamedTuple):
    path_args: dict
    custom_args: dict
    request_args: dict
    body_args: dict


class AuthenticationType(Enum):
    Basic = auto()
    Bearer = auto()
    Custom = auto()
    NoAuth = auto()


class Parser:
    def __init__(self, params: dict, args: dict):
        self._params = params
        self._args = args

        self.base_url = params.get(Constants.base_url)
        self.insecure = argToBoolean(params.get(Constants.insecure, False))
        self.proxy = params.get(Constants.proxy, False)

        self.method = args.get(Constants.method)
        self.body = args.get(Constants.body)
        self.context_key = args.get(Constants.context_key)
        self._parsed_arguments = self.parse_special_args(args)

        self.headers = Parser._extract_headers(args) | Parser._extract_headers(params) | self.generate_auth_header()
        self.suffix = self._parse_replace_suffix(args)

        # todo pass token as url path param
        self._pre_process_code = args.get(Constants.pre_process) or DEFAULT_PRE_PROCESS
        self._post_process_code = args.get(Constants.post_process) or DEFAULT_POST_PROCESS

        exec(self._pre_process_code, globals())  # imports the customized PreProcess class
        exec(self._post_process_code, globals())  # imports the customized PostProcess class

        # noinspection PyUnresolvedReferences
        self.pre_processor = PreProcess(self._parsed_arguments)
        # noinspection PyUnresolvedReferences
        self.post_processor = PostProcess()

    def generate_auth_header(self):
        auth_format = self._params.get(Constants.auth_format)
        authentication_type = self._parse_authentication_type(self._params)

        if auth_format and authentication_type != AuthenticationType.Custom:
            raise ValueError(f"Cannot have auth format with a non-custom authentication type {authentication_type}")

        if authentication_type == AuthenticationType.NoAuth:
            return dict()

        username = self._params.get('credentials', {}).get('username', '')
        password = self._params.get('credentials', {}).get('password', '')

        auth_type_to_auth_format = {
            AuthenticationType.Basic: f'Basic {Constants.username_placeholder}:{Constants.password_placeholder}',
            AuthenticationType.Bearer: f'Bearer {Constants.password_placeholder}',
            AuthenticationType.Custom: auth_format
        }
        try:
            auth_format = auth_type_to_auth_format[authentication_type]
        except KeyError:
            raise ValueError(f"Unexpected auth type={authentication_type}")

        if not auth_format:
            raise ValueError(f"Empty auth_format, auth type={authentication_type}")

        auth_header_value = auth_format \
            .replace(Constants.password_placeholder, password) \
            .replace(Constants.username_placeholder, username)

        return {Constants.auth_header_key: auth_header_value}

    @staticmethod
    def _parse_authentication_type(params: dict):
        raw_authentication_type = params.get(Constants.authentication_type, Constants.auth_none)

        string_to_type = {Constants.auth_basic: AuthenticationType.Basic,
                          Constants.auth_bearer: AuthenticationType.Bearer,
                          Constants.auth_none: AuthenticationType.NoAuth,
                          Constants.auth_custom: AuthenticationType.Custom}

        return string_to_type[raw_authentication_type]

    def _parse_replace_suffix(self, args):  # call after calling parse_special_args()
        suffix = args.get(Constants.suffix, '')
        for k, v in self._parsed_arguments.path_args.items():
            suffix = suffix.replace(f':{k}', v)
        return suffix

    @staticmethod
    def parse_special_args(args):
        path_params = {}
        custom_args = {}
        request_args = {}
        body_args = {}

        prefix_to_dict = {
            f'{Prefixes.path_param}:': path_params,
            f'{Prefixes.custom_arg}:': custom_args,
            f'{Prefixes.request_arg}:': request_args,
            f'{Prefixes.body_arg}:': body_args
        }

        for k, v in args.items():
            for prefix, destination in prefix_to_dict.items():
                if k.startswith(prefix):
                    destination[k.removeprefix(prefix)] = v
                    break

        return ParsedArguments(path_args=path_params, custom_args=custom_args,
                               request_args=request_args, body_args=body_args)

    @staticmethod
    def _extract_headers(data: dict):
        result = dict()
        result.update({k.removeprefix(f'{Prefixes.header}:'): v
                       for k, v in data.items()
                       if k.startswith(f'{Prefixes.header}:')})
        return result
