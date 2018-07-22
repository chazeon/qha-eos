import argparse

from .app import QHAEOSCommandHandler

def main():
    parser = argparse.ArgumentParser()
    handler = QHAEOSCommandHandler()
    handler.init_parser(parser)
    namespace = parser.parse_args()
    handler.run(namespace)

if __name__ == '__main__':
    main()