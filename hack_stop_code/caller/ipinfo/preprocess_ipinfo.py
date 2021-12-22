from hack_stop_code.caller.Parser import ParsedArguments


class PreProcess:
    def __init__(self, args: ParsedArguments) -> None:
        self._args = args

    def get_preprocessed_args(self):
        self._args.custom_args.update({'preprocess': 'has been run'})
        return self._args
