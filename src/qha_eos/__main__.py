import argparse

from .app import QHAEOSProgram

def main():
    parser = argparse.ArgumentParser()
    program = QHAEOSProgram()
    program.init_parser(parser)
    namespace = parser.parse_args()
    program.run(namespace)

if __name__ == '__main__':
    main()