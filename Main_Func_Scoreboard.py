import os
import verilog_functions as methods

t1 = int(input("Enter a val: "))
t2 = int(input("Enter b val: "))
t3 = float(input("Enter Float a: "))
t4 = float(input("Enter Float b: "))

scan = {'a': t1, 'b': t2, 'c': -1, 'fa': t3, 'fb': t4, 'FOH': 143}

x = []  # instruction set

x.append("LDR r1 a")
x.append("LDR r2 b")
x.append("ADD r3 r1 r1")
x.append("ADD r4 r2 r2")
x.append("FADD r12 fa fb")
x.append("STR r12 c")
x.append("FMUL r12 r12 #100")
x.append("ADD r7 r6 b")
x.append("DIV r11 fa b")
x.append("AND r10 #10 #6")
x.append("LDR r5 FOH")
x.append("AND r6 r7 r5")


sub_x = []  # split set
pc = 0


# x.append("MUL r2 a b")
# x.append("ADD r8 r1 r2")
# x.append("STR r8 r2")
# x.append("LDR r8 r2")

# x.append("ADD r1 a b")
# x.append("MUL r2 r1 r1")
# x.append("ADD r8 r1 r2")
# x.append("STR r8 r2")
# x.append("STR r2 r3")
# x.append("DIV r12 r8 r2")
# x.append("STR r2 r8")
# x.append("ADD r1 r2 r8")
# x.append("STR r1 r8")
# x.append("ADD r1 r1 r2")
# x.append("FADD r3 r2 r1")
# x.append("AND r2 r3 r4")
# x.append("MUL r3 r2 r1")

# x.append("ADD r0 r1 r2")
# x.append("MUL r1 r0 r1")

'''x.append("MUL r3 a b")
x.append("ADD r0 r1 r2")
x.append("MUL r3 r3 r3")
x.append("ADD r0 r1 r3")
x.append("MUL r1 r0 a")'''

# x.append("ADD r1 r2 r3")
# x.append("MUL r2 r1 r3")
# x.append("ADD r1 r2 r3")
# x.append("MUL r2 r1 r2")

# read_lock = [False for i in range(0, 12)]


class FuncUnit:
    def __init__(self, busy=False, op=None, fi=None, fj=None, fk=None, qj=None, qk=None, rj=False, rk=False):
        self.busy = busy
        self.op = op
        self.fi = fi
        self.fj = fj
        self.fk = fk
        self.qj = qj
        self.qk = qk
        self.rj = rj
        self.rk = rk


class InstStatus:
    def __init__(self, issue=None, read_op=None, execute=None, write=None):
        self.issue = issue
        self.read_op = read_op
        self.execute = execute
        self.write = write

    def __str__(self):
        return str(str(self.issue)+"              "+str(self.read_op)+"              "+str(self.execute)+"                "+str(self.write))


regStatus = {'r0': '', 'r1': '', 'r2': '', 'r3': '', 'r4': '', 'r5': '', 'r6': '', 'r7': '', 'r8': '', 'r9': '', 'r10': '', 'r11': '', 'r12': ''}

reg_file = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0, 'r8': 0, 'r9': 0, 'r10': 0, 'r11': 0, 'r12': 0}

dictFU = {'INT': FuncUnit(), 'ADDER': FuncUnit(), 'MUL1': FuncUnit(), 'MUL2': FuncUnit(), 'DIV': FuncUnit(), 'AND': FuncUnit(), 'FMUL': FuncUnit(), 'FADD': FuncUnit()}

dictIns = {i: InstStatus(0, 0, 0, 0) for i in range(len(x))}

# ins_mem = [[0 for j in range(0, 3)] for i in range(len(x))]

ins_mem = {i: [] for i in range(len(x))}

# print(reg_file['r11']+1)


