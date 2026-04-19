from typing import overload
import re

from lexer import Lexer

# stupid python overloading :'(
@overload
def expect(input, exp1) -> None: ...
@overload
def expect(input, exp1, exp2) -> None: ...
def expect(input, exp1, exp2=None) -> None:
    if exp2 is None:
        if input != exp1:
            raise Exception(f"\nExpected: {exp1}\n Got: {input}")
    else:
        if input != exp1 and input != exp2:
            raise Exception(f"\nExpected: {exp1} OR {exp2}\n Got: {input}")

# obviously this is the parser
class Parser:
  def __init__(self, debug=False) -> None:
    self.lexer = Lexer()
    self.tokens = []
    self.index = -1
    self.current_lexeme = tuple
    self.debug = debug

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

  # ---------- FOR TESTING ----------
  def print(self):
    print(self.tokens)

  # quiz = "<quiz>", quiz_block ,"</quiz>" ;
  def quiz(self):

    # ------ DEBUG ------
    if self.debug:
      print("Currently in quiz()")
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    # <quiz>
    self.get_next_lexeme()

    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    expect(self.current_lexeme, ('TAG_OPEN', '<quiz>'))

    self.get_next_lexeme()

      # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    self.quiz_block()
    # </quiz>
    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    expect(self.current_lexeme, ('TAG_CLOSE', '</quiz>'))
  
  # quiz_block = title, question, {question} ; 
  def quiz_block(self):
    # ------ DEBUG ------
    if self.debug:
      print("Currently in quiz_block()")

    self.title()

    self.get_next_lexeme()

    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    self.question()

    # optional: may have additional questions
    self.get_next_lexeme()
    while (self.current_lexeme == ('TAG_OPEN', '<question>')):
      self.question()
      self.get_next_lexeme()

  # title = "<title>", text, "</title>" ;
  def title(self):
    # ------ DEBUG ------
    if self.debug:
      print("Currently in title()")

    # <title>
    expect(self.current_lexeme, ('TAG_OPEN', '<title>'))

    self.get_next_lexeme()

    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    self.string()

    # </title>
    expect(self.current_lexeme, ('TAG_CLOSE', '</title>'))

  # = "<question>", question_block, "</question>" ;
  def question(self):
    # ------ DEBUG ------
    if self.debug:
      print("Currently in question()")

    # <question>
    expect(self.current_lexeme, ('TAG_OPEN', '<question>'))

    self.get_next_lexeme()
    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    self.question_block()

    # </question>
    expect(self.current_lexeme, ('TAG_CLOSE', '</question>'))

  # question_block = text, option, option, {option} ;
  def question_block(self):
    # ------ DEBUG ------
    if self.debug:
      print("Currently in question_block()")

    self.text()

    self.get_next_lexeme()
    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    self.option()

    self.get_next_lexeme()
    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    self.option()

  # optional: may have additonal option
    self.get_next_lexeme()
    while (self.current_lexeme[0] == 'TAG_OPEN' or self.current_lexeme[0] == 'TAG_WITH_ATTR'):
      self.option()
      self.get_next_lexeme()

  # option = "<option ", {correct="true"}, ">", text, "</option"> ;
  def option(self):
    # ------ DEBUG ------
    if self.debug:
      print("Currently in option()")

    # <option>
    expect(self.current_lexeme, ('TAG_OPEN', '<option>'), ('TAG_WITH_ATTR', '<option correct="true">'))

      
    self.get_next_lexeme()

    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    self.string()

    # </option>
    expect(self.current_lexeme, ('TAG_CLOSE', '</option>'))

  # text = <text>, {character}, </text> ;
  def text(self):
    # ------ DEBUG ------
    if self.debug:
      print("Currently in text()")

    expect(self.current_lexeme, ('TAG_OPEN', '<text>'))

    self.get_next_lexeme()

    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    self.string()
    
    expect(self.current_lexeme, ('TAG_CLOSE', '</text>'))

  def string(self):
    # ------ DEBUG ------
    if self.debug:
      print("Currently in string()")

    text = self.current_lexeme[0]
    expect(text, 'TEXT')

    self.get_next_lexeme()

    # ------ DEBUG ------
    if self.debug:
      print("Got next lexeme")
      print(f"Current counter: {self.index}")
      print(f"Current lexeme: {self.current_lexeme}\n")

    text = self.current_lexeme[0]

  # check if more text exists
    while (text == 'TEXT'):
      if self.debug:
        print("More text detected")
      expect(text, 'TEXT')
      self.get_next_lexeme()

      # ------ DEBUG ------
      if self.debug:
        print("Got next lexeme")
        print(f"Current counter: {self.index}")
        print(f"Current lexeme: {self.current_lexeme}\n")

      text = self.current_lexeme[0]

  # the actual main parser
  def parse(self):
    self.quiz()