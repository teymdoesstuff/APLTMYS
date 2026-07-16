# A Programming Language That Makes You Suicidal

[![Language Status](https://img.shields.io/badge/Status-Cognitohazard-red)](https://github.com)
[![License](https://img.shields.io/badge/License-None%20(Why%20would%20you%20steal%20this%3F)-black)](https://github.com)
[![Typo Rate](https://img.shields.io/badge/Typo%20Rate-100%25-blue)](https://github.com)

> *"Brainfuck is for toddlers. Whitespace is for the visually impaired. This is for the clinically insane."*

A Programming Language That Makes You Suicidal is an esoteric programming language designed to violate the Geneva Conventions of software engineering. It is completely invisible, relies on Base-3 mathematics applied to character counts, and will actively gaslight you into madness.

## The Lexicon of Pain

The language consists of exactly **two** characters, both of which are invisible or whitespace:

1. `ㅤ` (Hangul Filler, Unicode U+3164) - The Primitive.
2. `\n` (Newline) - The Separator.

If you can see your code, you are doing it wrong. Your source files will look like completely empty documents. If you accidentally press the spacebar, the program will crash, and the interpreter will mock you.

## The Core Rules of Suffering

### 1. The Base-3 Length Rule
You do not pass values by typing numbers. You pass values by typing the Hangul Filler (`ㅤ`). 

To figure out what value you are passing:
1. Find the ASCII value of the character you want (e.g., `A` = 65).
2. Convert that number to Base-3 (e.g., 65 in Base-3 is `2102`).
3. Type the Hangul Filler exactly that many times. (e.g., To type the letter `A`, you must type `2,102` invisible characters).

If you make a typo and type `2103` invisible characters, `2103` is not a valid Base-3 number. The program will crash.

### 2. Morse Code Commands
Commands are not English words. They are specific, alternating patterns of Hangul Fillers and Newlines.

*   `@@` (Two Newlines) = Separates arguments in a command.
*   `@@@` (Three Newlines) = Ends a command.

## Command Reference

| Command | Invisible Syntax (`ㅤ` and `\n`) | Visual Equivalent | Description |
| :--- | :--- | :--- | :--- |
| **PRINT** | `ㅤ\n\nㅤㅤ\nㅤㅤㅤ\nㅤ\nㅤ` | `>@@>>@>>>@>@` | Prints arguments to the screen. |
| **STORE** | `ㅤ\n\n\n\nㅤ\nㅤ` | `>@@@@>@>` | Creates a variable. Variable names are also Base-3 Hangul lengths. |
| **ADD** | `ㅤㅤ\n\nㅤㅤ\nㅤㅤ\n` | `>>@@>>@>>@` | Adds two variables. *Catch: It concatenates the digits and shifts them by a prime number based on the current nanosecond. If the result is unprintable, it crashes.* |
| **LISTEN** | `\n\n\n\n\nㅤㅤ` | `@@@@@>>` | Takes user input. *Catch: It reads the last 3 digits of the system clock nanosecond. You must run the script at the exact right millisecond to get the input you want.* |
| **DETOUR** | `\nㅤ\nㅤ\nㅤ\nㅤ` | `@>@>@>@>` | The GOTO command. *Catch: It jumps to line `(current_line * absolute_difference) % total_lines`. It is completely unpredictable.* |

## Error Messages

Because the code is invisible, debugging is impossible. Therefore, the interpreter does not tell you where the error is, or what the error is. It simply mocks you. 

Example error messages include:
*   `error: you made a typo, wont tell you where tho`
*   `error: the parser putted the toaster in the bath`
*   `error: base-3 violation, your brain is not compatible`
*   `error: the error is you`
*   `error: you missed an invisible character on line 842. good luck.`
*   `error: unexpected nothingness, did you forget to sacrifice a goat?`

## "Hello, World!"

Typing "Hello, World!" requires manually counting out over **100,000 invisible characters** with zero visual feedback. 

Here is what "Hello, World!" looks like in the source code:

```text


      
```

If you accidentally hit a spacebar instead of the Hangul Filler, the program will commit die.

## Usage

Because writing this by hand is a one-way ticket to a psychiatric ward, a Python generator and interpreter are provided.

1. **Generate the invisible code:**
   Run the generator script to create the `.sui` file.
   ```bash
   python gen_hello.py
   ```

2. **Run the interpreter:**
   Pray to the parser and run the source file.
   ```bash
   python suicide.py helloworld.sui
   ```

## Why?

Because Malbolge was too easy, and we wanted a language where the development environment is actively gaslighting you. You will stare at a blank screen, wondering if the file is empty, if your editor is broken, or if you just miscounted 10,000 invisible Unicode characters.

You made a typo. Good luck finding it.
```