def fetch():
    global x, pc, sub_x, clock

    if pc < len(x):
            temp = x[pc].split(' ')                             # Instruction fetch
            if temp[0] == 'LDR' and regStatus[temp[1]] == '':   # WAW hazard check
                if not dictFU['INT'].busy:                      # structural hazard check
                    dictIns[pc].issue = clock
                    sub_x.append(temp)
                    dictFU['INT'].busy = True
                    dictFU['INT'].op = temp[0]
                    dictFU['INT'].fk = None
                    dictFU['INT'].qj = None
                    dictFU['INT'].qk = None
                    dictFU['INT'].rk = True
                    dictFU['INT'].fi = temp[1]
                    regStatus[temp[1]] = pc
                    if temp[2][0] == 'r':
                        dictFU['INT'].fj = temp[2]
                        if regStatus[dictFU['INT'].fj] == '':
                            dictFU['INT'].rj = True
                        else:
                            dictFU['INT'].rj = False
                        # regStatus[temp[2]] = 'LDR'
                    else:
                        dictFU['INT'].fj = None
                        dictFU['INT'].rj = True
                    pc += 1
            elif temp[0] == 'STR':
                if temp[2][0] != 'r':
                    if not dictFU['INT'].busy:
                        dictIns[pc].issue = clock
                        sub_x.append(temp)
                        dictFU['INT'].busy = True
                        dictFU['INT'].op = temp[0]
                        if temp[1][0] == 'r':
                            dictFU['INT'].fj = temp[1]
                            if regStatus[dictFU['INT'].fj] == '':
                                dictFU['INT'].rj = True
                            else:
                                dictFU['INT'].rj = False
                            # regStatus[temp[1]] = 'STR'
                        else:
                            dictFU['INT'].fj = None
                            dictFU['INT'].rj = True
                        dictFU['INT'].rk = True
                        dictFU['INT'].fk = None
                        dictFU['INT'].qj = None
                        dictFU['INT'].qk = None
                        dictFU['INT'].fi = None
                        pc += 1

                elif temp[2][0] == 'r' and regStatus[temp[2]] == '':
                    if not dictFU['INT'].busy:
                        dictIns[pc].issue = clock
                        sub_x.append(temp)
                        dictFU['INT'].busy = True
                        dictFU['INT'].op = temp[0]
                        if temp[1][0] == 'r':
                            dictFU['INT'].fj = temp[1]
                            if regStatus[dictFU['INT'].fj] == '':
                                dictFU['INT'].rj = True
                            else:
                                dictFU['INT'].rj = False
                            # regStatus[temp[1]] = 'STR'
                        else:
                            dictFU['INT'].fj = None
                            dictFU['INT'].rj = True
                        dictFU['INT'].rk = True
                        dictFU['INT'].fk = None
                        dictFU['INT'].qj = None
                        dictFU['INT'].qk = None
                        dictFU['INT'].fi = temp[2]
                        if regStatus[temp[2]] == '':
                            regStatus[temp[2]] = pc
                        pc += 1

            elif temp[0] == 'ADD' and regStatus[temp[1]] == '':
                if not dictFU['ADDER'].busy:
                    dictIns[pc].issue = clock
                    sub_x.append(temp)
                    dictFU['ADDER'].busy = True
                    dictFU['ADDER'].op = temp[0]
                    dictFU['ADDER'].fi = temp[1]
                    regStatus[temp[1]] = pc
                    dictFU['ADDER'].qj = None
                    dictFU['ADDER'].qk = None
                    if temp[2][0] == 'r':
                        dictFU['ADDER'].fj = temp[2]
                        if regStatus[dictFU['ADDER'].fj] == '':
                            dictFU['ADDER'].rj = True
                        else:
                            dictFU['ADDER'].rj = False
                        # regStatus[temp[2]] = 'ADD'
                    else:
                        dictFU['ADDER'].fj = None
                        dictFU['ADDER'].rj = True
                    if temp[3][0] == 'r':
                        dictFU['ADDER'].fk = temp[3]
                        if regStatus[dictFU['ADDER'].fk] == '':
                            dictFU['ADDER'].rk = True
                        else:
                            dictFU['ADDER'].rk = False
                        # regStatus[temp[3]] = 'ADD'
                    else:
                        dictFU['ADDER'].fk = None
                        dictFU['ADDER'].rk = True
                    pc += 1

            elif temp[0] == 'MUL' and regStatus[temp[1]] == '':
                if not dictFU['MUL1'].busy:
                    dictIns[pc].issue = clock
                    sub_x.append(temp)
                    dictFU['MUL1'].busy = True
                    dictFU['MUL1'].op = pc
                    dictFU['MUL1'].fi = temp[1]
                    regStatus[temp[1]] = pc

                    dictFU['MUL1'].qj = None
                    dictFU['MUL1'].qk = None
                    if temp[2][0] == 'r':
                        dictFU['MUL1'].fj = temp[2]
                        if regStatus[dictFU['MUL1'].fj] == '':
                            dictFU['MUL1'].rj = True
                        else:
                            dictFU['MUL1'].rj = False
                        # regStatus[temp[2]] = 'MUL'
                    else:
                        dictFU['MUL1'].fj = None
                        dictFU['MUL1'].rj = True
                    if temp[3][0] == 'r':
                        dictFU['MUL1'].fk = temp[3]
                        if regStatus[dictFU['MUL1'].fk] == '':
                            dictFU['MUL1'].rk = True
                        else:
                            dictFU['MUL1'].rk = False
                        # regStatus[temp[3]] = 'MUL'+pc
                    else:
                        dictFU['MUL1'].fk = None
                        dictFU['MUL1'].rk = True
                    pc += 1

                elif not dictFU['MUL2'].busy:
                    dictIns[pc].issue = clock
                    sub_x.append(temp)
                    dictFU['MUL2'].busy = True
                    dictFU['MUL2'].op = pc
                    dictFU['MUL2'].fi = temp[1]
                    regStatus[temp[1]] = pc
                    dictFU['MUL2'].qj = None
                    dictFU['MUL2'].qk = None
                    if temp[2][0] == 'r':
                        dictFU['MUL2'].fj = temp[2]
                        if regStatus[dictFU['MUL2'].fj] == '':
                            dictFU['MUL2'].rj = True
                        else:
                            dictFU['MUL2'].rj = False
                        # regStatus[temp[2]] = 'MUL'
                    else:
                        dictFU['MUL2'].fj = None
                        dictFU['MUL2'].rj = True
                    if temp[3][0] == 'r':
                        dictFU['MUL2'].fk = temp[3]
                        if regStatus[dictFU['MUL2'].fk] == '':
                            dictFU['MUL2'].rk = True
                        else:
                            dictFU['MUL2'].rk = False
                        # regStatus[temp[3]] = 'MUL'
                    else:
                        dictFU['MUL2'].fk = None
                        dictFU['MUL2'].rk = True
                    pc += 1

            elif temp[0] == 'DIV' and regStatus[temp[1]] == '':
                if not dictFU['DIV'].busy:
                    dictIns[pc].issue = clock
                    sub_x.append(temp)
                    dictFU['DIV'].busy = True
                    dictFU['DIV'].op = temp[0]
                    dictFU['DIV'].fi = temp[1]
                    regStatus[temp[1]] = pc
                    dictFU['DIV'].qj = None
                    dictFU['DIV'].qk = None
                    if temp[2][0] == 'r':
                        dictFU['DIV'].fj = temp[2]
                        if regStatus[dictFU['DIV'].fj] == '':
                            dictFU['DIV'].rj = True
                        else:
                            dictFU['DIV'].rj = False
                        # regStatus[temp[2]] = 'DIV'
                    else:
                        dictFU['DIV'].fj = None
                        dictFU['DIV'].rj = True
                    if temp[3][0] == 'r':
                        dictFU['DIV'].fk = temp[3]
                        if regStatus[dictFU['DIV'].fk] == '':
                            dictFU['DIV'].rk = True
                        else:
                            dictFU['DIV'].rk = False
                        # regStatus[temp[3]] = 'DIV'
                    else:
                        dictFU['DIV'].fk = None
                        dictFU['DIV'].rk = True
                    pc += 1

            elif temp[0] == 'AND' and regStatus[temp[1]] == '':
                if not dictFU['AND'].busy:
                    dictIns[pc].issue = clock
                    sub_x.append(temp)
                    dictFU['AND'].busy = True
                    dictFU['AND'].op = temp[0]
                    dictFU['AND'].fi = temp[1]
                    regStatus[temp[1]] = pc
                    dictFU['AND'].qj = None
                    dictFU['AND'].qk = None
                    if temp[2][0] == 'r':
                        dictFU['AND'].fj = temp[2]
                        if regStatus[dictFU['AND'].fj] == '':
                            dictFU['AND'].rj = True
                        else:
                            dictFU['AND'].rj = False
                        # regStatus[temp[2]] = 'AND'
                    else:
                        dictFU['AND'].fj = None
                        dictFU['AND'].rj = True
                    if temp[3][0] == 'r':
                        dictFU['AND'].fk = temp[3]
                        if regStatus[dictFU['AND'].fk] == '':
                            dictFU['AND'].rk = True
                        else:
                            dictFU['AND'].rk = False
                        # regStatus[temp[3]] = 'AND'
                    else:
                        dictFU['AND'].fk = None
                        dictFU['AND'].rk = True
                    pc += 1

            elif temp[0] == 'FMUL' and regStatus[temp[1]] == '':
                if not dictFU['FMUL'].busy:
                    dictIns[pc].issue = clock
                    sub_x.append(temp)
                    dictFU['FMUL'].busy = True
                    dictFU['FMUL'].op = temp[0]
                    dictFU['FMUL'].fi = temp[1]
                    regStatus[temp[1]] = pc
                    dictFU['FMUL'].qj = None
                    dictFU['FMUL'].qk = None
                    if temp[2][0] == 'r':
                        dictFU['FMUL'].fj = temp[2]
                        if regStatus[dictFU['FMUL'].fj] == '':
                            dictFU['FMUL'].rj = True
                        else:
                            dictFU['FMUL'].rj = False
                        # regStatus[temp[2]] = 'FMUL'
                    else:
                        dictFU['FMUL'].fj = None
                        dictFU['FMUL'].rj = True
                    if temp[3][0] == 'r':
                        dictFU['FMUL'].fk = temp[3]
                        if regStatus[dictFU['FMUL'].fk] == '':
                            dictFU['FMUL'].rk = True
                        else:
                            dictFU['FMUL'].rk = False
                        # regStatus[temp[3]] = 'FMUL'
                    else:
                        dictFU['FMUL'].fk = None
                        dictFU['FMUL'].rk = True
                    pc += 1

            elif temp[0] == 'FADD' and regStatus[temp[1]] == '':
                if not dictFU['FADD'].busy:
                    dictIns[pc].issue = clock
                    sub_x.append(temp)
                    dictFU['FADD'].busy = True
                    dictFU['FADD'].op = temp[0]
                    dictFU['FADD'].fi = temp[1]
                    regStatus[temp[1]] = pc
                    dictFU['FADD'].qj = None
                    dictFU['FADD'].qk = None
                    if temp[2][0] == 'r':
                        dictFU['FADD'].fj = temp[2]
                        if regStatus[dictFU['FADD'].fj] == '':
                            dictFU['FADD'].rj = True
                        else:
                            dictFU['FADD'].rj = False
                        # regStatus[temp[2]] = 'FADD'
                    else:
                        dictFU['FADD'].fj = None
                        dictFU['FADD'].rj = True
                    if temp[3][0] == 'r':
                        dictFU['FADD'].fk = temp[3]
                        if regStatus[dictFU['FADD'].fk] == '':
                            dictFU['FADD'].rk = True
                        else:
                            dictFU['FADD'].rk = False
                        # regStatus[temp[3]] = 'FADD'
                    else:
                        dictFU['FADD'].fk = None
                        dictFU['FADD'].rk = True
                    pc += 1

