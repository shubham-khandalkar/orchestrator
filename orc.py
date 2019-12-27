"""
    This program orchestrates various programs to be called from a simple orc
    command. Keep this file in a folder and add that folder to PATH variable.
    If you want single word call create a cmd/batch file at the folder, name
    it orc.cmd and save the following content in it:
        @echo off
        python -m orc %*
"""
import sys
import os
import time
import pickle

DATA_FILE_LOCATION = ''
PROGRAMS_LIST = {}


class Redirection:
    """
        This class is used to save the scripts data. More readable than
        creating a dictionary
    """
    def __init__(self):
        self.name = None
        self.type = None
        self.directory = None
        self.command = None


def read():
    """
        Reads the saved scripts data from data file
    """
    global PROGRAMS_LIST
    if os.path.isfile(DATA_FILE_LOCATION):
        with open(DATA_FILE_LOCATION, 'rb') as data_file:
            try:
                PROGRAMS_LIST = pickle.load(data_file)
            except Exception:
                PROGRAMS_LIST = {}
                data_file.close()
                os.remove(DATA_FILE_LOCATION)
            if not isinstance(PROGRAMS_LIST, dict):
                PROGRAMS_LIST = {}
                data_file.close()
                os.remove(DATA_FILE_LOCATION)
    else:
        PROGRAMS_LIST = {}


def save():
    """
        Saves the scripts data into data file
    """
    global PROGRAMS_LIST
    if os.path.isfile(DATA_FILE_LOCATION):
        os.remove(DATA_FILE_LOCATION)
    pickle.dump(PROGRAMS_LIST, open(DATA_FILE_LOCATION, 'wb+'))


def add(program_name, location, script_type='python'):
    """
        Adds script data to the dictionary
    """
    global PROGRAMS_LIST
    red = Redirection()
    red.type = script_type
    if script_type == 'python':
        if program_name[-3:] == ".py":
            red.command = program_name
            program_name = program_name[:-3]
        else:
            red.command = program_name + ".py"
        red.name = program_name
        if "\\" + command != location[-len(command) - 1:]:
            red.directory = os.path.abspath(location)
        else:
            red.directory = location[:-location[::-1].index("\\")]
    else:
        red.type = script_type
        red.directory = location
        red.name = program_name
        if red.type == 'directory':
            red.command = ''
        else:
            red.command = program_name
    PROGRAMS_LIST[program_name] = red
    save()


def timewrapped(arg, timer=False):
    """
        Prints the time taken to run the script
    """
    t_start = time.time()
    os.system(arg)
    if timer:
        print('total time taken: ' + str(time.time() - t_start) + " secs")


def run(program_name, args='', timer=False):
    """
        Runs the script
    """
    red = PROGRAMS_LIST.get(program_name)
    if red is None:
        print('No script found')
        exit()
    if red.type == 'python':
        print('executing command: ' + "python " +
              os.path.join(red.directory, red.command) + ' ' + args)
        timewrapped("python " + os.path.join(red.directory, red.command) +
                    ' ' + args, timer)
    else:
        if red.type == 'directory':
            print('executing command: ' + red.directory + "\\" + args)
            timewrapped(red.directory + "\\" + args, timer)
        else:
            print('executing command: ' + red.directory + "\\" + red.command +
                  " " + args)
            timewrapped(red.directory + "\\" + red.command + " " + args, timer)


def orc_list():
    """
        Lists all the scripts saved
    """
    for prog in PROGRAMS_LIST:
        print('{}:\t{} {} {}'.
              format(prog, PROGRAMS_LIST[prog].type, PROGRAMS_LIST[prog]
                     .directory, PROGRAMS_LIST[prog].command))


def clean(forced=False):
    """
        Deletes saved scipts
    """
    inp = ''
    if not forced:
        print('are you sure (y/n)? ', end='')
        inp = input()
    if forced or inp.upper() == 'Y' or inp.upper() == 'YES':
        if os.path.isfile(DATA_FILE_LOCATION):
            os.remove(DATA_FILE_LOCATION)


def orc_help(command=None):
    """
        Help description for the orcestration script
    """
    if command is None or command == '':
        print()
        print('Usage: python orc.py COMMAND')
        print()
        print('Commands:')
        print('  run\tRuns the script if saved')
        print('  ls\tLists all saved scripts')
        print('  add\tAdds script to saved list')
        print()
        print("Run 'python orc.py COMMAND --help' for more information on a" +
              " command.")
        print()
    elif command == 'run':
        print()
        print('Usage: python orc.py [run] [options] SCRIPT_NAME')
        print()
        print('Runs the script if saved. The run command itself is optional')
        print()
        print('Options:')
        print('  -t\tPrints time taken to run the script')
        print()
    elif command == 'ls':
        print()
        print('Usage: python orc.py ls')
        print()
        print('Lists all saved scripts')
        print()
    elif command == 'add':
        print()
        print('Usage: python orc.py add [options] SCRIPT_NAME [SCRIPT_LOCATI' +
              'ON]')
        print()
        print('Adds script to saved list. If no script location is provided ' +
              'current working directory will be saved. By default all scrip' +
              't are assumed python scripts. Use options to modify script ty' +
              'pe')
        print()
        print('Options:')
        print('  -d\t\tChanges the script type to directory')
        print('  --non-python\tChanges the script type to any executable')
        print()
    exit()


if __name__ == '__main__':
    DATA_FILE_LOCATION = sys.argv[0]
    if '\\' in DATA_FILE_LOCATION:
        DATA_FILE_LOCATION = DATA_FILE_LOCATION[:-DATA_FILE_LOCATION[::-1]
                                                .index("\\")]
    else:
        DATA_FILE_LOCATION = os.getcwd()
    DATA_FILE_LOCATION = os.path.join(DATA_FILE_LOCATION, "orc_data.dat")
    read()
    args = sys.argv[1:]
    if not args:
        print('invalid entry')
        exit()

    command = args[0]
    args = args[1:]
    if command not in ('add', 'ls', 'clean', '--help'):
        timer = False
        if command == 'run':
            if not args:
                print('invalid entry ' + str(sys.argv[1:]))
                exit()
            if args[0] == '--help':
                orc_help('run')
            if args[0] == '-t':
                if len(args) == 1:
                    print('invalid entry ' + str(sys.argv[1:]))
                    exit()
                args = args[1:]
                timer = True
            program_name = args[0]
            args = args[1:]
        else:
            if args and command == '-t':
                timer = True
                program_name = args[0]
            else:
                program_name = command
        run(program_name, ' '.join(args), timer)
    else:
        if command == 'add':
            script_type = 'python'
            if args[0] == '--help':
                orc_help('add')
            directory = False
            if args[0] == '--non-python' or \
               (len(args) > 1 and args[1] == '--non-python'):
                script_type = 'other'
                args = args[1:]
            if args[0] == '-d' or (len(args) > 1 and args[1] == '-d'):
                script_type = 'directory'
                args = args[1:]
            if len(args) == 1:
                add(args[0], os.getcwd(), script_type)
            elif len(args) == 2:
                add(args[0], args[1], script_type)
            else:
                print('invalid entry ' + str(sys.argv[1:]))
        elif command == 'ls':
            if args and args[0] == '--help':
                orc_help('ls')
            orc_list()
        elif command == 'clean':
            if len(args) == 1:
                if args[0] == '-f':
                    clean(True)
                    exit()
            clean(False)
        elif command == '--help':
            orc_help('')
