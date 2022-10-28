import os


def LimparTela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')