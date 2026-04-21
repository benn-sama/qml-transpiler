from transpiler import Transpiler

def test_ast_in_transpiler():
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

  transpiler = Transpiler()

  transpiler.parse(input)
  transpiler.print()
  print("********************TEST_1********************\n")

def test_json():
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

  transpiler = Transpiler()

  transpiler.parse(input)
  transpiler.print_dict()
  print(transpiler.json_dump())
  
  

  print("********************TEST_2********************\n")



if __name__ == "__main__":
  test_ast_in_transpiler()
  test_json()