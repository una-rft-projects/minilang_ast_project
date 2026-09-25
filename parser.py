# Teoria da Computação e Compiladores
# Aluno: Pedro Elias de Araújo Correa
# RA: 202612345
# Data: 25/09/2026
# Assinatura de presença — Atividade: MiniLang if/else/while e AST

"""Analisa tokens e constrói a árvore sintática abstrata da MiniLang."""

from ast_nodes import (
    Number, Identifier, BinaryExpression, Assignment,
    Program, IfStatement, WhileLoop, Block,
)

# Parser descendente recursivo para a gramática das expressões da linguagem.
class Parser:
    def __init__(self, tokens):
        # A lista de tokens é consumida da esquerda para a direita.
        self.tokens = tokens
        # Indica qual token será analisado pelo próximo método.
        self.position = 0

    def current(self):
        # Retorna o token atual ou None quando todos já foram consumidos.
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def consume(self, tipo):
        # Confere o tipo esperado e avança a posição em caso de sucesso.
        token = self.current()
        if token is None:
            raise SyntaxError(f"Esperado {tipo}, mas a entrada terminou.")
        if token.tipo != tipo:
            raise SyntaxError(f"Esperado {tipo}, encontrado {token.tipo} ({token.valor}).")
        self.position += 1
        return token

    def parse(self):
        statements = []
        while self.current() is not None:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current()
        if token is None:
            raise SyntaxError("Fim inesperado da instrução.")
        if token.tipo == "IF":
            return self.parse_if()
        if token.tipo == "WHILE":
            return self.parse_while()
        if token.tipo == "ABRE_CHAVE":
            return self.parse_block()
        return self.parse_assignment()

    def parse_if(self):
        self.consume("IF")
        self.consume("ABRE_PARENTESES")
        condition = self.parse_expression()
        self.consume("FECHA_PARENTESES")
        then_branch = self.parse_statement()
        else_branch = None
        if self.current() and self.current().tipo == "ELSE":
            self.consume("ELSE")
            else_branch = self.parse_statement()
        return IfStatement(condition, then_branch, else_branch)

    def parse_while(self):
        self.consume("WHILE")
        self.consume("ABRE_PARENTESES")
        condition = self.parse_expression()
        self.consume("FECHA_PARENTESES")
        body = self.parse_statement()
        return WhileLoop(condition, body)

    def parse_block(self):
        self.consume("ABRE_CHAVE")
        statements = []
        while self.current() and self.current().tipo != "FECHA_CHAVE":
            statements.append(self.parse_statement())
        self.consume("FECHA_CHAVE")
        return Block(statements)

    def parse_assignment(self):
        # Uma atribuição segue o formato: identificador = expressão ;
        nome = self.consume("IDENTIFICADOR")
        self.consume("ATRIBUICAO")
        valor = self.parse_expression()
        self.consume("PONTO_E_VIRGULA")
        return Assignment(Identifier(nome.valor), valor)

    def parse_expression(self):
        # Comparações têm menor precedência que + e -
        left = self.parse_additive()
        while self.current() and self.current().tipo in ("MENOR", "MAIOR", "IGUAL"):
            op = self.current().valor
            self.position += 1
            right = self.parse_additive()
            left = BinaryExpression(left, op, right)
        return left

    def parse_additive(self):
        left = self.parse_term()
        while self.current() and self.current().tipo in ("SOMA", "SUBTRACAO"):
            op = self.current().valor
            self.position += 1
            right = self.parse_term()
            left = BinaryExpression(left, op, right)
        return left

    def parse_term(self):
        # Um termo agrupa fatores ligados por multiplicação ou divisão.
        left = self.parse_factor()
        while self.current() and self.current().tipo in ("MULTIPLICACAO", "DIVISAO"):
            op = self.current().valor
            self.position += 1
            right = self.parse_factor()
            left = BinaryExpression(left, op, right)
        return left

    def parse_factor(self):
        # Fatores são números, variáveis ou expressões entre parênteses.
        token = self.current()
        if token is None:
            raise SyntaxError("Fim inesperado da expressão.")
        if token.tipo == "NUMERO":
            # A AST guarda números como inteiros, não como texto.
            self.position += 1
            return Number(int(token.valor))
        if token.tipo == "IDENTIFICADOR":
            # A resolução do valor da variável fica para o interpretador.
            self.position += 1
            return Identifier(token.valor)
        if token.tipo == "ABRE_PARENTESES":
            # Os parênteses alteram a ordem natural de avaliação.
            self.position += 1
            expr = self.parse_expression()
            self.consume("FECHA_PARENTESES")
            return expr
        raise SyntaxError(f"Token inesperado: {token.tipo} ({token.valor})")
