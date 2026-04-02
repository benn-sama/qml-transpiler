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

    title          = "<title>", string, "</title>" ;

    question       = "<question>", question_block, "</question>" ;
    question_block = text, option, option, {option} ;
    option         = "<option ", {correct="true"}, ">", string, "</option"> ;

    character = any character ;
    string = {character} ;

"""