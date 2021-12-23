from CommonServerPython import return_results
import demistomock as demisto  # todo remove
from hack_stop_code.caller.runner import Runner


def main():
    runner = Runner(params=demisto.params(), args=demisto.args())
    results = runner.run()
    return_results(results)


if __name__ == '__main__':
    main()