'''            else:
                flag = 0
                print(pc)
            if flag:
                pc += 1'''


def decode():
    global clock, pc, x, sub_x
    f1 = 0
    f2 = 0
    for i in range(0, len(x)):
        if dictIns[i].issue > 0 and not dictIns[i].read_op and dictIns[i].issue != clock:
            if sub_x[i][0] != 'STR' and sub_x[i][0] != 'LDR':
                if sub_x[i][2][0] == 'r':
                    if (regStatus[sub_x[i][2]] == '' or str(regStatus[sub_x[i][2]]) >= str(i)): # RAW AND WAR HAZARD CHECK
                        f1 = 1
                else:
                    f1 = 1
                if sub_x[i][3][0] == 'r':
                    if (regStatus[sub_x[i][3]] == '' or str(regStatus[sub_x[i][3]]) >= str(i)):
                        f2 = 1
                else:
                    f2 = 1
                if f1 and f2:
                    dictIns[i].read_op = clock
                    if sub_x[i][2][0] == 'r':
                        ins_mem[i].append(reg_file[sub_x[i][2]])
                    elif sub_x[i][2][0] == '#':
                        ins_mem[i].append(int(sub_x[i][2][1:]))
                    else:
                        ins_mem[i].append(scan[sub_x[i][2]])
                    if sub_x[i][3][0] == 'r':
                        ins_mem[i].append(reg_file[sub_x[i][3]])
                    elif sub_x[i][3][0] == '#':
                        ins_mem[i].append(int(sub_x[i][3][1:]))
                    else:
                        ins_mem[i].append(scan[sub_x[i][3]])
                    ins_mem[i].append(-1)

            elif sub_x[i][0] == 'LDR':
                if sub_x[i][2][0] == 'r':
