import sys
import code
import Symbol_table


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


def is_const(char):
    try:
        int(char)
        return True
    except ValueError:
        return False


def first_pass(file_name: str, tb: Symbol_table):
    # record
    line_num = 0
    for line in read_file(file_name):
        l = line.strip()
        if is_useless(l):
            # comments or blank line
            continue

        t = command_type(l)
        if t == 'L':
            # '(ADSDA)' -> 'ADSDA'
            content = l[1:-1]
            tb.add_entry(content, line_num)
        else:
            # A or C
            line_num += 1


def second_pass(file_name: str, tb: Symbol_table, dest_file):
    f = dest_file

    for line in read_file(file_name):
        l = line.strip()
        if is_useless(l):
            # comments or blank line
            continue

        # clear Inline Comments!
        # 'M=D  // M[2] = D (greatest number)' -> 'M=D'
        l = l.split('//')[0].strip()

        t = command_type(l)
        if t == 'A':
            # '@ABC' -> 'ABC'
            # '@123' -> '123'
            content = l[1:]
            if is_const(content[0]):
                # is a num
                const = int(content)
            else:
                # is a symbol
                if not tb.contains(content):
                    # first used variable
                    tb.add_entry(content)
                # then get it.
                const = tb.get_address(content)
            # convert int to string of 16bits binary-num.
            c = f'{const:016b}'
            print('A_COMMAND:', c)
        elif t == 'C':
            # dest, comp, jump = c_parts(l)
            c = code(c_parts(l))
            print('C_COMMAND:', c)
        elif t == 'L':
            # do nothing
            continue
        # write one code
        f.write(c + '\n')


def parser(file_name):
    # first pass for adding label infos to the symbol table.
    tb = Symbol_table()
    first_pass(file_name, tb)

    # open dest file.
    d = dest_file(file_name)
    print('destination:', d)
    with open(d, 'w+') as f:
        # then make the perfect!
        second_pass(file_name, tb, f)


sys.modules[__name__] = parser
