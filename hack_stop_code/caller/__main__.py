# todo jochman fix all imports
from CommonServerPython import return_results
from hack_stop_code.caller.runner import Runner


def main():
    runner = Runner()
    results = runner.run()
    return_results(results)


if __name__ == '__main__':
    main()
