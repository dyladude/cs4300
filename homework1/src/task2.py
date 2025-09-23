"""
Task 2: Variables & Data Types
Return a few example values showcasing common Python types.
"""

def types_demo():
    an_int = 42
    a_float = 3.14
    a_string = "python"
    a_bool = True
    return {
        "an_int": an_int,
        "a_float": a_float,
        "a_string": a_string,
        "a_bool": a_bool,
    }

if __name__ == "__main__":
    vals = types_demo()
    for k, v in vals.items():
        print(f"{k}: {v} ({type(v).__name__})")
