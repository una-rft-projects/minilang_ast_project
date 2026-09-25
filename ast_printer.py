"""Imprime a árvore sintática abstrata em um formato hierárquico legível."""

from ast_nodes import (
    Number, Identifier, BinaryExpression, Assignment,
    Program, Block, IfStatement, WhileLoop,
)

def print_ast(node, indent=""):
    # O recuo representa a profundidade do nó dentro da árvore.
    if isinstance(node, Program):
        print(indent + "Program")
        for statement in node.statements:
            print_ast(statement, indent + "  ")
    elif isinstance(node, Block):
        print(indent + "Block")
        for statement in node.statements:
            print_ast(statement, indent + "  ")
    elif isinstance(node, IfStatement):
        print(indent + "IfStatement")
        print(indent + "  condition:")
        print_ast(node.condition, indent + "    ")
        print(indent + "  then:")
        print_ast(node.then_branch, indent + "    ")
        if node.else_branch is not None:
            print(indent + "  else:")
            print_ast(node.else_branch, indent + "    ")
    elif isinstance(node, WhileLoop):
        print(indent + "WhileLoop")
        print(indent + "  condition:")
        print_ast(node.condition, indent + "    ")
        print(indent + "  body:")
        print_ast(node.body, indent + "    ")
    elif isinstance(node, Assignment):
        # A atribuição possui um destino e uma expressão de valor.
        print(indent + "Assignment")
        print(indent + "  target:")
        print_ast(node.target, indent + "    ")
        print(indent + "  value:")
        print_ast(node.value, indent + "    ")
    elif isinstance(node, BinaryExpression):
        # Mostra o operador e depois imprime os operandos recursivamente.
        print(indent + f"BinaryExpression({node.operator})")
        print_ast(node.left, indent + "  ")
        print_ast(node.right, indent + "  ")
    elif isinstance(node, Number):
        # Folha da árvore que contém um valor numérico.
        print(indent + f"Number({node.value})")
    elif isinstance(node, Identifier):
        # Folha da árvore que contém o nome de uma variável.
        print(indent + f'Identifier("{node.name}")')
