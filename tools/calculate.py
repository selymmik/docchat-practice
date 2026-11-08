
'''
Calculations function
'''


def calculate(expression: str) -> str:
    """Execute the calculation
    >>> calculate("12*12")
    '144'
    >>> calculate("twelve*one")
    "Error: name 'twelve' is not defined"
    """
    try:
        result = eval(expression)  # Use safe evaluation in production
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