#                    if regStatus[sub_x[i][2]] == ''
                    if (regStatus[sub_x[i][2]] == '' or str(regStatus[sub_x[i][2]]) >= str(i)):
                        #or (str(regStatus[sub_x[i][2]]) < str(i) and dictIns[int(str(regStatus[sub_x[i][2]]))].write):
                        f1 = 1
                else:
                    f1 = 1
                if f1:
                    dictIns[i].read_op = clock
                    if sub_x[i][2][0] == 'r':
                        ins_mem[i].append(reg_file[sub_x[i][2]])
                    elif sub_x[i][2][0] == '#':
                        ins_mem[i].append(int(sub_x[i][2][1:]))
                    else:
                        ins_mem[i].append(scan[sub_x[i][2]])
                    ins_mem[i].append(-1)

            elif sub_x[i][0] == 'STR':
                if sub_x[i][1][0] == 'r':
#                    if regStatus[sub_x[i][1]] == '':
                    if (regStatus[sub_x[i][1]] == '' or str(regStatus[sub_x[i][1]]) >= str(i)):
                        #or (str(regStatus[sub_x[i][2]]) < str(i) and dictIns[int(str(regStatus[sub_x[i][2]]))].write):
                        f1 = 1
                else:
                    f1 = 1
                if f1:
                    dictIns[i].read_op = clock
                    if sub_x[i][1][0] == 'r':
                        ins_mem[i].append(reg_file[sub_x[i][1]])
                    elif sub_x[i][2][0] == '#':
                        ins_mem[i].append(int(sub_x[i][1][1:]))
                    else:
                        ins_mem[i].append(scan[sub_x[i][1]])
                    ins_mem[i].append(-1)


