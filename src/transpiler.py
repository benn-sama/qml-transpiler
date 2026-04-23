import json
from dataclasses import asdict

from .parser import Parser

class Transpiler:
  def __init__(self) -> None:
    self.parser = Parser()
    self.ast = None
  
  def parse(self, file):
    self.ast = self.parser.parse(file)

    return self.json_dump()

  def print(self):
    print(self.ast)

  def json_dump(self):
    if self.ast is None:
      return
    
    return json.dumps(asdict(self.ast), indent=4)
  
  def print_dict(self):
    print(asdict(self.ast)) # type: ignore