import re
from unidecode import unidecode


def verify_outside_block(line:str, has_main:bool, in_function:bool):
    if verify_include(line) or verify_vars(line):
        return True, has_main, in_function
    elif verify_main(line):
        return True, True, True
    elif verify_function(line):
        return True, has_main, True
    return False, has_main, in_function
    

def verify_in_block(line:str, in_block:bool):
    if verify_if(line):
        return True,True
    elif verify_while(line):
        return True, True
    elif verify_for(line):
        return True,True
    elif verify_printf(line):
        return True,in_block
    elif verify_scanf(line):
        return True,in_block
    elif verify_operations(line):
        return True,in_block
    elif verify_vars(line):
        return True,in_block
    elif verify_loop_controllers(line):
        return True,in_block
    elif verify_increment_operation(line):
        return True,in_block
    elif verify_return(line):
        return True,in_block
    else:
        return False,False


def verify_include(line:str):
    include_pattern = r"#include\s*<[A-Za-z]\w*.h>"
    return re.match(include_pattern, line)


def verify_main(line:str):
    main_function_pattern = r"(int|char|float|double|void)\s*main\(((int|float|double|char|void)\s+[A-Za-z]\w*\s*(,\s*(int|float|double|char|void)\s+[A-Za-z]\w*)?)?\){"
    return re.match(main_function_pattern, line)


def verify_function(line:str):
    function_pattern = r"(int|float|double|char|void)\s+[A-Za-z]\w*\s*\(((int|float|double|char|void)\s+[A-Za-z]\w*\s*(,\s*(int|float|double|char|void)\s+[A-Za-z]\w*)?)?\)\s*{"
    return re.match(function_pattern, line)


def verify_still_in_function_or_block(line:str):
    still_in_function_or_block_pattern = r"\s*}\s*"
    return re.match(still_in_function_or_block_pattern, line)


def verify_if(line:str):
    if_pattern = r"if\s*\(\s*[A-Za-z]\w*\s*(==|!=|>=|>|<|<=)\s*('?[A-Za-z0-9_*\-+#\"$@%&*\(\)]*'?|\"?\s*[A-Za-z0-9_*\-+#$@%&'*\(\)]*\"?)(\s*((\|\||&&))*(\s*[A-Za-z]\w*\s*(==|!=|>=|>|<|<=)\s*('?[A-Za-z0-9_*\-+#\"$@%&*\(\)]*'?|\"?\s*[A-Za-z0-9_*\-+#$@%&'*\(\)]*\"?)))*\s*\)\s*{"
    return re.match(if_pattern, line)


def verify_while(line:str):
    while_pattern = r"while\s*\(\s*[A-Za-z]\w*\s*(==|!=|>=|>|<|<=)\s*('?[A-Za-z0-9_*\-+#\"$@%&*\(\)]*'?|\"?\s*[A-Za-z0-9_*\-+#$@%&'*\(\)]*\"?)(\s*((\|\||&&))*(\s*[A-Za-z]\w*\s*(==|!=|>=|>|<|<=)\s*('?[A-Za-z0-9_*\-+#\"$@%&*\(\)]*'?|\"?\s*[A-Za-z0-9_*\-+#$@%&'*\(\)]*\"?)))*\s*\)\s*{"
    return re.match(while_pattern, line)


def verify_for(line:str):
    for_pattern = r"for\(\s*((int)?\s*[A-Za-z]\w*\s*=\s*\d*)?;(\s*[A-Za-z]\w*\s*[>|<|>=|<=|==|!=]\s*\d*)?;(\s*[A-Za-z]\w*\s*((\+=|\*=|/=|%=)\s*\d*|(\+\+|--)))?\s*\)\s*{"
    return re.match(for_pattern, line)


def verify_printf(line:str):
    printf_pattern = r"printf\(\s*\"[A-Za-z0-9 _*\-+#:$@%.&'*\(\)]*\"(\s*,\s*[A-Za-z]\w*\s*)*\);"
    return re.match(printf_pattern, line)


def verify_scanf(line:str):
    scanf_pattern = r"scanf\(\s*\"[A-Za-z0-9 _*\-+#:$@%.&'*\(\)]*\"(\s*,\s*[&,*]*[A-Za-z]\w*\s*)*\);"
    return re.match(scanf_pattern, line)


def verify_operations(line:str):
    operation_pattern = r"[A-Za-z]\w*\s*=\s*(\(([A-Za-z]\w*|\d*)\s*(\s*[+-/*%]\s*([A-Za-z]\w*|\d*)*)*\))*(([A-Za-z]\w*|\d*)\s*(\s*[+-/*%]\s*([A-Za-z]\w*|\d*)*))*(\(([A-Za-z]\w*|\d*)\s*(\s*[+-/*%]\s*([A-Za-z]\w*|\d*)*)*\))*\s*;"
    return re.match(operation_pattern, line)


def verify_vars(line:str):
    var_pattern = r"(((int\s+)[A-Za-z]\w*(\s*=\s*\d*)?)|((float|double)\s+)[A-Za-z_]\w*(\s*=\s*\d*(.\d*)?)?|(char\s+)[A-Za-z_]\w*(\s*=\s*'[A-Za-z0-9_*\-+#\"$@%&*\(\)]*')?)(\s*,\s*(((int\s+)?[A-Za-z]\w*(\s*=\s*\d*)?)|((float|double)\s+)?[A-Za-z_]\w*(\s*=\s*\d*(.\d*)?)?|(char\s+)?[A-Za-z_]\w*(\s*=\s*'[A-Za-z0-9_*\-+#\"$@%&*\(\)]*')?)*)*;"
    return re.match(var_pattern, line)

def verify_loop_controllers(line:str):
    loop_control_pattern = r"(break|continue)\s*;"
    return re.match(loop_control_pattern, line)


def verify_increment_operation(line:str):
    increment_operation_pattern = r"\s*[A-Za-z]\w*\s*((\+=|\*=|/=|%=)\s*\d*|(\+\+|--))"
    return re.match(increment_operation_pattern, line)


def verify_return(line:str):
    return_pattern = r"\s*return\s*([A-Za-z]\w*|\d*|\"[A-Za-z0-9_*\-+#\"$@%&*\(\)]*\"|\'[A-Za-z0-9_*\-+#\"$@%&*\(\)]*\');"
    return re.match(return_pattern, line)


def verify_comment(line:str):
    comment_pattern = r"//.*"
    return re.match(comment_pattern, line)


def print_not_valid_message(i:int, line:str):
    print('Código Inválido')
    print(f'Erro na linha: {i + 1}:')
    print(line)


if __name__ == '__main__':
    in_function = False
    has_main = False
    in_block = False
    with open('file.c', 'r') as f:
        for i, line in enumerate(f):
            line = unidecode(line.strip())

            if not line:
                continue
            elif verify_comment(line):
                continue
            elif in_block:
                if verify_still_in_function_or_block(line):
                    in_block = False
                    continue
            elif in_function:
                if verify_still_in_function_or_block(line):
                    in_function = False
                    continue
            
            if in_block or in_function:
                valid,in_block = verify_in_block(line, in_block)
            else:
                valid,has_main,in_function = verify_outside_block(line, has_main, in_function)

            if not valid:
                print_not_valid_message(i, line)
                exit()
 
    if has_main and not in_function and not in_block:
        print('Código Válido')
    else:
        print('Código Inválido')
