"""Declara os nós que podem formar a árvore sintática abstrata (AST)."""

from dataclasses import dataclass
from typing import Optional

# Classe-base comum para todos os elementos da AST.
class ASTNode:
    pass

# Representa um número inteiro escrito no programa.
@dataclass
class Number(ASTNode):
    value: int

# Representa o uso de uma variável pelo seu nome.
@dataclass
class Identifier(ASTNode):
    name: str

# Representa uma operação entre duas expressões, como 2 + 3.
@dataclass
class BinaryExpression(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

# Representa a atribuição do resultado de uma expressão a uma variável.
@dataclass
class Assignment(ASTNode):
    target: Identifier
    value: ASTNode

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None

@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: ASTNode

@dataclass
class Block(ASTNode):
    statements: list

@dataclass
class Program(ASTNode):
    statements: list
