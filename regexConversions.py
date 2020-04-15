"""
    Assume that the data structure for representing a regular expression is the next
    reg_exp:= {‘key’ : ‘atm’, ‘val’ : token}
            | {‘key’ : ‘|’, ‘val’ : {‘fst’ : reg_expr, ‘snd’ : reg_expr}}
            | {‘key’ : ‘.’, ‘val’ : {‘fst’ : reg_expr, ‘snd’ : reg_expr}}
            | {‘key’ : ‘*’, ‘val’ : reg_expr}
    1. The function printing the correspondent regular expression under the following assumption:
    Priority is following: ‘*’ > ‘.’ > ‘|’
    ‘*’ is postfix
    ‘.’ and ‘|’ are left associative
    is implemented.
    2. The function transforming a correct string presentation for a regular expression into the data structure
    described above is implemented.
"""

import json


def conversion_reg_expr_to_str(reg_expr: dict) -> str:
    """ The function convert regular expression to string representation
        :param reg_expr: dict -- the regular expression represented in JSON format in dict.
        :return: regular expression represented in string representation.
    """
    key = reg_expr['key']
    value = reg_expr['val']
    if key == 'atm':
        return value
    elif key == '*':
        if value['key'] == 'atm':
            return conversion_reg_expr_to_str(value) + '*'
        return '(' + conversion_reg_expr_to_str(value) + ')*'
    elif key == '.':
        fst = conversion_reg_expr_to_str(value['fst'])
        snd = conversion_reg_expr_to_str(value['snd'])
        if value['fst']['key'] == '|':
            fst = '(' + fst + ')'
        if value['snd']['key'] == '|':
            snd = '(' + snd + ')'
        return fst + '.' + snd
    elif key == '|':
        return conversion_reg_expr_to_str(value['fst']) + '|' + conversion_reg_expr_to_str(value['snd'])


def conversion_reg_expr_to_json(reg_expr: str) -> dict:
    """
        Task A.2 (advanced)
        The function transforming a correct string presentation for
          a regular expression represented in JSON format.
        :param reg_expr: str -- the infix regular expression represented in string format
        :return: regular expression represented in JSON format in dict.
    """
    # convert regular expression to postfix one
    reg_expr = conversion_to_postfix_expr(reg_expr)
    stack = []
    """
        for each token in the postfix expression:
            if token is an operator then:
                the corresponding operation is performed 
                    on the required number of values extracted from the stack,
                    taken in the order of adding;
                push result back onto the stack;
            else if token is an operand then:
                it is placed on the top of the stack.
        result of evaluating the expression lies on top of the stack
    """
    for char in reg_expr:
        if char == '*':
            value = stack.pop()
            new_value = {"key": "*", "val": value}
            stack.append(new_value)
        elif char == '.' or char == '|':
            second = stack.pop()
            first = stack.pop()
            new_value = {"key": char, "val": {"fst": first, "snd": second}}
            stack.append(new_value)
        else:
            new_value = {"key": "atm", "val": char}
            stack.append(new_value)
    return stack.pop()


def conversion_to_postfix_expr(reg_expr: str) -> str:
    """ The function transforming an infix regular expression to postfix one
        :param reg_expr: str -- the infix regular expression represented in string format
        :return: postfix regular expression represented in string format
    """
    # priority of operations
    priority_operations = {'*': 1, '.': 2, '|': 3, '(': 4, ')': 4}

    # resulting postfix regular expression
    postfix_reg_expr = ""
    stack = []
    """
        for each token in the infix expression:
            if the token is a number or a postfix function:
                add it to the resulting string.
            else if the token is an opening bracket:
                put it on the stack.
            else if token is an closing bracket:
                until the opening bracket becomes the top element of the stack:
                    push the elements from the stack to the resulting string;
                opening bracket is removed from the stack
            else if token is a binary operation:
                while the operation on top of the stack is prioritized:
                    push the top element of the stack into the resulting string.
        push all the characters from the stack to the resulting string.
    """
    for char in reg_expr:
        if char == '(':
            stack.append('(')
        elif char == ')':
            while stack[-1] != '(':
                postfix_reg_expr += stack.pop()
            stack.pop()
        elif char == '.' or char == '|':
            while len(stack) > 0 and priority_operations[char] > priority_operations[stack[-1]]:
                postfix_reg_expr += stack.pop()
            stack.append(char)
        elif char == '*' or char != ' ':
            postfix_reg_expr += char
    while len(stack) > 0:
        postfix_reg_expr += stack.pop()
    return postfix_reg_expr


def get_data_from_json_file(name_file: str) -> dict:
    """ The function reads the regular expression represented in JSON format.
        :param name_file: str -- the name of the file
        :return: decoded regular expression
    """
    with open(name_file, "r") as read_file:
        return json.load(read_file)


def get_data_from_txt_file(name_file: str) -> str:
    """ The function reads the regular expression represented in string format.
        :param name_file: str -- the name of the file
        :return: regular expression represented in string format
    """
    with open(name_file, "r") as read_file:
        return read_file.readline()


'''
 Printing the corresponding regular expression in string representation
 from regular expression in JSON representation.
'''
reg_expr_str = conversion_reg_expr_to_str(get_data_from_json_file("reg_expr.json"))
print(reg_expr_str)

'''
 Printing the corresponding regular expression in JSON representation 
 from regular expression in string representation.
'''
reg_expr_json = conversion_reg_expr_to_json(get_data_from_txt_file("reg_expr.txt"))
print(reg_expr_json)
