from Parser import Prefixes, Parser, CommandArguments, DEFAULT_PRE_PROCESS, DEFAULT_POST_PROCESS
from utils import Constants


def test_sanity():
    args = {
        'ip': '1.1.1.1',
        Constants.pre_process: None,
        Constants.post_process: None,
        Constants.method: 'GET',
        Constants.suffix: 'ip',
        Constants.context_key: 'context_key',
        'headers:accept': 'json/application',
        f'{Prefixes.body_arg}:body_arg_1': 'body_arg_value_1',
        f'{Prefixes.url_arg}:url_arg_1': 'url_arg_value_1',
        f'{Prefixes.custom_arg}:custom_arg_1': 'custom_arg_value_1',
        f'{Prefixes.request_arg}:request_arg_1': 'request_arg_value_1',
    }
    params = {
        'base_url': 'ipinfo.io',
        'header:authorization:bearer': 'my_secret_key',
        'context_key': 'ipinfo.ip'
    }
    p = Parser(params=params, args=args)
    assert p.suffix == 'ip'
    assert p.method == 'GET'
    assert p.headers == {'bearer': 'my_secret_key'}
    expected_url_args = {'url_arg_1': 'url_arg_value_1'}
    expected_custom_args = {'custom_arg_1': 'custom_arg_value_1'}
    expected_body_args = {'body_arg_1': 'body_arg_value_1'}
    expected_request_args = {'request_arg_1': 'request_arg_value_1'}
    assert p.parsed_arguments == CommandArguments(url_args=expected_url_args, custom_args=expected_custom_args,
                                                  request_args=expected_request_args, body_args=expected_body_args)
    assert p._pre_process_code == DEFAULT_PRE_PROCESS
    assert p._post_process_code == DEFAULT_POST_PROCESS
    assert p.context_key == 'context_key'
