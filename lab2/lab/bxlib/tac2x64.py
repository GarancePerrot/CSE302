# --------------------------------------------------------------------
import abc

# --------------------------------------------------------------------
class AsmGen(abc.ABC):
    BACKENDS   = {}

    def __init__(self):
        self._temps = dict()
        self._asm   = []

    def _temp(self, temp):
        index = self._temps.setdefault(temp, len(self._temps))
        return self._format_temp(index)

    @abc.abstractmethod
    def _format_temp(self, index):
        pass

    def __call__(self, instr): 
        opcode = instr["opcode"]
        args   = instr["args"]

        if instr["result"] is not None:
            args.append(instr["result"])

        getattr(self, f'_emit_{opcode}')(*args)

    def _get_asm(self, opcode, *args):
        if not args:
            return f'\t{opcode}'
        return f'\t{opcode}\t{", ".join(args)}'

    def _get_label(self, lbl):
        return f'{lbl}:'

    def _emit(self, opcode, *args):
        self._asm.append(self._get_asm(opcode, *args))

    @classmethod
    def get_backend(cls, name):
        return cls.BACKENDS[name]

# --------------------------------------------------------------------
class AsmGen_x64_Linux(AsmGen):
    def _format_temp(self, index):
        return f'-{8*index}(%rbp)'

    def _emit_const(self, ctt, dst):
        self._emit('movq', f'${ctt}', self._temp(dst))

    def _emit_copy(self, src, dst):
        self._emit('movq', self._temp(src), '%r11')
        self._emit('movq', '%r11', self._temp(dst))

    def _emit_alu1(self, opcode, src, dst):
        self._emit('movq', self._temp(src), '%r11')
        self._emit(opcode, '%r11')
        self._emit('movq', '%r11', self._temp(dst))

    def _emit_neg(self, src, dst):
        self._emit_alu1('negq', src, dst)

    def _emit_not(self, src, dst):
        self._emit_alu1('notq', src, dst)

    def _emit_alu2(self, opcode, op1, op2, dst):
        self._emit('movq', self._temp(op1), '%r11')
        self._emit(opcode, self._temp(op2), '%r11')
        self._emit('movq', '%r11', self._temp(dst))

    def _emit_add(self, op1, op2, dst):
        self._emit_alu2('addq', op1, op2, dst)
        
    def _emit_sub(self, op1, op2, dst):
        self._emit_alu2('subq', op1, op2, dst)

    def _emit_mul(self, op1, op2, dst):
        self._emit('movq', self._temp(op1), '%r11')
        self._emit('imulq', self._temp(op2))
        self._emit('movq', '%rax', self._temp(dst))

    def _emit_div(self, op1, op2, dst):
        self._emit('movq', self._temp(op1), '%r11')
        self._emit('cqto')
        self._emit('idivq', self._temp(op2))
        self._emit('movq', '%rax', self._temp(dst))

    def _emit_mod(self, op1, op2, dst):
        self._emit('movq', self._temp(op1), '%r11')
        self._emit('cqto')
        self._emit('idivq', self._temp(op2))
        self._emit('movq', '%rdx', self._temp(dst))

    def _emit_and(self, op1, op2, dst):
        self._emit_alu2('andq', op1, op2, dst)

    def _emit_or(self, op1, op2, dst):
        self._emit_alu2('orq', op1, op2, dst)

    def _emit_xor(self, op1, op2, dst):
        self._emit_alu2('xorq', op1, op2, dst)

    def _emit_shl(self, op1, op2, dst):
        self._emit('movq', self._temp(op1), '%r11')
        self._emit('movq', self._temp(op2), '%rcx')
        self._emit('salq', '%cl', '%r11')
        self._emit('movq', '%r11', self._temp(dst))

    def _emit_shr(self, op1, op2, dst):
        self._emit('movq', self._temp(op1), '%r11')
        self._emit('movq', self._temp(op2), '%rcx')
        self._emit('sarq', '%cl', '%r11')
        self._emit('movq', '%r11', self._temp(dst))

    def _emit_print(self, arg):
        self._emit('leaq', '.lprintfmt(%rip)', '%rdi')
        self._emit('movq', self._temp(arg), '%rsi')
        self._emit('xorq', '%rax', '%rax')
        self._emit('callq', 'printf@PLT')

    def code(self):
        nvars  = len(self._temps)
        nvars += nvars & 1

        return [
            self._get_asm('pushq', '%rbp'),
            self._get_asm('movq', '%rsp', '%rbp'),
            self._get_asm('subq', f'${8*nvars}', '%rsp'),
        ] + self._asm + [
            self._get_asm('movq', '%rbp', '%rsp'),
            self._get_asm('popq', '%rbp'),
            self._get_asm('xorq', '%rax', '%rax'),
            self._get_asm('retq'),
        ]

    @classmethod
    def lower(cls, tac_full) -> str: #tac_full is the result of MM : tac_full = [ { "proc" = "@main" , "body" = [ tac ] } ]
        emitter = cls()

        tac = (tac_full[0])["body"] #extracting tac instructions 

        for instr in tac:           #tac is a list of instr of the form {"opcode" : _ , "args" : _ , "result" : _}
            emitter(instr)

        aout = [
            emitter._get_asm('.section', '.rodata'),
            emitter._get_label('.lprintfmt'),
            emitter._get_asm('.string', '"%ld\\n"'),
            '',
            emitter._get_asm('.text'),
            emitter._get_asm('.globl', 'main'),
            emitter._get_label('main'),
        ] + emitter.code()

        return "\n".join(aout) + "\n"

AsmGen.BACKENDS['x64-linux'] = AsmGen_x64_Linux