def exe():
    global clock, pc, x, sub_x
    for i in range(0, len(x)):
        if dictIns[i].read_op > 0 and not dictIns[i].execute:
            if sub_x[i][0] == 'ADD':
                ins_mem[i][2] = methods.cla(ins_mem[i][0], ins_mem[i][1])
#                ins_mem[i][2] = ins_mem[i][0] + ins_mem[i][1]
                dictIns[i].execute = clock + 8
            elif sub_x[i][0] == 'MUL':
                ins_mem[i][2] = methods.wtm(ins_mem[i][0], ins_mem[i][1])
#                ins_mem[i][2] = ins_mem[i][0] * ins_mem[i][1]
                dictIns[i].execute = clock + 19
            elif sub_x[i][0] == 'FMUL':
                ins_mem[i][2] = methods.fpm(ins_mem[i][0], ins_mem[i][1])
#                ins_mem[i][2] = ins_mem[i][0] * ins_mem[i][1]
                dictIns[i].execute = clock + 30
            elif sub_x[i][0] == 'FADD':
                ins_mem[i][2] = methods.fpa(ins_mem[i][0], ins_mem[i][1])
#                ins_mem[i][2] = ins_mem[i][0] + ins_mem[i][1]
                dictIns[i].execute = clock + 30
            elif sub_x[i][0] == 'AND':
                ins_mem[i][2] = ins_mem[i][0] & ins_mem[i][1]
                dictIns[i].execute = clock + 1
            elif sub_x[i][0] == 'DIV':
                ins_mem[i][2] = ins_mem[i][0] / ins_mem[i][1]
                dictIns[i].execute = clock + 40
            elif sub_x[i][0] == 'LDR':
                ins_mem[i][1] = ins_mem[i][0]
                dictIns[i].execute = clock + 1
            elif sub_x[i][0] == 'STR':
                ins_mem[i][1] = ins_mem[i][0]
                dictIns[i].execute = clock + 1


