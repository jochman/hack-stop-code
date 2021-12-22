from pathlib import Path

import pytest

import demistomock as demisto
from Parser import (DEFAULT_POST_PROCESS, DEFAULT_PRE_PROCESS,
                    ParsedArguments, Parser, Prefixes)
from hack_stop_code.caller.runner import Runner
from utils import Constants


class TestParser:
    def test_sanity(self):
        args = {
            'ip': '1.1.1.1',
            Constants.pre_process: None,
            Constants.post_process: None,
            Constants.method: 'GET',
            Constants.suffix: ':ip',
            Constants.context_key: 'context_key',
            f'{Prefixes.header}:accept': 'json/application',
            f'{Prefixes.body_arg}:body_arg_1': 'body_arg_value_1',
            f'{Prefixes.path_param}:url_arg_1': 'url_arg_value_1',
            f'{Prefixes.custom_arg}:custom_arg_1': 'custom_arg_value_1',
            f'{Prefixes.request_arg}:request_arg_1': 'request_arg_value_1',
        }
        params = {
            'base_url': 'ipinfo.io',
            'context_key': 'ipinfo.ip',
            'credentials': {'password': 'my_secret_key'},
            Constants.authentication_type: Constants.auth_bearer,
        }
        p = Parser(params=params, args=args)
        assert p.suffix == ':ip'
        assert p.method == 'GET'
        assert p.headers == {Constants.auth_header_key: 'Bearer my_secret_key', 'accept': 'json/application'}
        expected_url_args = {'url_arg_1': 'url_arg_value_1'}
        expected_custom_args = {'custom_arg_1': 'custom_arg_value_1'}
        expected_body_args = {'body_arg_1': 'body_arg_value_1'}
        expected_request_args = {'request_arg_1': 'request_arg_value_1'}
        assert p._parsed_arguments == ParsedArguments(url_args=expected_url_args, custom_args=expected_custom_args,
                                                      request_args=expected_request_args, body_args=expected_body_args)
        assert p._pre_process_code == DEFAULT_PRE_PROCESS
        assert p._post_process_code == DEFAULT_POST_PROCESS
        assert p.context_key == 'context_key'

    def test_custom_authentication(self):
        args = {}
        password = 'best password'
        username = 'awesome user'
        params = {
            'credentials': {'username': username, 'password': password},
            Constants.authentication_type: Constants.auth_custom,
            Constants.auth_format: f'my username is :username and my password is :password'
        }
        p = Parser(params=params, args=args)
        assert p.headers == {Constants.auth_header_key: f'my username is {username} and my password is {password}'}
        assert p._pre_process_code == DEFAULT_PRE_PROCESS
        assert p._post_process_code == DEFAULT_POST_PROCESS

    def test_sanity(self):
        args = {
            Constants.pre_process: None,
            Constants.post_process: None,
            Constants.method: 'GET',
            Constants.suffix: ':ip',
            Constants.context_key: 'context_key',
            f'{Prefixes.header}:accept': 'json/application',
            f'{Prefixes.body_arg}:body_arg_1': 'body_arg_value_1',
            f'{Prefixes.path_param}:ip': '1.1.1.1',
            f'{Prefixes.custom_arg}:custom_arg_1': 'custom_arg_value_1',
            f'{Prefixes.request_arg}:request_arg_1': 'request_arg_value_1',
        }
        params = {
            'base_url': 'ipinfo.io',
            'context_key': 'ipinfo.ip',
            'credentials': {'password': 'my_secret_key'},
            Constants.authentication_type: Constants.auth_bearer,
        }
        p = Parser(params=params, args=args)
        assert p.suffix == '1.1.1.1'
        assert p.method == 'GET'
        assert p.headers == {Constants.auth_header_key: 'Bearer my_secret_key', 'accept': 'json/application'}
        expected_path_args = {'ip': '1.1.1.1'}
        expected_custom_args = {'custom_arg_1': 'custom_arg_value_1'}
        expected_body_args = {'body_arg_1': 'body_arg_value_1'}
        expected_request_args = {'request_arg_1': 'request_arg_value_1'}
        assert p._parsed_arguments == ParsedArguments(path_args=expected_path_args, custom_args=expected_custom_args,
                                                      request_args=expected_request_args, body_args=expected_body_args)
        assert p._pre_process_code == DEFAULT_PRE_PROCESS
        assert p._post_process_code == DEFAULT_POST_PROCESS
        assert p.context_key == 'context_key'
        # try to instantiate
        assert p.pre_processor
        assert p.post_processor

    def test_basic_authentication(self):
        args = {}
        password = 'best password'
        username = 'awesome user'
        params = {
            'credentials': {'username': username, 'password': password},
            Constants.authentication_type: Constants.auth_basic,
        }
        p = Parser(params=params, args=args)
        assert p.headers == {Constants.auth_header_key: f'Basic {username}:{password}'}
        assert p._pre_process_code == DEFAULT_PRE_PROCESS
        assert p._post_process_code == DEFAULT_POST_PROCESS

    def test_none_authentication(self):
        args = {}
        params = {Constants.authentication_type: Constants.auth_none}
        p = Parser(params=params, args=args)
        assert p.headers == {}

    @pytest.mark.parametrize('auth_type', (Constants.auth_none, Constants.auth_basic, Constants.auth_bearer))
    def test_empty_custom_raises(self, auth_type: str):
        args = {}
        params = {
            Constants.auth_format: 'not empty',
            Constants.authentication_type: auth_type,
        }
        with pytest.raises(ValueError):
            Parser(params=params, args=args)

    def test_none_authentication_missing_format(self):
        args = {}
        params = {
            Constants.auth_format: '',
            Constants.authentication_type: Constants.auth_custom,
        }
        with pytest.raises(ValueError):
            Parser(params=params, args=args)

    def test_pre_process(self, capsys):
        pre_string_to_print = 1
        post_string_to_print = 2
        pre_code = f'print({pre_string_to_print})'
        post_code = f'print({post_string_to_print})'
        args = {Constants.pre_process: pre_code,
                Constants.post_process: post_code}
        params = {
        }
        p = Parser(params=params, args=args)
        out, err = capsys.readouterr()
        assert out == f'{pre_string_to_print}\n{post_string_to_print}\n'
        assert p._pre_process_code == pre_code
        assert p._post_process_code == post_code


