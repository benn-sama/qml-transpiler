import re

class Lexer:
  # defines patterns
  TOKEN_SPEC = [
    ('TAG_CLOSE',      r'</[a-zA-Z]+>'),
    ('TAG_WITH_ATTR',  r'<[a-zA-Z]+\s+[a-zA-Z]+="[^"]*">'),
    ('TAG_OPEN',       r'<[a-zA-Z]+>'),
    ('NEWLINE',        r'\n'),
    ('WHITESPACE',     r'\s+'),
    ('TEXT',           r'[^<]+'),
  ]

  # combines patterns in TOKEN_SPEC
  master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
  regex = re.compile(master_pattern)

  # scan and extract (can extract all, or just one line)
  def tokenize(self, input:str) -> tuple:
    tokens = ()

    # give inputs/values and assign their types, then return list of token
    for match in self.regex.finditer(input):
      type  = match.lastgroup
      value = match.group()

      # this part ignores whitespace and new lines
      if type == 'WHITESPACE' or type == 'NEWLINE':
        continue
    
      tokens = (type, value)

    return tokens