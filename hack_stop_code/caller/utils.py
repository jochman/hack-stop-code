from pathlib import Path
from typing import Union


class Constants:
    body = 'body'
    auth_custom = 'auth_custom'
    auth_format = 'auth_format'
    authentication_type = '_auth_type'
    auth_header_key = 'Authorization'
    password_placeholder = ':password'
    username_placeholder = ':username'
    auth_bearer = 'Bearer'
    auth_basic = 'Basic'
    auth_none = 'None'
    context_key = 'context_key'
    method = 'method'
    suffix = '_suffix'
    post_process = '_post_process'
    pre_process = '_pre_process'
    base_url = 'base_url'
    insecure = 'insecure'
    proxy = 'proxy'


def load_json(path: Union[str, Path]):
    with Path(path).open() as f:
        return load_json(f)
