'''
    Python Version:     3.7.2
    Author:             Adrian Vasu
    Description:        This program is written tos imulate a detemrinistic pushdown
                        automaton/accepter. This program was written as a part of
                        CSC 450 at the University of Mount Union during which the
                        student was enrolled in the Spring 2019 semester. The
                        dpda_simulator acccepts an input string comprised of chars
                        in the alphabet (e.g. aaabbb) and the location of a folder
                        with specific configuration files (see below) to simulate
                        the DPDA. The program then determines whether the provided
                        input string is Accepted or Rejected based on the other files.

    DPDA File Configuration Description:
            * Q.conf        Largest integer index for elements in set Q
                            one integer corresponding to the largest state
                            possible
            * Sigma.conf    A finite input alphabet (all unicode)
                            letters should not be seperated at all
            * Gamma.conf    A finite stack alphabet (all unicode).
                            letters/numbers sould not be seperated
                            at all
            * Delta.conf    The transition functions.
                            each function should be on a newline
                            each state and instantaneous description should
                            be seperated by a space
            * F.conf        The set of possible final states
                            seperated by commas

    DPDA Septuple Description: (Q, Sigma, Gamma, Delta, S, I, F)
            * Q         Largest integer index for elements in set Q.
            * Sigma     A finite input alphabet (all unicode).
            * Gamma     A finite stack alphabet (all unicode).
            * Delta     The transition functions.
            * S         The initial start state.
            * I         The initial stack contents.
            * F         The set of possible final states.

    Original project description: https://github.com/csc220-mountunion/CSC450assignment

    Assigned by Dr. Ken Weber: March 1st, 2019
    Completed by Adrian Vasu:  April 17th, 2019
'''

import sys      # Used to take advantage of stdin and stdout
import time     # Used to step through program slower

# Configuration Variables
config = dict.fromkeys(['Q', 'Sigma', 'Gamma', 'Delta', 'S', 'I', 'F'], None)   # utilized to hold configuration file contents
stackContents = None                                                            # utilized to pass stack contents through various methods
curState = None                                                                 # utilized to pass state contents through various methods

def dpda_simulator():   # simulator method utilizes conf files and input to simulate dpda
    my_input = input()  # pull input from stdin

    global stackContents
    global curState

    for x in range(0, len(my_input)):   # Looping through the input
        if (not my_input[x] in config['Sigma']):
            print('String Rejected: Invalid Alphabet Character') # Check to make sure all characters in input are in alphabet
            break
        else:
            if (x == 0):                # initialize variables if it is first input char
                currentState = [my_input[x+1], config['I'], config['S']]
                print(f'Current Character: {currentState[0]}, Current Stack Contents: {currentState[1]}, Current State: {currentState[2]}')
                if (not transition(currentState)):
                    print('String Rejected: No more Transitions')
                    break
            else:                       # loop over remaining chars utilizing transition statments
                if ((x + 1) == len(my_input) and curState in config['F']):
                    print('\nString Accepted\n')
                    break
                if (x + 1 >= len(my_input)): #need lambda transition
                    if (stackContents == ''):
                        stackContents = str(0)
                    currentState = [None, stackContents, curState]
                else:
                    if (stackContents == ''):
                        stackContents = str(0)
                    currentState = [my_input[x+1], stackContents, curState]
                print(f'Current Character: {currentState[0]}, Current Stack Contents: {currentState[1]}, Current State: {currentState[2]}')
                if (not transition(currentState)):
                    print('String Rejected: No more Transitions')
                    break

        if ((x + 1) == len(my_input) and curState in config['F']):
            print('\nString Accepted\n')
            break

        time.sleep(1)

def transition(currentState):
    cs = currentState[2]
    cc = currentState[0]
    ts = currentState[1][0]
    foundTransition = False
    global stackContents
    global curState

    #print(cc, ts, cs)

    for x in range(0, len(config['Delta'])):
        if (config['Delta'][x][2] == cc and config['Delta'][x][4] == ts and config['Delta'][x][0] == cs):
            print('Found Match')
            if (config['Delta'][x][8:].rstrip() == ''):
                stackContents = stackContents[1:]
            else:
                if (not stackContents == None):
                    stackContents = config['Delta'][x][8:].rstrip()
                else:
                    stackContents = config['Delta'][x][8:].rstrip()
            curState = config['Delta'][x][6]
            foundTransition = True
            return True
            break

    if (not foundTransition):
        for x in range(0, len(config['Delta'])):
            if (config['Delta'][x][0] == 'L' and config['Delta'][x][2] == cs and config['Delta'][x][4] == ts):
                print('Matched Lambda')
                if (not stackContents == None):
                    stackContents = config['Delta'][x][8:].rstrip() + stackContents
                else:
                    stackContents = config['Delta'][x][8:].rstrip()
                curState = config['Delta'][x][6]
                return True

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

    dpda_simulator()

def main(argv):
    if (len(sys.argv) < 2):
        usage_string = f'usage: python {argv[0]} /location/of/configuration/files/'
        print(usage_string)
    else:
        if (not argv[1][len(argv[1])-1] == '/'):
            setup_config(argv[1] + '/')
        else:
            setup_config(argv[1])

if (__name__ == '__main__'):
    main(sys.argv)
