# todo jochman fix all imports
from hack_stop_code.caller.Parser import Parser
from hack_stop_code.caller.runner import Runner


def main():
    # Initialization
    parser = Parser(params=demisto.params(), args=demisto.args())
    pre_processor = parser.pre_processor
    post_processor = parser.post_processor

    # Calling
    runner = Runner(pre_processor, post_processor)
    runner.run()

if __name__ == '__main__':
    main()
