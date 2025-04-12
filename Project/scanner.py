# scanner.py

class Scanner:
    def __init__(self, input_path):
        self.input_path = input_path
        self.tokens = {}
        self.errors = {}
        self.symbol_table = []
        self.keywords = ["if", "else", "void", "int", "while", "break", "return"]
        self.symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<', '==']

    def tokenize(self):
        with open(self.input_path, "r") as f:
            lines = f.readlines()

        for lineno, line in enumerate(lines, 1):
            self._process_line(line, lineno) # pass each line to _process_line method whit line number

    def _process_line(self, line, lineno):
        index = 0 # index is used for searching token
        length = len(line) 
        tokens = []
        errors = []

        while index < length:
            ch = line[index]

            # end of token
            if ch in [' ', '\n', '\r', '\t', '\v', '\f']:
                index += 1
                continue

            elif ch.isdigit(): # check if token is digit
                start = index # start is used for start of token
                while index < length and line[index].isdigit(): # loop for searching digits
                    index += 1
                if index < length and line[index].isalpha(): # check if token is invalid
                    while index < length and (line[index].isalpha() or line[index].isdigit()): # when token is not end and (digit or alpha) go to next 
                        index += 1
                    lexeme = line[start:index] # new invalid lexeme
                    errors.append((lexeme, 'Invalid number'))
                else:  # valid number
                    lexeme = line[start:index]
                    tokens.append(('NUM', lexeme))

            elif ch.isalpha():
                start = index
                while index < length and line[index].isalnum():
                    index += 1
                lexeme = line[start:index]
                if lexeme in self.keywords: # check if token is keyword
                    tokens.append(('KEYWORD', lexeme))
                else: # check if token is identifier
                    tokens.append(('ID', lexeme))
                    if lexeme not in self.symbol_table: # add identifier to symbol table
                        self.symbol_table.append(lexeme)

            elif ch == '/':
                if index + 1 < length and line[index + 1] == '*': # check if token is comment
                    start = index
                    index += 2
                    while index + 1 < length and not (line[index] == '*' and line[index + 1] == '/'):
                        index += 1
                    if index + 1 < length: # it's valid comment and don't tokenize
                        index += 2
                        continue
                    else:
                        snippet = line[start+2:start+9] + "..." if len(line) > start+2 else "..."
                        errors.append((f"/* {snippet}", "Unclosed comment"))
                        break
                else:
                    tokens.append(('SYMBOL', '/')) # if not a comment it's a symbol
                    index += 1

            elif ch == '=': # check if token is assignment symbol (=, ==)
                if index + 1 < length and line[index + 1] == '=':
                    tokens.append(('SYMBOL', '=='))
                    index += 2
                else: 
                    tokens.append(('SYMBOL', '='))
                    index += 1

            elif ch in self.symbols: # not a comment and identifier then it's a symbol
                tokens.append(('SYMBOL', ch))
                index += 1

            elif ch == '*' and index + 1 < length and line[index + 1] == '/':
                errors.append(('*/', 'Unmatched comment'))
                index += 2

            else: # i can't find any token then it's invalid token
                errors.append((ch, 'Invalid input'))
                index += 1

        if tokens:
            self.tokens.setdefault(lineno, []).extend(tokens)
        if errors:
            self.errors.setdefault(lineno, []).extend(errors)

    def write_outputs(self):
        self._write_tokens()
        self._write_errors()
        self._write_symbol_table()

    def _write_tokens(self):
        with open("tokens.txt", "w") as f:
            if not self.tokens:
                return
            for lineno in sorted(self.tokens.keys()):
                token_line = " ".join(f"({typ}, {val})" for typ, val in self.tokens[lineno])
                f.write(f"{lineno} {token_line}\n")

    def _write_errors(self):
        with open("lexical_errors.txt", "w") as f:
            if not self.errors:
                f.write("There is no lexical error.\n")
            else:
                for lineno in sorted(self.errors.keys()):
                    error_line = " ".join(f"({val}, {msg})" for val, msg in self.errors[lineno])
                    f.write(f"{lineno} {error_line}\n")

    def _write_symbol_table(self):
        symbols = self.keywords + self.symbol_table
        with open("symbol_table.txt", "w") as f:
            for idx, symbol in enumerate(symbols, 1):
                f.write(f"{idx}. {symbol}\n")
