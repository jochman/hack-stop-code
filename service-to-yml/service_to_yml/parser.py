from schema import WebSchema, Demisto
import re


class Parser:
    command_headers = {'params', 'headers'}

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
        for param in re.findall(suffix, r':[^/]+') or []:
            params.append(
                Demisto.Argument(
                    name=f'_path_param:{param.rstrip(":")}',
                    defaultValue='',
                    hidden=False,
                    required=True
                )
            )
        return params

    def _parse_configuration(
        self, oldparams: list[WebSchema.Param], prefix: str
    ):
        params: list[Demisto.Configuration] = []
        params.extend(
            [
                self._parse_single_configuration(param, prefix)
                for param in oldparams
            ]
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
                ]
            )
            for header in self.command_headers:
                params = [WebSchema.Param(**param)
                          for param in command.dict()[header]]

                arguments.extend(
                    [
                        Demisto.Argument(
                            name=f'{header}:{argument.key}',
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
                .replace(':', ''),
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
                self.integration.configuration.headers, 'headers'
            ),
        )
        return integration
