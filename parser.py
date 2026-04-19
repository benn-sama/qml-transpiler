from typing import overload
import re
import logging

from lexer import Lexer

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
    self.logger         = logging.getLogger(__name__) # init python logger

    if debug: 
      logging.basicConfig(level=logging.DEBUG) # allows logger to actually print logs here

      self.logger.debug(
         "\nParser class initialized\n" \
         "---Instance Variables---\n" \
         "lexer = %s\n" \
         "tokens = %s\n" \
         "index = %s\n" \
         "current_lexeme = %s\n" \
         "logger = %s\n",
         type(self.lexer),
         type(self.tokens),
         self.index,
         type(self.current_lexeme),
         type(self.logger)
      )


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

  # ---------- THIS FUNCTION IS FOR TESTING TOKENIZER ----------
  def print(self):
    print(self.tokens)

  # quiz = "<quiz>", quiz_block ,"</quiz>" ;
  def quiz(self):

    # ------ DEBUG ------
    self.logger.debug(
      "\nquiz(): Just started - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\nquiz(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    # <quiz>
    expect(self.current_lexeme, ('TAG_OPEN', '<quiz>'))

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\nquiz(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.quiz_block()

    # ------ DEBUG ------
    self.logger.debug(
      "\nquiz(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    # </quiz>
    expect(self.current_lexeme, ('TAG_CLOSE', '</quiz>'))
  
  # quiz_block = title, question, {question} ; 
  def quiz_block(self):
    # ------ DEBUG ------
    self.logger.debug(
      "\nCurrently in quiz_block()\n",
    )

    self.title()

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\nquiz_block(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.question()

    # optional: may have additional questions
    self.get_next_lexeme()
    while (self.current_lexeme == ('TAG_OPEN', '<question>')):
      self.question()
      self.get_next_lexeme()

      # ------ DEBUG ------
      self.logger.debug(
        "\nGot next lexeme\nquiz_block(): - index: %s, lexeme: %s \n",
        self.index, self.current_lexeme
      )

  # title = "<title>", text, "</title>" ;
  def title(self):
    # ------ DEBUG ------
    self.logger.debug(
      "\nCurrently in title()\n"
    )

    # <title>
    expect(self.current_lexeme, ('TAG_OPEN', '<title>'))

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\ntitle(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.string()

    # </title>
    expect(self.current_lexeme, ('TAG_CLOSE', '</title>'))

  # = "<question>", question_block, "</question>" ;
  def question(self):
    # ------ DEBUG ------
    self.logger.debug(
      "\nCurrently in question()\n"
    )

    # <question>
    expect(self.current_lexeme, ('TAG_OPEN', '<question>'))

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\nquestion(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.question_block()

    # </question>
    expect(self.current_lexeme, ('TAG_CLOSE', '</question>'))

  # question_block = text, option, option, {option} ;
  def question_block(self):
    # ------ DEBUG ------
    self.logger.debug(
      "\nCurrently in question_block()\n"
    )

    self.text()

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\nquestion_block(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.option()

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\nquestion_block(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.option()

  # optional: may have additonal option
    self.get_next_lexeme()
    while (self.current_lexeme[0] == 'TAG_OPEN' or self.current_lexeme[0] == 'TAG_WITH_ATTR'):
      self.option()
      self.get_next_lexeme()

      # ------ DEBUG ------
      self.logger.debug(
        "\nGot next lexeme\nquestion_block(): - index: %s, lexeme: %s \n",
        self.index, self.current_lexeme
      )

  # option = "<option ", {correct="true"}, ">", text, "</option"> ;
  def option(self):
    # ------ DEBUG ------
    self.logger.debug(
      "\nCurrently in option()\n"
    )

    # <option>
    expect(self.current_lexeme, ('TAG_OPEN', '<option>'), ('TAG_WITH_ATTR', '<option correct="true">'))

      
    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\noption(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.string()

    # </option>
    expect(self.current_lexeme, ('TAG_CLOSE', '</option>'))

  # text = <text>, {character}, </text> ;
  def text(self):
    # ------ DEBUG ------
    self.logger.debug(
      "\nCurrenlty in text()"
    ) 

    expect(self.current_lexeme, ('TAG_OPEN', '<text>'))

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\ntext(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    self.string()
    
    expect(self.current_lexeme, ('TAG_CLOSE', '</text>'))

  def string(self):
    # ------ DEBUG ------
    self.logger.debug(
      "\nCurrently in string()\n"
    )

    text = self.current_lexeme[0]

    # Type: STRING
    expect(text, 'STRING')

    self.get_next_lexeme()

    # ------ DEBUG ------
    self.logger.debug(
      "\nGot next lexeme\nstring(): - index: %s, lexeme: %s \n",
      self.index, self.current_lexeme
    )

    text = self.current_lexeme[0]

  # check if more text exists
    while (text == 'STRING'):
      self.logger.debug(
         "\nMore STRING detected"
      )

      # Type: STRING
      expect(text, 'STRING')
      self.get_next_lexeme()

      # ------ DEBUG ------
      self.logger.debug(
        "\nGot next lexeme\nstring(): - index: %s, lexeme: %s \n",
        self.index, self.current_lexeme
      )

      text = self.current_lexeme[0]

  # the actual main parser
  def parse(self):
    self.logger.debug(
       "\nParser started\n"
    )

    self.quiz()