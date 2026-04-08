"""
Docstring for ebnf

QML tags inluded:
- <quiz></quiz>            -> {title:1 AND question: x >= 1}
- <title></title>
- <question></question>    -> {text:1 AND option: x >= 2}
- <text></text>
- <option></option>        -> {optional: correct="true" tag}


- set A = {quiz}
- subset of A, B = {title, question}
- subset of B, C = {text, option}
"""

"""
  Grammer (EBNF) - matches lexer/tokenization and identifier rules:

    quiz           = "<quiz>", quiz_block ,"</quiz>" ;
    quiz_block     = title, question, {question} ; 

    title          = "<title>", text, "</title>" ;

    question       = "<question>", question_block, "</question>" ;
    question_block = text, option, option, {option} ;
    option         = "<option ", {correct="true"}, ">", text, "</option"> ;

    character = any character ;
    text = {character} ;
"""

import re

# patterns
# TAG_OPEN         = r'<[a-zA-Z]+>'                           # <quiz>, <title>, <question>, <text
# TAG_CLOSE        = r'</[a-zA-Z]+>'                          # </quiz>, </title>, </question>, </text>
# TAG_WITH_ATTR    = r'<[a-zA-Z]+\s+[a-zA-Z]+="[^"]*">'       # <option correct="true">
# TEXT             = r'[^<]+'                                 # anything between tags
# WHITESPACE       = r'\s+'                                   # spaces, tabs, newlines

TOKEN_SPEC = [
    ('TAG_CLOSE',      r'</[a-zA-Z]+>'),
    ('TAG_WITH_ATTR',  r'<[a-zA-Z]+\s+[a-zA-Z]+="[^"]*">'),
    ('TAG_OPEN',       r'<[a-zA-Z]+>'),
    ('TEXT',           r'[^<]+'),
    ('WHITESPACE',     r'\s+'),
]

master_pattern = '|'.join(
    f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC
)

regex = re.compile(master_pattern)