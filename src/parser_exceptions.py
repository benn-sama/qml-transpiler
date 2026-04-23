from typing import overload

# stupid python overloading :'(
@overload
def expect(input, exp1) -> None: ...

@overload
def expect(input, exp1, exp2) -> None: ...

def expect(input, exp1, exp2=None) -> None:
    if exp2 is None: # checks if some exp2 has passed to the function 
        if input != exp1:
            raise Exception(f"\nExpected: {exp1}\n Got: {input}")
    else:            # assumes some exp2 exists
        if input != exp1 and input != exp2:
            raise Exception(f"\nExpected: {exp1} OR {exp2}\n Got: {input}")