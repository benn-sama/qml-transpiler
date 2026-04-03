import re

class Lexer:
  # defines patterns
  TOKEN_SPEC = [
    ('TAG_CLOSE',      r'</[a-zA-Z]+>'),
    ('TAG_WITH_ATTR',  r'<[a-zA-Z]+\s+[a-zA-Z]+="[^"]*">'),
    ('TAG_OPEN',       r'<[a-zA-Z]+>'),
    ('TEXT',           r'[^<]+'),
    ('WHITESPACE',     r'\s+'),
  ]

  # combines patterns in TOKEN_SPEC
  master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
  regex = re.compile(master_pattern)

  # scan and extract 
  def tokenize(self, input:str ) -> list:
    tokens = []

    # give inputs/values and assign their types, then return list of token
    for match in self.regex.finditer(input):
      type  = match.lastgroup
      value = match.group()

      # this part ignores whitespace
      if type == 'WHITESPACE':
        continue
    
      tokens.append((type, value))

    return tokens