'''
    Python Version:     3.7.2
    Author:             Skyler Knecht
    Description:        Python script that simulates a deterministic pushdown automaton (DPDA).
                        Accpeting input (e.g., aabbaa), the program will compute whether the provided
                        input is Accepted or Rejected.
'''

import sys

def setup_config():
    pass


def main(argv):
    if len(sys.argv) < 2:
        usage_string = f'usage: python {argv[0]} /location/of/configuration/files'
        print(usage_string)
    else:
        setup_config()


if __name__ == '__main__':
    main(sys.argv)
