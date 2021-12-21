from pathlib import Path

import typer

from . import PreProcess, PostProcess, ApiCall, Runner


def main(
        args_path: Path = typer.Argument(..., file_okay=True, resolve_path=True, readable=True),
        params_path: Path = typer.Argument(..., file_okay=True, resolve_path=True, readable=True)
):
    args = load_json(args_path)
    params = load_json(params_path)

    pre_processor = PreProcess(args)
    post_processor = PostProcess()

    api_call = ApiCall(params)
    runner = Runner(pre_processor, api_call, post_processor)
    print(runner.run(args))


if __name__ == '__main__':
    typer.run(main)
