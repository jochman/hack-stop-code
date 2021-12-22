from pathlib import Path

parser = Path('caller/Parser.py')
runner = Path('caller/runner.py')
pre_process = Path('caller/pre_process.py')
post_process = Path('caller/post_process.py')
api_call = Path('caller/api_call.py')
csp = Path('caller/CommonServerPython.py')

result = "\n".join(file.read_text() for file in (parser, runner, pre_process, post_process, api_call, csp))
Path('unified.txt').write_text(result)