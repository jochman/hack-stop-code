from . import PreProcess, PostProcess, ApiCall, Runner
from pathlib import Path
import json
import typer

def main(
    args_path: Path = typer.Argument(..., file_okay=True, resolve_path=True, readable=True), 
    params_path: Path = typer.Argument(..., file_okay=True, resolve_path=True, readable=True)
    ):
    with open(args_path) as f:
        args = json.load(f)
    with open(params_path) as f:
        params = json.load(f)
    pre_process = PreProcess(args)
    api_call = ApiCall(**params)
    post_process = PostProcess()
    runner = Runner(pre_process, api_call, post_process)
    print(runner.run(args))

if __name__ == '__main__':
    typer.run(main)