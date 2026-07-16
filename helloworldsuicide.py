HANGUL_FILLER = '\u3164'

def generate_base3_guards(char):
    ascii_val = ord(char)
    if ascii_val == 0: return ">" * 0
    
    base3_str = ""
    temp = ascii_val
    while temp > 0:
        base3_str = str(temp % 3) + base3_str
        temp //= 3
        
    num_guards = int(base3_str)
    return ">" * num_guards

def generate_print_statement(text):
    morse_print = ">@@>>@>>>@>@"
    args = []
    for char in text:
        args.append(generate_base3_guards(char))
    
    return morse_print + "@@".join(args) + "@@@"

# Generate the file
target_text = "Hello, World!"
code = generate_print_statement(target_text)

# Convert standard code to invisible code
invisible_code = code.replace('>', HANGUL_FILLER).replace('@', '\n')

with open("helloworld.sui", "w", encoding='utf-8') as f:
    f.write(invisible_code)

print(f"Invisible 'Hello, World!' generated! It contains {len(invisible_code)} invisible characters.")