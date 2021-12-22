class PreProcess:
    def __init__(self, args: ParsedArguments) -> None:
        self._args = args

    def get_preprocessed_args(self):
        # If necessary, change self._args
        # (the ParsedArguments object is immutable, but its members are mutable)
        return self._args
