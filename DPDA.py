'''
    Python Version:     3.7.2
    Author:             Skyler Knecht
    Description:        Python script that simulates a deterministic pushdown automaton (DPDA).
                        Accpeting input (e.g., aabbaa) and speicific configuration files, the program
                        will compute whether the provided input is Accepted or Rejected.

    Variable Descriptions: (Q, Sigma, Gamma, Delta, S, I, F)
            * Q         Largest state subscript.
            * Sigma     A finite set of input symbols.
            * Gamma     A finite stack alphabet.
            * Delta     The transition functions.
            * S         The start state.
            * I         The initial contents of the stack.
            * F         The final state.
'''

import sys

# Configuration Variables
config = dict.fromkeys(['Q', 'Sigma', 'Gamma', 'Delta', 'S', 'I', 'F'], None)

def dpda_simulator():
    my_input = input()

    for x in my_input:
        if (not my_input[x] in config['Sigma']):
            print('Error')

def setup_config(config_location):
    global config

    with open(f'{config_location}Q.conf') as f:
        config['Q'] = f.read(1)

    with open(f'{config_location}Sigma.conf') as f:
        config['Sigma'] = f.read()

    with open(f'{config_location}Gamma.conf') as f:
        config['Gamma'] = f.read()

    with open(f'{config_location}Delta.conf') as f:
        config['Delta'] = f.read()

    with open(f'{config_location}F.conf') as f:
        config['F'] = f.read()

    dpda_simulator()

def main(argv):
    if len(sys.argv) < 2:
        usage_string = f'usage: python {argv[0]} /location/of/configuration/files/'
        print(usage_string)
    else:
        setup_config(argv[1])

if __name__ == '__main__':
    main(sys.argv)
