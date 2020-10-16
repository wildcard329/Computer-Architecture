"""CPU functionality."""

import sys

SP = 0b00000111
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
POP = 0b01000110
RET = 0b00010001
PUSH = 0b01000101
CALL = 0b01010000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.fl = 0
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.reg[SP] = 0xF4
        self.cmds = {}
        self.cmds[LDI] = self.LDI_val
        self.cmds[PRN] = self.PRN_val
        self.cmds[MUL] = self.MUL_val
        self.cmds[HLT] = self.HLT_val
        self.cmds[POP] = self.POP_val
        self.cmds[JEQ] = self.JEQ_val
        self.cmds[JNE] = self.JNE_val
        self.cmds[CMP] = self.CMP_val
        self.cmds[PUSH] = self.PUSH_val

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        try:

            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number: '{n}")
                        sys.exit(1)

                    self.ram_write(address, n)
                    address += 1

        except FileNotFoundError:
            print(f'File not found: {sys.argv[1]}')
            sys.exit(2)

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == 'CMP':
            if reg_a == reg_b:
                self.fl | 0b001
                self.fl & 0b001
            elif reg_a < reg_b:
                self.fl | 0b100
                self.fl & 0b100
            elif reg_a > reg_b:
                self.fl | 0b010
                self.fl & 0b010
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def PRN_val(self, idx, arg2):
        print(self.reg[idx])

    def LDI_val(self, arg1, arg2):
        self.reg[arg1] = self.ram_read(arg2)

    def MUL_val(self, num1, num2):
        self.alu("MUL", num1, self.ram_read(num2))

    def HLT_val(self, arg1, arg2):
        sys.exit(0)

    def PUSH_val(self, arg1, arg2):
        self.reg[SP] -= 1
        val = self.reg[arg1]
        self.ram[self.reg[SP]] = val

    def POP_val(self, arg1, arg2):
        val = self.ram[self.reg[SP]]
        self.reg[arg1] = val
        self.reg[SP] += 1

    def CALL_val(self, arg1, arg2):
        self.PUSH_val(arg2)
        self.pc = arg1

    def RET_val(self, arg1, arg2):
        self.pc = self.POP_val()

    def JMP_val(self, arg1, arg2):
        self.pc = self.reg[arg1]

    def JNE_val(self, arg1, arg2):
        if self.fl == 0:
            print('jne')
            self.JMP_val(arg1, arg2)

    def JEQ_val(self, arg1, arg2):
        if self.fl == 1:
            print('jeq')
            self.JMP_val(arg1, arg2)

    def CMP_val(self, arg1, arg2):
        reg_a = self.reg[arg1]
        reg_b = self.reg[self.ram_read(arg2)]
        self.alu("CMP", reg_a, reg_b)

    def run(self):
        """Run the CPU."""

        while True:
            ir = self.ram_read((self.pc))
            argA = self.ram_read(self.pc + 1)
            argB = self.pc + 2

            if ir in self.cmds:
                self.cmds[ir](argA, argB)
                # print(self.reg[0])
                # input()
            if ir is not None:
                i_len = ((ir & 0b11000000) >> 6) + 1
                self.pc += i_len
