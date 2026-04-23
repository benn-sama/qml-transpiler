from typing import overload
import re
import logging

from lexer import Lexer
from nodes import Option, Question, Quiz

# stupid python overloading :'(
@overload
def expect(input, exp1) -> None: ...

@overload
def expect(input, exp1, exp2) -> None: ...

def expect(input, exp1, exp2=None) -> None:
    if exp2 is None: # checks if some exp2 has passed to the function 
        if input != exp1:
            raise Exception(f"\nExpected: {exp1}\n Got: {input}")
    else:            # assumes some exp2 exists
        if input != exp1 and input != exp2:
            raise Exception(f"\nExpected: {exp1} OR {exp2}\n Got: {input}")

# obviously this is the parser
class Parser:
  def __init__(self, debug=False) -> None:
    self.lexer          = Lexer()
    self.tokens         = []
    self.index          = -1
    self.current_lexeme = tuple

  # tokenizes the whole file 
  def tokenize_file(self, file: str):
    # regex stuff
    TOKEN_SPEC = [
      r'<[a-zA-Z]+\s+[a-zA-Z]+="[^"]*">', # open, attribute
      r'<[a-zA-Z]+>',                     # open, no attribute
      r'[^<]+',                           # text
      r'</[a-zA-Z]+>',                    # close
      r'\n',                              # new line
      r'\s+'                              # white space
    ]

    # combines patterns in TOKEN_SPEC
    master_pattern = '|'.join(TOKEN_SPEC)
    regex = re.compile(master_pattern)

    # splits apart the sentences
    for match in regex.finditer(file):
        value = match.group().strip()
        
        if not value:
            continue
        
        if value.startswith('<'):
            self.tokens.append(value)
        else:
            self.tokens.extend(value.split())

  # gets next lexeme 
  def get_next_lexeme(self):
    self.index += 1
    current_token = self.tokens[self.index]

    self.current_lexeme = self.lexer.tokenize(current_token)

  # quiz = "<quiz>", quiz_block ,"</quiz>" ;
  def quiz(self):
    self.get_next_lexeme()

    # <quiz>
    expect(self.current_lexeme, ('TAG_OPEN', '<quiz>'))

    self.get_next_lexeme()
    title, question = self.quiz_block()

    # </quiz>
    expect(self.current_lexeme, ('TAG_CLOSE', '</quiz>'))

    return Quiz(title=title, question=question)
  
  # quiz_block = title, question, {question} ; 
  def quiz_block(self) -> tuple[str, list]:

    title = self.title()

    self.get_next_lexeme()
    questions = []
    questions.append(self.question())

    # optional: may have additional questions
    self.get_next_lexeme()
    while (self.current_lexeme == ('TAG_OPEN', '<question>')):
      questions.append(self.question())
      self.get_next_lexeme()

    return title, questions

  # title = "<title>", text, "</title>" ;
  def title(self) -> str:
    # <title>
    expect(self.current_lexeme, ('TAG_OPEN', '<title>'))

    self.get_next_lexeme()
    title = self.string()

    # </title>
    expect(self.current_lexeme, ('TAG_CLOSE', '</title>'))

    return title

  # = "<question>", question_block, "</question>" ;
  def question(self) -> Question:
    # <question>
    expect(self.current_lexeme, ('TAG_OPEN', '<question>'))

    self.get_next_lexeme()
    text, options = self.question_block()

    # </question>
    expect(self.current_lexeme, ('TAG_CLOSE', '</question>'))
    return Question(text=text, options=options)

  # question_block = text, option, option, {option} ;
  def question_block(self) -> tuple[str, list]:
    text = self.text()
    self.get_next_lexeme()

    options = []
    options.append(self.option())
    self.get_next_lexeme()

    options.append(self.option())

  # optional: may have additonal option
    self.get_next_lexeme()
    while (self.current_lexeme[0] == 'TAG_OPEN' or self.current_lexeme[0] == 'TAG_WITH_ATTR'):
      options.append(self.option())
      self.get_next_lexeme()

    return text, options

  # option = "<option ", {correct="true"}, ">", text, "</option"> ;
  def option(self) -> Option:
    # check for correct option
    correct = self.current_lexeme == ('TAG_WITH_ATTR', '<option correct="true">')
    # <option>
    expect(self.current_lexeme, ('TAG_OPEN', '<option>'), ('TAG_WITH_ATTR', '<option correct="true">'))

    self.get_next_lexeme()
    text = self.string()

    # </option>
    expect(self.current_lexeme, ('TAG_CLOSE', '</option>'))

    return Option(correct=correct, text=text)

  # text = <text>, {character}, </text> ;
  def text(self) -> str:
    expect(self.current_lexeme, ('TAG_OPEN', '<text>'))

    self.get_next_lexeme()
    text = self.string()
    
    expect(self.current_lexeme, ('TAG_CLOSE', '</text>'))
    return text

  def string(self) -> str:
    words = []
    type  = self.current_lexeme[0]
    value = self.current_lexeme[1]

    # Type: STRING
    expect(type, 'STRING')
    words.append(value)

    self.get_next_lexeme()

    type  = self.current_lexeme[0]
    value = self.current_lexeme[1]

  # check if more text exists
    while (type == 'STRING'):
      # Type: STRING
      expect(type, 'STRING')
      words.append(value)

      self.get_next_lexeme()
      type  = self.current_lexeme[0]
      value = self.current_lexeme[1]
    
    return ' '.join(words)

  # the actual main parser
  def parse(self, file: str):
    self.tokenize_file(file)
    # returns the ast
    return self.quiz()