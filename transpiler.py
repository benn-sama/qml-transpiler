from parser import Parser
from nodes import Quiz

class Transpiler:
  def __init__(self) -> None:
    self.parser = Parser()
    self.ast = Quiz
  
  def parse(self, file: str):
    self.ast = self.parser.parse(file)