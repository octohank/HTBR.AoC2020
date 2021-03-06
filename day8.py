import stdfuns
import re

def parse_statement(str):
    m = re.match(r'(nop|acc|jmp) ([\+\-]\d+)', str)
    return (m.group(1), m.group(2), 0)

run_cmd = {
    'nop': lambda x, i, accu: (i + 1, accu),
    'acc': lambda x, i, accu: (i + 1, accu + int(x)),
    'jmp': lambda x, i, accu: (i + int(x), accu)
}

def calc_accumulator(i, exec_table, accumulator):
    statement = exec_table[i]
    cmd = statement[0]
    val = statement[1]

    res = run_cmd[cmd](val, i, accumulator)
    exec_table[i] = (statement[0], statement[1], statement[2] + 1)

    # if next command is EOF, return
    if(len(exec_table) == res[0]):
        return (res[1], True)
 
    if(exec_table[res[0]][2] > 0):
        return (res[1], False)

    return calc_accumulator(res[0], exec_table, res[1])

data = stdfuns.open_file_split('day8.txt')

exec_table = [parse_statement(statement) for statement in data]

print('part 1:', calc_accumulator(0, exec_table, 0)[0])

# reset exec_table
exec_table = [parse_statement(statement) for statement in data]

flip = {
    'nop': lambda row: ('jmp', row[1], row[2]),
    'jmp': lambda row: ('nop', row[1], row[2])
}

vals = [(i, val[0]) for i, val in enumerate(exec_table) if val[0] == 'nop' or val[0] == 'jmp']
for i, val in vals:
    exec_copy = exec_table.copy()

    exec_copy[i] = flip[val](exec_copy[i])

    res = calc_accumulator(0, exec_copy, 0)
    if(res[1]):
        print('part 2:', res[0])
