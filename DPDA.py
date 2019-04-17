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
stackContents = None
curState = None

def dpda_simulator():
    my_input = input()

    global stackContents
    global curState

    for x in range(0, len(my_input)):
        if (not my_input[x] in config['Sigma']):
            print('Error input is not in alphabet') # Invalid alphabet character
            break
        else:
            if (x == 0):
                currentState = [my_input[x], config['I'], config['S']]
                print(currentState)
                if (not transition(currentState)):
                    print('Error no more transitions available')
                    break
            else:
                currentState = [my_input[x], stackContents, curState]
                print(currentState)
                if (not transition(currentState)):
                    print('Error no more transitions available')
                    break
        if (x == len(my_input)):
            print('String accepted')
            break

def transition(currentState):
    cs = currentState[2]
    cc = currentState[0]
    ts = currentState[1][len(currentState[1]) - 1]
    foundTransition = False
    global stackContents
    global curState

    print(cc, ts, cs)

    for x in range(0, len(config['Delta'])):
        #print('\n\n', config['Delta'][x][0], config['Delta'][x][2], config['Delta'][x][4])
        if (config['Delta'][x][2] == cc and config['Delta'][x][4] == ts and config['Delta'][x][0] == cs):
            print('found match')
            stackContents = currentState[1] + config['Delta'][x][8:].rstrip()
            curState = config['Delta'][x][6]
            foundTransition = True
            return True
            break
        print('still in for loop')

    if (not foundTransition):
        for x in range(0, len(config['Delta'])):
            if (config['Delta'][x][0] == 'L' and config['Delta'][x][2] == cc and config['Delta'][x][4] == ts):
                stackContents = currentState[1] + config['Delta'][x][8:]
                curState = config['Delta'][x][6]
                return True
            else:
                return False




def setup_config(config_location):
    global config

    with open(f'{config_location}Q.conf') as f:
        config['Q'] = f.read(1)

    with open(f'{config_location}Sigma.conf') as f:
        config['Sigma'] = f.readline()

    with open(f'{config_location}Gamma.conf') as f:
        config['Gamma'] = f.readline()

    with open(f'{config_location}delta.conf') as f:
        config['Delta'] = f.readlines()

    with open(f'{config_location}F.conf') as f:
        config['F'] = f.readline().split(',')

    config['I'] = config['Gamma'][0]

    config['S'] = config['Delta'][0][0]

    #for x in config:
    #    print(config[x])

    dpda_simulator()

def main(argv):
    if len(sys.argv) < 2:
        usage_string = f'usage: python {argv[0]} /location/of/configuration/files/'
        print(usage_string)
    else:
        setup_config(argv[1])

if __name__ == '__main__':
    main(sys.argv)
