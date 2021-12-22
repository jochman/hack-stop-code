from typing_extensions import Required
from schema import WebSchema, Demisto
import logging
import re

logger = logging.getLogger('')


class Parser:
    header_to_yml = {
        'params': '_request_arg',
        'headers': '_header'
    }

    def __init__(self, integration: WebSchema.Integration):
        self.integration = integration

    def _parse_single_configuration(self, param: WebSchema.Param, prefix=''):
        return Demisto.Configuration(
            display=param.key,
            name=f'{prefix}:{param.key}' if prefix else param.key,
            defaultvalue=param.value,
            required=param.required,
            hidden=param.required,
        )

    def _parse_path_params(self, cmd: WebSchema.Command):
        suffix = cmd.suffix
        params = []
        for param in re.findall(r':[^/]+', suffix):
            params.append(
                Demisto.Argument(
                    name=f'_path_param:{param.strip(":")}',
                    defaultValue='',
                    hidden=False,
                    required=True
                )
            )
        return params

    def _parse_conf_per_header(self, oldparams: list[WebSchema.Param], prefix: str):
        params: list[Demisto.Configuration] = []
        params.extend(
            [
                self._parse_single_configuration(param, prefix)
                for param in oldparams
            ]
        )
        return params

    def _parse_configuration(
        self, conf: WebSchema.Configuration
    ):
        params: list[Demisto.Configuration] = list()
        print(conf.base_url)
        params.extend(
            [
                Demisto.Configuration(
                name='base_url',
                display='Base URL',
                defaultvalue=conf.base_url,
                hidden=False,
                required=True
            ),
                Demisto.Configuration(
                name='context_key',
                display='Context Key',
                defaultvalue=conf.context_key,
                hidden=False,
                required=True
            ),
            Demisto.Configuration(
                name='insecure',
                display='Insecure',
                defaultvalue=conf.insecure if conf.insecure else False,
                hidden=False,
                required=False,
                type=8
            ),
            Demisto.Configuration(
                name='proxy',
                display='Use proxy',
                defaultvalue=conf.proxy if conf.proxy else False,
                hidden=False,
                required=False,
                type=8
            )
            ]
        )
        params.extend(
            self._parse_conf_per_header(conf.headers, '_header')
        )
        return params

    def _parse_commands(self):
        commands = self.integration.commands
        new_commands: list[Demisto.Command] = list()
        for command in commands:
            arguments = list()
            arguments.extend(
                [
                    Demisto.Argument(
                        name='method', defaultValue=command.method, hidden=True
                    ),
                    Demisto.Argument(
                        name='suffix', defaultValue=command.suffix, hidden=True
                    ),
                    Demisto.Argument(
                        name='_pre_process', defaultValue=command.pre_process, hidden=True
                    ),
                    Demisto.Argument(
                        name='_post_process', defaultValue=command.post_process, hidden=True
                    ),
                ]
            )
            for header, translate in self.header_to_yml.items():
                params = [WebSchema.Param(**param)
                          for param in command.dict()[header]]

                arguments.extend(
                    [
                        Demisto.Argument(
                            name=f'{translate}:{argument.key}',
                            defaultValue=argument.value,
                            hidden=argument.hidden,
                            required=argument.required,
                        )
                        for argument in params
                    ]
                )
            arguments.extend(
                self._parse_path_params(command)
            )
            cmd = Demisto.Command(
                name=f'{self.integration.configuration.name}-{command.method}-{command.suffix}'.lower()
                .replace(' ', '-')
                .replace('/', '-')
                .replace('--', '-')
                .replace(':', '')
                .strip('-'),
                arguments=arguments,
            )
            new_commands.append(cmd)

        return new_commands

    def parse(self) -> Demisto.Integration:

        integration = Demisto.Integration(
            commonfields=Demisto.CommonFields(
                id=self.integration.configuration.name, version=-1
            ),
            display=self.integration.configuration.name,
            name=self.integration.configuration.name,
            category='Endpoint',
            script=Demisto.Script(commands=self._parse_commands()),
            configuration=self._parse_configuration(
                self.integration.configuration
            ),
        )
        return integration
