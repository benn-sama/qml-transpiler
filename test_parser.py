from parser_debug import Parser

def tokenize_test():
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
  
  parser = Parser()

  # tokenize the input
  parser.tokenize_file(input)

  # prints all tokens
  parser.print()
  print("********************TEST_1********************\n")

def test_ast():
  print("********************TEST_2********************")
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

  parser = Parser()
  ast = parser.parse(input)

  print(ast)
  print("********************TEST_2********************\n")

def test_the_whole_damn_thing():
  print("********************TEST_3********************")
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

  parser = Parser(True)
  parser.parse(input)
  print("********************TEST_3********************\n")



if __name__ == "__main__":
  tokenize_test()
  test_ast()
  test_the_whole_damn_thing()