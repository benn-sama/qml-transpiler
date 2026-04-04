from lexer import Lexer

def test_1(lexer: Lexer):
  print("********************TEST_1********************")
  input = """<quiz>
    <title> Programming Languages Midterm </title>
    
    <question>
        <text> Which programming paradigm is based on mathematical functions? </text>
        <option> Imperative </option>
        <option correct="true"> Functional </option>
        <option> Object-Oriented </option>
    </question>

    <question>
        <text> What is the primary purpose of a lexical analyzer? </text>
        <option correct="true"> To group characters into lexemes and assign tokens. </option>
        <option> To generate machine code. </option>
        <option> To build a parse tree. </option>
    </question>
</quiz>"""

  tokenized = lexer.tokenize(input)
  
  for t in tokenized:
    print(t)
    
  print("********************TEST_1********************")

def test_2(lexer: Lexer):
  print("********************TEST_2********************")

  input = """<quiz>
    <title> Programming Languages Midterm </title>

    <question>
        <text> What is the primary purpose of a lexical analyzer? </text>
    </question>
</quiz>"""
  
  tokenized = lexer.tokenize(input)
  for t in tokenized:
    print(t)

  print("********************TEST_2********************")

def test_3(lexer: Lexer):
  print("********************TEST_3********************")

  input = """<quiz>
  <title> Programming Languages Midterm </title>
</quiz>"""

  tokenized = lexer.tokenize(input)
  for t in tokenized:
    print(t)
  
  print("********************TEST_3********************")

if __name__ == "__main__":
  lexer = Lexer()
  
  test_1(lexer)
  test_2(lexer)
  test_3(lexer)