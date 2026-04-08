from lexer import Lexer
"""<quiz>
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


def test_open(lexer: Lexer):
  print("********************TEST_1********************")
  input = ['<quiz>', '<title>', '<question>', '<text>', '<option>']

  # print tuple
  
    
  print("********************TEST_1********************")

def test_open_with_attr(lexer: Lexer):
  print("********************TEST_2********************")

  input = "<title>"
  
  # print tuple
  tokenized = lexer.tokenize(input)
  print(tokenized)

  print("********************TEST_2********************")

def test_close(lexer: Lexer):
  print("********************TEST_3********************")

  input = "<text> What is the primary purpose of a lexical analyzer? </text>"

  # print tuple
  tokenized = lexer.tokenize(input)
  print(tokenized)
  
  print("********************TEST_3********************")

if __name__ == "__main__":
  lexer = Lexer()
  
  test_open(lexer)
  test_open_with_attr(lexer)
  test_close(lexer)