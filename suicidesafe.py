import sys
import time
import random

# The Lexicon of Pain
VALID_CHARS = {'>', '@'}

# Even more demeaning error messages
ERROR_MESSAGES = [
    "error: you made a typo, wont tell you where tho",
    "error: the error is you",
    "error: base-3 violation, your brain is not compatible",
    "error: segfault in your soul",
    "error: try praying to the parser",
    "error: invalid token, try screaming",
    "error: the @ is mocking you",
    "error: the >s are misaligned, consult a priest",
    "error: unprintable character detected, closing thread",
    "error: stack overflow in the space between your ears",
    "error: the parser committed die",
    "error: unexpected token, did you forget to sacrifice a goat?",
    "error: base-3 overflow in your frontal lobe",
    "error: syntax error lol",
    "error: lmao even"
]

def throw_error():
    print(random.choice(ERROR_MESSAGES))
    sys.exit(1)

# --- LEXER ---
class Lexer:
    def __init__(self, text):
        self.text = text.replace(" ", "").replace("\n", "").replace("\t", "")
        self.tokens = []

    def tokenize(self):
        if not self.text:
            throw_error()

        i = 0
        while i < len(self.text):
            if self.text[i] == '>':
                start = i
                while i < len(self.text) and self.text[i] == '>':
                    i += 1
                self.tokens.append(('GUARD', i - start))
            elif self.text[i] == '@':
                start = i
                while i < len(self.text) and self.text[i] == '@':
                    i += 1
                self.tokens.append(('AT', i - start))
            else:
                throw_error()
        
        return self.tokens

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
class Parser:
    # Command signatures mapped to their token lengths
    # >@@>>@>>>@>@ -> 1,2,2,1,3,1,1,1 (8 tokens)
    # >@@@@>@> -> 1,4,1,1,1 (5 tokens)
    # >>@@>>@>>@ -> 2,2,2,1,2,1 (6 tokens)
    # @@@@@>> -> 5,2 (2 tokens)
    # @>@>@>@> -> 1,1,1,1,1,1 (6 tokens)
    COMMAND_SIGS = {
        (1, 2, 2, 1, 3, 1, 1, 1): 'PRINT',
        (1, 4, 1, 1, 1): 'STORE',
        (2, 2, 2, 1, 2, 1): 'ADD',
        (5, 2): 'LISTEN',
        (1, 1, 1, 1, 1, 1): 'DETOUR'
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type, expected_count=None):
        tok = self.current()
        if tok is None: throw_error()
        if tok[0] != expected_type: throw_error()
        if expected_count is not None and tok[1] != expected_count: throw_error()
        self.pos += 1
        return tok

    def parse_arg(self):
        tok = self.consume('GUARD')
        return ValueNode(tok[1])

    def parse_program(self):
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        # Peek ahead to find which command signature matches
        best_match = None
        match_len = 0
        
        for sig, cmd_type in self.COMMAND_SIGS.items():
            if len(sig) > len(self.tokens) - self.pos:
                continue
            
            match = True
            for i, count in enumerate(sig):
                if self.tokens[self.pos + i][0] == 'GUARD' and self.tokens[self.pos + i][1] == count:
                    continue
                elif self.tokens[self.pos + i][0] == 'AT' and self.tokens[self.pos + i][1] == count:
                    continue
                else:
                    match = False
                    break
            
            if match and len(sig) > match_len:
                best_match = cmd_type
                match_len = len(sig)

        if not best_match:
            throw_error()

        # Consume the command signature tokens
        for _ in range(match_len):
            self.pos += 1

        # Parse arguments
        if best_match == 'PRINT':
            args = [self.parse_arg()]
            while self.pos < len(self.tokens) and self.current()[0] == 'AT' and self.current()[1] == 2:
                self.consume('AT', 2)
                args.append(self.parse_arg())
            self.consume('AT', 3)
            return PrintNode(args)

        elif best_match == 'STORE':
            name = self.parse_arg()
            self.consume('AT', 2)
            val = self.parse_arg()
            self.consume('AT', 3)
            return StoreNode(name, val)

        elif best_match == 'ADD':
            dest = self.parse_arg()
            self.consume('AT', 2)
            s1 = self.parse_arg()
            self.consume('AT', 2)
            s2 = self.parse_arg()
            self.consume('AT', 3)
            return AddNode(dest, s1, s2)

        elif best_match == 'LISTEN':
            dest = self.parse_arg()
            self.consume('AT', 3)
            return ListenNode(dest)

        elif best_match == 'DETOUR':
            v1 = self.parse_arg()
            self.consume('AT', 2)
            v2 = self.parse_arg()
            self.consume('AT', 3)
            return DetourNode(v1, v2)

        throw_error()

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
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse_program()
        
        interpreter = Interpreter(ast)
        interpreter.run()

    except Exception:
        throw_error()
