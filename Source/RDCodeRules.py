"""
Parse Tree Visualizer
Copyright (C) 2024-2025 Leon Zeltser (leonzeltser at gmail dot com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

INDENT: str = ' ' * 4


class RDCodeRules:
    def __init__(self, name: str) -> None:
        self.name: str = name

        self.program_first_statements: str = ''  # things like include statements in C go here

        self.declare_functions: bool = False
        self.function_declaration_beginning: str = ''
        self.function_declaration_end: str = ''

        self.first_code: str = ''  # match, error, and main functions go here
        self.end_of_main: str = ''

        self.function_definition_beginning: str = ''
        self.function_definition_end: str = ''
        self.start_symbol_comment: str = ''

        self.switch_beginning: str = ''
        self.case_beginning: str = ''
        self.case_separator: str = ''
        self.case_end: str = ''
        self.comment_begin: str = ''
        self.comment_end: str = ''

        self.call_function_beginning: str = ''
        self.call_function_end: str = ''
        self.call_match_beginning: str = ''
        self.call_match_end: str = ''

        self.end_of_case: str = ''
        self.skip_case: str = ''
        self.switch_default: str = ''  # this will call the parse error and end of statement

        self.function_last_line: str = ''

        self.program_last_statements: str = ''


Pseudocode = RDCodeRules('Pseudocode')
Pseudocode.first_code = f"""procedure match(expected)
{INDENT}if input_token = expected then consume_input_token()
{INDENT}else parse_error


procedure main()
{INDENT}"""
Pseudocode.end_of_main = '()  /* invoke start symbol */\n\n'
Pseudocode.function_definition_beginning = 'procedure '
Pseudocode.function_definition_end = '()'
Pseudocode.start_symbol_comment = '  /* this is the start symbol */'
Pseudocode.switch_beginning = INDENT + 'case input_token of'
Pseudocode.case_beginning = 2 * INDENT
Pseudocode.case_separator = ', '
Pseudocode.case_end = ' :'
Pseudocode.comment_begin = '  /* '
Pseudocode.comment_end = ' */'
Pseudocode.call_function_beginning = 3 * INDENT
Pseudocode.call_function_end = '()'
Pseudocode.call_match_beginning = 3 * INDENT + 'match('
Pseudocode.call_match_end = ')'
Pseudocode.end_of_case = ' '
Pseudocode.skip_case = 3 * INDENT + 'skip  /* epsilon production */'
Pseudocode.switch_default = INDENT + 'otherwise parse_error'
Pseudocode.function_last_line = '\n'

C = RDCodeRules('C')
C.program_first_statements = """#include <stdlib.h>

void match(token);
void error(void);"""
C.declare_functions = True
C.function_declaration_beginning = 'void '
C.function_declaration_end = '(void);'
C.first_code = f"""void match(token expected) {'{'}
{INDENT}if (input_token == expected) {'{'}
{2 * INDENT}consume_input_token();
{INDENT}{'}'}
{INDENT}else {'{'}
{2 * INDENT}error();
{INDENT}{'}'}
{'}'}

void error(void) {'{'}
{INDENT}exit(1);
{'}'}


int main(int argc, char* argv[]) {'{'}
{INDENT}"""
C.end_of_main = f"();  // invoke start symbol\n{INDENT}return 0;\n" + '}\n\n'
C.function_definition_beginning = 'void '
C.function_definition_end = '(void) {'
C.start_symbol_comment = '  // this is the start symbol'
C.switch_beginning = INDENT + "switch(input_token) {"
C.case_beginning = INDENT + "case '"
C.case_separator = f"':\n{INDENT}case '"
C.case_end = "':"
C.comment_begin = '  // '
C.call_function_beginning = 2 * INDENT
C.call_function_end = '();'
C.call_match_beginning = 2 * INDENT + 'match('
C.call_match_end = ');'
C.end_of_case = 2 * INDENT + 'break;'
C.skip_case = 2 * INDENT + '// epsilon production'
C.switch_default = INDENT + f'default:\n{2 * INDENT}error();\n{2 * INDENT}break;\n{INDENT}' + '}\n}'
C.function_last_line = '\n'
C.program_last_statements = ''

Python = RDCodeRules('Python')
Python.first_code = f"""def match_(expected):
{INDENT}if input_token == expected:
{INDENT * 2} consume(input_token)
{INDENT}else:
{INDENT * 2} raise ParseError


def main()
{INDENT}"""
Python.end_of_main = '()  # invoke start symbol\n\n'
Python.function_definition_beginning = 'def '
Python.function_definition_end = '():'
Python.start_symbol_comment = '  # this is the start symbol'
Python.switch_beginning = INDENT + 'match input_token:'
Python.case_beginning = 2 * INDENT + "case '"
Python.case_separator = "' | '"
Python.case_end = "':"
Python.comment_begin = '  # '
Python.call_function_beginning = 3 * INDENT
Python.call_function_end = '()'
Python.call_match_beginning = 3 * INDENT + "match_('"
Python.call_match_end = "')"
Python.skip_case = 3 * INDENT + 'pass  /* epsilon production */'
Python.switch_default = f"{2 * INDENT}case _:\n{3 * INDENT}raise ParseError"
Python.function_last_line = '\n'
Python.program_last_statements = f"""
if __name__ == '__main__':
{INDENT}main()
"""

RecursiveDescentCodeLanguages: list[RDCodeRules] = [
    Pseudocode, C, Python
]

# TODO: Add OCaml, Java, D, C#, Haskell, Rust, Go, JavaScript, Ada, Ruby
