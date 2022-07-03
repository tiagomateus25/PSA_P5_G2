#!/usr/bin/python3
from colorama import Fore, Back, Style
from key import key
from xbox import xbox
from pid import pid
from escs_calibration import calibration


def instructions():

    print(Back.MAGENTA + 'Instructions:' + Style.RESET_ALL + '\n')
    print('If you chose the ' + Back.MAGENTA + 'key' + Style.RESET_ALL + ' option: \n ')
    print('Press ' + Fore.YELLOW + 'a' + Style.RESET_ALL + ' to go left.')
    print('Press ' + Fore.YELLOW + 'd' + Style.RESET_ALL + ' to go right.')
    print('Press ' + Fore.YELLOW + 'w' + Style.RESET_ALL + ' to go in front.')
    print('Press ' + Fore.YELLOW + 's' + Style.RESET_ALL + ' to go back.')
    print('Press ' + Fore.YELLOW + 'spacebar' + Style.RESET_ALL + ' to go up.')
    print('Press ' + Fore.YELLOW + 'c' + Style.RESET_ALL + ' to go down.')
    print('Press ' + Fore.YELLOW + 'r' + Style.RESET_ALL + ' to stabilize.\n')
    print('If you chose the ' + Back.MAGENTA + 'xbox' + Style.RESET_ALL + ' option: \n')
    print('Use the ' + Fore.YELLOW + 'joystick' + Style.RESET_ALL + ' to control the drone: \n')
    print('Tilt the ' + Fore.YELLOW + 'joystick left' + Style.RESET_ALL + ' to go left.')
    print('Tilt the ' + Fore.YELLOW + 'joystick right' + Style.RESET_ALL + ' to go right.')
    print('Tilt the ' + Fore.YELLOW + 'joystick front' + Style.RESET_ALL + ' to go front.')
    print('Tilt the ' + Fore.YELLOW + 'joystick back' + Style.RESET_ALL + ' to go back.')
    print('Press ' + Fore.YELLOW + 'RT' + Style.RESET_ALL + ' to go up.')
    print('Press ' + Fore.YELLOW + 'LT' + Style.RESET_ALL + ' to go down. \n')

    inp = input()
    if inp == 'calibration':
        print('\n')
        calibration()
    if inp == 'instructions':
        print('\n')
        instructions()
    if inp == 'key':
        print('\n')
        key()
    if inp == 'xbox':
        print('\n')
        xbox()
    if inp == 'pid':
        print('\n')
        pid()


def main():
    print(Back.MAGENTA + '<--------------------Welcome to the Pydrone alpha version!--------'
                         '------------>' + Style.RESET_ALL + '\n')
    print(Back.MAGENTA + 'List of commands:' + Style.RESET_ALL + '\n')
    print('Type ' + Fore.RED + 'instructions' + Style.RESET_ALL + ' in the terminal '
                                                                  'and press Enter for the instructions list.')
    print('Type ' + Fore.RED + 'calibration' + Style.RESET_ALL + ' in the terminal '
                                                                 'and press Enter for the calibration of the ESCs.')
    print('Type ' + Fore.RED + 'key' + Style.RESET_ALL + ' to control the drone with the keyboard, after '
                                                         'calibration is complete.')
    print('Type ' + Fore.RED + 'xbox' + Style.RESET_ALL + ' to control the drone with the xbox controller, after '
                                                          'calibration is complete. \n')
    print('Type ' + Fore.RED + 'keypid' + Style.RESET_ALL + ' to control the drone with the keyboard + pid, after '
                                                            'calibration is complete. \n')
    print('Type ' + Fore.RED + 'xboxpid' + Style.RESET_ALL + ' to control the drone with the xbox controller + pid, '
                                                             'after calibration is complete. \n')
    print('Press ' + Fore.RED + 'Ctrl-C' + Style.RESET_ALL + ' to quit.\n')
    print(Back.MAGENTA + 'Suggestions:' + Style.RESET_ALL + '\n')
    print('Start off with the ' + Fore.RED + 'calibration' + Style.RESET_ALL + ' command if this is '
                                                                               'your first time flying Pydrone. \n')
    print('Learn how to control the drone with the ' + Fore.RED + 'instructions' + Style.RESET_ALL + ' command. \n')

    inp = input()
    if inp == 'calibration':
        print('\n')
        calibration()
    if inp == 'instructions':
        print('\n')
        instructions()
    if inp == 'key':
        print('\n')
        key()
    if inp == 'xbox':
        print('\n')
        xbox()
    if inp == 'pid':
        print('\n')
        pid()


if __name__ == "__main__":
    main()
