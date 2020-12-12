import os, sys

def ls():
    dirlist = os.listdir()
    for d in dirlist:
        print(d)

def cd(dirname):
    os.chdir(dirname)

def pwd():
    print(os.getcwd())

def print_help():
    print('''Comand line tools written in python''')

def commands(com):
    try:
        if 'help' in com:
            print_help()
        elif 'pwd' in com:
            pwd()
        elif 'cd' in com:
            cd(com[3:])
        elif 'ls' in com:
            ls()
    except:
        print(f'Command error: {sys.exc_info()[0]}')

def main():
    while True:
        entry = input(f'{os.getcwd()}  >>> ');
        if 'exit' in entry:
            break
        else:
            commands(entry)
if __name__ == '__main__':
    main()