def write_back():
    global clock, pc, x, sub_x

    for i in range(0, len(x)):
        if not dictIns[i].write and 0 < dictIns[i].execute < clock:
            if sub_x[i][0] == 'ADD':
                reg_file[sub_x[i][1]] = ins_mem[i][2]
                dictIns[i].write = clock
                dictFU['ADDER'].busy = False
                regStatus[sub_x[i][1]] = ''
                dictFU['ADDER'].fi = None
                dictFU['ADDER'].fj = None
                dictFU['ADDER'].fk = None
            elif sub_x[i][0] == 'MUL':
                reg_file[sub_x[i][1]] = ins_mem[i][2]
                dictIns[i].write = clock
                regStatus[sub_x[i][1]] = ''
                if dictFU['MUL1'].op == str(i):
                    dictFU['MUL1'].busy = False
                    dictFU['MUL1'].fi = None
                    dictFU['MUL1'].fj = None
                    dictFU['MUL1'].fk = None
                else:
                    dictFU['MUL2'].busy = False
                    dictFU['MUL2'].fi = None
                    dictFU['MUL2'].fj = None
                    dictFU['MUL2'].fk = None
            elif sub_x[i][0] == 'FMUL':
                reg_file[sub_x[i][1]] = ins_mem[i][2]
                dictIns[i].write = clock
                dictFU['FMUL'].busy = False
                regStatus[sub_x[i][1]] = ''
                dictFU['FMUL'].fi = None
                dictFU['FMUL'].fj = None
                dictFU['FMUL'].fk = None
            elif sub_x[i][0] == 'FADD':
                reg_file[sub_x[i][1]] = ins_mem[i][2]
                dictIns[i].write = clock
                dictFU['FADD'].busy = False
                regStatus[sub_x[i][1]] = ''
                dictFU['FADD'].fi = None
                dictFU['FADD'].fj = None
                dictFU['FADD'].fk = None
            elif sub_x[i][0] == 'AND':
                reg_file[sub_x[i][1]] = ins_mem[i][2]
                dictIns[i].write = clock
                dictFU['AND'].busy = False
                regStatus[sub_x[i][1]] = ''
                dictFU['AND'].fi = None
                dictFU['AND'].fj = None
                dictFU['AND'].fk = None
            elif sub_x[i][0] == 'DIV':
                reg_file[sub_x[i][1]] = ins_mem[i][2]
                dictIns[i].write = clock
                dictFU['DIV'].busy = False
                regStatus[sub_x[i][1]] = ''
                dictFU['DIV'].fi = None
                dictFU['DIV'].fj = None
                dictFU['DIV'].fk = None
            elif sub_x[i][0] == 'STR':
                if sub_x[i][2][0] == 'r':
                    reg_file[sub_x[i][2]] = ins_mem[i][1]
                    regStatus[sub_x[i][2]] = ''
                else:
                    scan[sub_x[i][2]] = ins_mem[i][1]
                dictIns[i].write = clock
                dictFU['INT'].busy = False
                dictFU['INT'].fi = None
                dictFU['INT'].fj = None
                dictFU['INT'].fk = None
            elif sub_x[i][0] == 'LDR':
                reg_file[sub_x[i][1]] = ins_mem[i][1]
                dictIns[i].write = clock
                dictFU['INT'].busy = False
                regStatus[sub_x[i][1]] = ''
                dictFU['INT'].fi = None
                dictFU['INT'].fj = None
                dictFU['INT'].fk = None


