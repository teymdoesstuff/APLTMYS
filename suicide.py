import sys
import time
import random

HANGUL_FILLER = '\u3164'

ERROR_MESSAGES = [
    "error: you made a typo, wont tell you where tho",
    "error: the error is you",
    "error: base-3 violation, your brain is not compatible",
    "error: segfault in your soul",
    "error: try praying to the parser",
    "error: invalid token, try screaming",
    "error: the invisible void is mocking you",
    "error: misaligned whitespace in the 4th dimension",
    "error: unprintable character detected, closing thread",
    "error: stack overflow in the space between your ears",
    "error: the parser committed die",
    "error: unexpected nothingness, did you forget to sacrifice a goat?",
    "error: base-3 overflow in your frontal lobe",
    "error: syntax error in the empty void lol",
    "error: lmao even",
    "error: you missed an invisible character on line 842. good luck.",
    "error: your screen is dirty, or the code is wrong. i wont say which.",
    "error: the parser putted the toaster in the bath",
    "error: the code just called me ugly, im not running this",
    "error: out of invisible memory",
    "error: the hangul filler ate the newline, they are fighting",
    "error: i forgot what i was doing"
]

def throw_error():
    print(random.choice(ERROR_MESSAGES))
    sys.exit(1)

# --- PREPROCESSOR ---
def preprocess(text):
    allowed = {HANGUL_FILLER, '\n', '\r'}
    for char in text:
        if char not in allowed:
            throw_error()
    
    # Normalize line endings, then convert back to standard > and @ for the parser
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = text.replace(HANGUL_FILLER, '>').replace('\n', '@')
    return text

# --- AST NODES ---
class PrintNode:
    def __init__(self, args): self.args = args

class StoreNode:
    def __init__(self, name, value): self.name = name; self.value = value

class AddNode:
    def __init__(self, dest, src1, src2): self.dest = dest; self.src1 = src1; self.src2 = src2

class ListenNode:
    def __init__(self, dest): self.dest = dest

class DetourNode:
    def __init__(self, val1, val2): self.val1 = val1; self.val2 = val2

class ValueNode:
    def __init__(self, length): self.length = length

# --- PARSER ---
COMMAND_STRINGS = {
    ">@@>>@>>>@>@": "PRINT",
    ">@@@@>@>": "STORE",
    ">>@@>>@>>@": "ADD",
    "@@@@@>>": "LISTEN",
    "@>@>@>@>": "DETOUR"
}

class Parser:
    def __init__(self, code):
        self.code = code
        self.pos = 0

    def parse_program(self):
        statements = []
        while self.pos < len(self.code):
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        cmd_type = None
        cmd_len = 0
        for cmd_str, ctype in COMMAND_STRINGS.items():
            if self.code.startswith(cmd_str, self.pos):
                cmd_type = ctype
                cmd_len = len(cmd_str)
                break
        
        if not cmd_type:
            throw_error()
            
        self.pos += cmd_len

        if cmd_type == 'PRINT':
            args = [self.parse_arg()]
            while self.match_sep():
                self.consume_sep()
                args.append(self.parse_arg())
            self.consume_term()
            return PrintNode(args)
            
        elif cmd_type == 'STORE':
            name = self.parse_arg()
            self.consume_sep()
            val = self.parse_arg()
            self.consume_term()
            return StoreNode(name, val)
            
        elif cmd_type == 'ADD':
            dest = self.parse_arg()
            self.consume_sep()
            s1 = self.parse_arg()
            self.consume_sep()
            s2 = self.parse_arg()
            self.consume_term()
            return AddNode(dest, s1, s2)
            
        elif cmd_type == 'LISTEN':
            dest = self.parse_arg()
            self.consume_term()
            return ListenNode(dest)
            
        elif cmd_type == 'DETOUR':
            v1 = self.parse_arg()
            self.consume_sep()
            v2 = self.parse_arg()
            self.consume_term()
            return DetourNode(v1, v2)

    def parse_arg(self):
        start = self.pos
        while self.pos < len(self.code) and self.code[self.pos] == '>':
            self.pos += 1
        length = self.pos - start
        if length == 0:
            throw_error()
        return ValueNode(length)

    def match_sep(self):
        return self.code.startswith("@@", self.pos) and not self.code.startswith("@@@", self.pos)

    def consume_sep(self):
        self.pos += 2

    def consume_term(self):
        if not self.code.startswith("@@@", self.pos):
            throw_error()
        self.pos += 3

# --- EVALUATOR ---
class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.env = {}
        self.pc = 0

    def eval_literal(self, node):
        count = node.length
        if count == 0: return 0
        try:
            return int(str(count), 3)
        except ValueError:
            throw_error()

    def eval_name(self, node):
        return node.length

    def run(self):
        while self.pc < len(self.ast):
            stmt = self.ast[self.pc]
            if isinstance(stmt, PrintNode):
                out = ""
                for arg in stmt.args:
                    out += chr(self.eval_literal(arg))
                print(out, end="")
                self.pc += 1

            elif isinstance(stmt, StoreNode):
                name = self.eval_name(stmt.name)
                val = self.eval_literal(stmt.value)
                self.env[name] = val
                self.pc += 1

            elif isinstance(stmt, AddNode):
                dest = self.eval_name(stmt.dest)
                s1_name = self.eval_name(stmt.src1)
                s2_name = self.eval_name(stmt.src2)
                
                if s1_name not in self.env or s2_name not in self.env: throw_error()
                
                v1 = self.env[s1_name]
                v2 = self.env[s2_name]
                
                concat = int(str(v1) + str(v2))
                shift = time.time_ns() % 97
                result = concat + shift
                
                if result < 32 or result > 126: throw_error()
                
                self.env[dest] = result
                self.pc += 1

            elif isinstance(stmt, ListenNode):
                dest = self.eval_name(stmt.dest)
                nano_val = time.time_ns() % 1000
                self.env[dest] = nano_val
                self.pc += 1

            elif isinstance(stmt, DetourNode):
                v1 = self.eval_literal(stmt.val1)
                v2 = self.eval_literal(stmt.val2)
                
                diff = abs(v1 - v2)
                if diff == 0:
                    self.pc += 1
                else:
                    self.pc = (self.pc * diff) % len(self.ast)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python suicide.py <source_file.sui>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            source = f.read()
        
        processed_code = preprocess(source)
        
        parser = Parser(processed_code)
        ast = parser.parse_program()
        
        interpreter = Interpreter(ast)
        interpreter.run()

    except Exception:
        throw_error()