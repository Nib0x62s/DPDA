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
            * Delta     Possible transitions. Structure is: (Current State, Char, Stack, Next State, New Stack)
            * S         The start state.
            * I         The initial contents of the stack.
            * F         The final state.
'''

import sys

# Configuration Variables
config = dict.fromkeys(['Q', 'Sigma', 'Gamma', 'Delta', 'S', 'I', 'F'], None)


def remove_newlines(list):
    '''
    remove_newlines() takes in a list, removes all new lines in every item and returns
    a newly formated list.
    '''
    new_list = []
    for item in list:
        new_list.append(item.rstrip())

    return new_list

def find_transition(current_state, current_character, current_stack):
    '''
    find_transition takes in the properties of the current state of the automaton,
    compares those properties to the list of transitions avaliable in delta and
    based on the comparison find_transition will return a new current_state and
    current_stack for the automaton to change to.
    '''
    print(f'Current State: {current_state}, Current Character: {current_character}, Current Stack: {current_stack}')
    for transition in config['Delta']:
        transition = transition.split(' ')
        if transition[0] == current_state and transition[1] == current_character and transition[2] == current_stack[0]:
            if len(transition) == 5:
                return transition[3], transition[4]
            else:
                return transition[3], current_stack[1:]

    for transition in config['Delta']:
        transition = transition.split(' ')
        if transition[0] == 'L' and transition[1] == current_state and transition[2] == current_stack[0]:
            return transition[3], current_stack[1:]

    return None, '0'


def simulator():
    '''
    simulator() will process user input through a specificed pushdown atomaton structure based on
    configuration files. Through several comparisons and logic the simulator() will output if the
    user supplied input is either accepted or rejected.
    '''
    my_input = input('Enter Input: ')
    current_state = config['S']
    current_stack = config['I']

    for x in range(0, len(my_input)):
        if my_input[x] in config['Sigma']: # Is the current character in our alphabet.
            current_state, current_stack = find_transition(current_state, my_input[x], current_stack) # Set the current_state and curren_stack variables accordingly
            if len(current_stack) == 0: # If the stack is empty, fill it in with a value of 0
                current_stack = '0'
            if current_state == None: # If there is no current state then the string was rejected so break out of the loop
                break
        else:
            return 'Rejected'

        if x + 1 == len(my_input) and current_state in config['F']: # If we're at the end of the string and the current state is a final state then the strin is accepted
            return 'Accepted'

    return 'Rejected'

def setup_config(config_location):
    '''
    setup_config() will define key's specified in a global dictionary called config. The values are pulled
    from files located in the paramater passed through. The key's defined here will be used to specify how
    the pushdown automaton will work.
    '''
    global config

    with open(f'{config_location}Q.conf') as f:
        config['Q'] = f.read(1)

    with open(f'{config_location}Sigma.conf') as f:
        config['Sigma'] = f.readline()

    with open(f'{config_location}Gamma.conf') as f:
        config['Gamma'] = f.readline()

    with open(f'{config_location}delta.conf') as f:
        config['Delta'] = remove_newlines(f.readlines())

    with open(f'{config_location}F.conf') as f:
        config['F'] = remove_newlines(f.readline().split(','))

    config['S'] = '0'

    config['I'] = config['Gamma'][0]

def main(argv):
    '''
    main() will check to see if the arguments passed are sufficient for the program, if not
    main() will print out the usage information on how the program is inteded to run.
    If the arguments are sufficient main() will call various methods to being the pushdown
    automaton process.
    '''
    if len(sys.argv) < 2:
        usage_string = f'usage: python {argv[0]} /location/of/configuration/files'
        print(usage_string)
    else:
        setup_config(argv[1])
        print(simulator())

if __name__ == '__main__':
    main(sys.argv)
