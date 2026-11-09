
'''
Calculations function
'''


def calculate(expression: str) -> str:
    """Execute the calculation
    >>> calculate("12*12")
    '144'
    >>> calculate("twelve*one")
    'Error: Invalid expression'
    >>> calculate("12/0")
    'Error: division by zero'
    """
    allowed = "0123456789+-*/(). %"
    if not all(char in allowed for char in expression):
        return "Error: Invalid expression"
    try:
        result = eval(expression) 
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