clock = 1

while clock < 1000:
    fetch()
    decode()
    exe()
    write_back()
    clock += 1


print("\t\t\t\t\tIssue\t","Read_Op ","Execute  ","WriteBack","    Source1","      Source2","       Destination")
print()

for i in range(0, len(x)):
    print("Ins"+str(i+1),"\t:\t",x[i], end='')
    if i != 6:
        print("\t\t",str(dictIns[i]),end='')
        for j in range(len(ins_mem[i])):
            dummy = int(ins_mem[i][j])
            if float(dummy) == ins_mem[i][j]:
                print("\t\t   ",ins_mem[i][j],end='')
            else:
                print("   \t",ins_mem[i][j],end='')
        print()
    else:
        print("\t",str(dictIns[i]),end='')
        for j in range(len(ins_mem[i])):
            dummy = int(ins_mem[i][j])
            if float(dummy) == ins_mem[i][j]:
                print("\t   ",ins_mem[i][j],"    ",end='')
            else:
                print("   \t   ",ins_mem[i][j],"  ",end='')
#            print("\t       ",ins_mem[i][j],"    ",end='')
        print()
    print()


print("The value of c :", scan['c'])






















'''if sub_x[i][0] == 'ADD' and dictFU['ADDER'].rj and dictFU['ADDER'].rk:
    f1 = 1
elif sub_x[i][0] == 'MUL' and dictFU['MUL1'].rj and dictFU['MUL1'].rk and str(i) == dictFU['MUL1'].op:
    f1 = 1
elif sub_x[i][0] == 'MUL' and dictFU['MUL2'].rj and dictFU['MUL2'].rk and str(i) == dictFU['MUL2'].op:
    f1 = 1
elif sub_x[i][0] == 'FMUL' and dictFU['FMUL'].rj and dictFU['FMUL'].rk:
    f1 = 1
elif sub_x[i][0] == 'FADD' and dictFU['FADD'].rj and dictFU['FADD'].rk:
    f1 = 1
elif sub_x[i][0] == 'AND' and dictFU['AND'].rj and dictFU['AND'].rk:
    f1 = 1
elif sub_x[i][0] == 'DIV' and dictFU['DIV'].rj and dictFU['DIV'].rk:
    f1 = 1'''
# print(i)
# print(sub_x[i][2])




# Instruction Decode and Register Fetch
'''if temp[0] != 'LDR' and temp[0] != 'STR':
    if temp[2][0] == '#':
        temp1 = int(temp[2][1:])
    elif temp[2][0] != 'r':
        temp1 = int(temp[2])
    else:
        temp1 = int(reg_file[temp[2]])

    if temp[3][0] == '#':
        temp2 = int(temp[3][1:])
    elif temp[3][0] != 'r':
        temp2 = int(temp[3])
    else:
        temp2 = int(reg_file[temp[3]])

else:
    if temp[0] == 'LDR':
        if temp[2][0] == '#':
            temp1 = int(temp[2][1:])
        elif temp[2][0] != 'r':
            temp1 = int(temp[2])
        else:
            temp1 = int(reg_file[temp[2]])
    else:       # store part
        if temp[1][0] == '#':
            temp1 = int(temp[2][1:])
        elif temp[1][0] != 'r':
            temp1 = int(temp[1])
        else:
            temp1 = int(reg_file[temp[1]])'''