class TestAll:
    def test_sanity(self, mocker, requests_mock):
        args = {
            Constants.method: 'GET',
            Constants.suffix: ':ip',
            Constants.pre_process: Path('ipinfo/preprocess_ipinfo.py').read_text(),
            Constants.context_key: 'ipinfo.ip',
            f'{Prefixes.header}:accept': 'json/application',
            f'{Prefixes.path_param}:ip': '1.1.1.1',
        }
        params = {
            'base_url': 'https://ipinfo.io',
            'context_key': 'ipinfo.ip',
            'credentials': {'password': 'my_secret_key'},
            Constants.authentication_type: Constants.auth_bearer,
        }
        mocker.patch.object(demisto, 'params', return_value=params)
        mocker.patch.object(demisto, 'args', return_value=args)

        mocked_request = requests_mock.get('https://ipinfo.io/1.1.1.1', json={'works': 'well'})

        runner = Runner()
        response = runner.run()
        assert response.outputs == {'works': 'well'}
        assert response.to_context() == {'Type': 1, 'ContentsFormat': 'json', 'Contents': {'works': 'well'},
                                         'HumanReadable': '### Results\n|works|\n|---|\n| well |\n',
                                         'EntryContext': {'demo/': {'works': 'well'}}, 'IndicatorTimeline': [],
                                         'IgnoreAutoExtract': False, 'Note': False, 'Relationships': []}
        assert mocked_request.call_count == 1
        assert runner.parser._parsed_arguments.custom_args == {'preprocess': 'has been run'}
