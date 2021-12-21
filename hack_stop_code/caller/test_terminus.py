from Parser import Prefixes, Parser
from utils import Constants


def test_sanity():
    args = {
        'ip': '1.1.1.1',
        Constants.pre_process: None,
        Constants.post_process: None,
        Constants.method: 'GET',
        Constants.suffix: 'ip',
        'headers:accept': 'json/application',
        f'{Prefixes.body_arg}:body_arg_1': 'body_arg_value_1',
        f'{Prefixes.url_arg}:url_arg_1': 'url_arg_value_1',
    }
    params = {
        'base_url': 'ipinfo.io',
        'header:authorization': 'my_secret_key',
        'context_key': 'ipinfo.ip'
    }
    Parser(params=params, args=args)
    assert 0
