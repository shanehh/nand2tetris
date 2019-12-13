import sys
import code


def read_file(name):
    with open(name, 'r') as f:
        for l in f:
            yield l


def write_file(name):
    with open(name, 'w+') as f:
        pass


def command_type(line):
    l = line
    # fist char
    print(l)
    ft = l[0]
    if ft == '(':
        # lable
        return 'L'
    elif ft == '@':
        # addressing
        return 'A'
    else:
        # computing
        return 'C'


def c_parts(c_command):
    # r stands for remains

    # dest=comp;jump
    r = c_command.split('=')
    if len(r) == 2:
        dest = r[0].strip()
        r = r[1]
    else:
        dest = None
        r = r[0]

    # comp;jump
    r = r.split(';')
    comp = r[0].strip()
    if len(r) == 2:
        jump = r[1].strip()
    else:
        jump = None
    return dest, comp, jump


def dest_file(file_name):
    """
    "Add.asm" -> "Add.hack"
    """
    naked = file_name.rsplit('.', 1)[0]
    return naked + '.hack'


def is_useless(line):
    l = line
    return l.startswith('//') or l == ''


def parser(file_name):
    # open dest file.
    d = dest_file(file_name)
    print('destination:', d)
    f = open(d, 'w+')

    for line in read_file(file_name):
        l = line.strip()
        if is_useless(l):
            # comments or blank line
            continue

        t = command_type(l)
        if t == 'A':
            # @123 -> 123
            const = int(l[1:])
            # convert int to string of 16bits binary-num.
            c = f'{const:016b}'
            print('A_COMMAND:', c)
        elif t == 'C':
            # dest, comp, jump = c_parts(l)
            c = code(c_parts(l))
            print('C_COMMAND:', c)
        # write one code
        f.write(c + '\n')
    f.close()


sys.modules[__name__] = parser
