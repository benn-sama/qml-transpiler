from dataclasses import dataclass

# <option correct="true"> Functional </option>
@dataclass
class Option:
    correct: bool
    text: str

# <question>
#   <text></text>
#   <option correct="true"> Functional </option>
# </question>
@dataclass
class Question:
    text: str | None
    options: list[Option]

# <quiz>
#   <question>
#    ...
#   </question
# </quiz>
@dataclass
class Quiz:
    title: str
    question: list[Question] 