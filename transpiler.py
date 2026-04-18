from parser import Parser

class Transpiler:
  def __init__(self) -> None:
    self.parser = Parser()

  def init_file(self, input: str) -> None:
    self.parser.tokenize_file(input)
  
  def parse(self):
    self.parser.parse()