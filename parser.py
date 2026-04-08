from typing import overload

from lexer import Lexer

@overload
def expect(input, exp1) -> None: ...
@overload
def expect(input, exp1, exp2) -> None: ...

def expect(input, exp1, exp2=None) -> None:
  if exp2 is None:
    if input != exp1:
      raise Exception(f"Expected: {exp1}\n Got: {input}")
  else:
    if input != exp1 or input != exp2:
      raise Exception(f"Expected: {exp1} OR {exp2}\n Got: {input}")
    
  raise Exception("Failed to raise exception!")
  


class Parser:
  def __init__(self) -> None:
    self.lexer = Lexer()
    self.tokens = []
    self.index = -1
    self.current_lexeme = tuple

  def tokenize_file(self, file: str):
    for line in file.splitlines():
      self.tokens.append(line)
  
  def get_next_lexeme(self):
    self.index += 1
    current_token = self.tokens[self.index]

    self.current_lexeme = self.lexer.tokenize(current_token)

  # quiz = "<quiz>", quiz_block ,"</quiz>" ;
  def quiz(self):
    # <quiz>
    self.get_next_lexeme()
    expect(self.current_lexeme, ('TAG_OPEN', '<quiz>'))

    self.get_next_lexeme()
    self.quiz_block()
    # </quiz>
    expect(self.current_lexeme, ('TAG_CLOSE', '</quiz>'))
  
  # quiz_block = title, question, {question} ; 
  def quiz_block(self):
    self.title()

    self.get_next_lexeme()
    self.question()

    # optional: may have additional questions
    self.get_next_lexeme()
    while (self.current_lexeme == ('TAG_OPEN', '<question>')):
      self.question()
      self.get_next_lexeme()

  # title = "<title>", text, "</title>" ;
  def title(self):
    # <title>
    expect(self.current_lexeme, ('TAG_OPEN', '<title>'))

    self.get_next_lexeme()
    self.text()

    # </title>
    self.get_next_lexeme()
    expect(self.current_lexeme, ('TAG_CLOSE', '</title>'))

  # = "<question>", question_block, "</question>" ;
  def question(self):
    # <question>
    expect(self.current_lexeme, ('TAG_OPEN', '<question>'))

    self.get_next_lexeme()
    self.question_block()

    # </question>
    expect(self.current_lexeme, ('TAG_CLOSE', '</question>'))

  # question_block = text, option, option, {option} ;
  def question_block(self):
    self.text()

    self.get_next_lexeme()
    self.option()

    self.get_next_lexeme()
    self.option()

  # optional: may have additonal option
    self.get_next_lexeme()
    while (self.current_lexeme[0] == 'TAG_OPEN' or self.current_lexeme[0] == 'TAG_WITH_ATTR'):
      self.option()
      self.get_next_lexeme()

  # option = "<option ", {correct="true"}, ">", text, "</option"> ;
  def option(self):
    # <option>
    expect(self.current_lexeme, ('TAG_OPEN', '<option>'), ('TAG_WITH_ATTR', '<option correct="true">'))

    self.get_next_lexeme()
    self.text()

    # </option>
    self.get_next_lexeme()
    expect(self.current_lexeme, ('TAG_CLOSE', '</option>'))
  # text = {character} ;
  def text(self):
    expect(self.current_lexeme, ('TAG_CLOSE', '</option>'), ('TAG_WITH_ATTR', '<option correct="true">'))