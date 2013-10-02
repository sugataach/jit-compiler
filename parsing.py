# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Parsing

# <markdowncell>

# The `parser` takes a series of tokens from the lexical analysis stage and converts them into instances of the AST nodes in the `astnodes` module.

# <headingcell level=2>

# Token stack

# <markdowncell>

# The token stack allows individual tokens to be popped off the stack and the top-most token to be 'peeked'. It also allows saving positions for later restoration.

# <codecell>

import collections

# <codecell>

class ParseError(Exception):
    def __init__(self, message, *tokens):
        self.message = message
        self.tokens = tokens
    
    def __str__(self):
        if len(self.tokens) == 0:
            return self.message
        return '{0}-{1}: {2}'.format(self.tokens[0].slice.start, self.tokens[-1].slice.stop-1, self.message)

# <codecell>

class TokenStack(object):
    def __init__(self, tokens):
        self._tokens = list(tokens)
        self._cursor = 0
        self._cursor_stack = []
    
    def peek(self):
        try:
            return self._tokens[self._cursor]
        except IndexError:
            raise ParseError('Unexpected end of input')
    
    def pop(self):
        rv = self.peek()
        self._cursor += 1
        return rv
    
    def push_cursor(self):
        self._cursor_stack.append(self._cursor)
    
    def pop_cursor(self):
        self._cursor = self._cursor_stack.pop()

# <headingcell level=2>

# Expression parsing

# <codecell>

class ParseBase(object):
    def __init__(self, token_stack):
        self.token_stack = token_stack
        self.node = self.parse()
    
    def parse(self):
        raise NotImplementedError()
    
    def pop_expecting(self, type_):
        next_token = self.token_stack.pop()
        if next_token.type is not type_:
            raise ParseError('Unexpected token; was expecting {0}, got {1}'.format(type_, next_token.type), next_token)
        return next_token

# <codecell>

from lexing import TokenType

# <codecell>

import astnodes

# <codecell>

class IntegerLiteralExpression(ParseBase):
    def parse(self):
        int_token = self.pop_expecting(TokenType.integer)
        return astnodes.IntegerLiteral(int_token.value)

# <codecell>

from lexing import lex

# <codecell>

IntegerLiteralExpression(TokenStack(lex('5'))).node

# <codecell>

class UnaryOpExpression(ParseBase):
    def parse(self):
        op_token = self.token_stack.pop()
        if op_token.type not in [TokenType.plus, TokenType.minus]:
            raise ParseError('Expected unary operator, got {0}'.format(op_token.type), op_token)
        rhs_node = Expression(self.token_stack).node
        return astnodes.UnaryOpExpression(op_token.value, rhs_node)

# <codecell>

Expression = IntegerLiteralExpression

# <codecell>

UnaryOpExpression(TokenStack(lex('-5'))).node

# <codecell>

class BracketedExpression(ParseBase):
    def parse(self):
        self.pop_expecting(TokenType.left_paren)
        expr_node = Expression(self.token_stack).node
        self.pop_expecting(TokenType.right_paren)
        return expr_node

# <codecell>

BracketedExpression(TokenStack(lex('(5)'))).node

# <codecell>

class PrimaryExpression(ParseBase):
    def try_to_parse(self, parser):
        """Return a tuple node, success indicating the parsed AST node and whether parsing succeeded."""
        try:
            self.token_stack.push_cursor()
            return parser(self.token_stack).node, True
        except ParseError as err:
            self.token_stack.pop_cursor()
            return None, False
        
    def parse(self):
        rv, ok = self.try_to_parse(IntegerLiteralExpression)
        if ok:
            return rv
        
        rv, ok = self.try_to_parse(UnaryOpExpression)
        if ok:
            return rv
        
        rv, ok = self.try_to_parse(BracketedExpression)
        if ok:
            return rv
        
        raise ParseError(
                'Expected integer, unary operator or bracket. Got {0}'.format(self.token_stack.peek().type),
                self.token_stack.peek())

# <codecell>

Expression = PrimaryExpression

# <codecell>

Expression(TokenStack(lex('-(+5)'))).node

# <headingcell level=2>

# Binary Operators

# <codecell>

class BinaryOpExpression(ParseBase):
    _op_precedence = {
        '+': 20, '-': 20,
        '*': 30, '/': 30,
    }
    
    def parse(self):
        primary = PrimaryExpression(self.token_stack).node
        return self.parse_expression_(primary, 0)
    
    def parse_expression_(self, lhs, min_precedence):
        while self.next_is_binary_() and self.precedence_() >= min_precedence:
            op_token = self.token_stack.pop()
            rhs = PrimaryExpression(self.token_stack)
            while self.next_is_binary_() and self.precedence_() > self.precedence_(op_token):
                rhs = self.parse_expression_(rhs, self.precedence_())
            lhs = astnodes.BinaryOpExpression(lhs, op_token.value, rhs)
        return lhs
    
    def next_is_binary_(self):
        try:
            next_token = self.token_stack.peek()
        except:
            return False
        return next_token.value in BinaryOpExpression._op_precedence
    
    def precedence_(self, token = None):
        token = token or self.token_stack.peek()
        return BinaryOpExpression._op_precedence[token.value]

# <codecell>

Expression = BinaryOpExpression

# <codecell>

Expression(TokenStack(lex('-(+52)*1'))).node.to_dict()

# <codecell>


# <codecell>


