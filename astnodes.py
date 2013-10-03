# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Abstract Syntax Tree

# <markdowncell>

# The abstract syntax tree defines a set of nodes which represent an individual semantic component of our language. Each node allows for code generation and for generating a description of the tree and from then on.

# <markdowncell>

# Expression nodes

# <codecell>

import collections

# <codecell>

class IntegerLiteral(collections.namedtuple('IntegerLiteral', 'value')):
    def to_dict(self):
        return { 'type': 'IntegerLiteral', 'value': self.value }

# <codecell>

IntegerLiteral(5).to_dict()

# <codecell>

class UnaryOpExpression(collections.namedtuple('UnaryOpExpression', ('op', 'rhs'))):
    def to_dict(self):
        return { 'type': 'UnaryOpExpression', 'op': self.op, 'rhs': self.rhs.to_dict() }

# <codecell>

UnaryOpExpression('-', IntegerLiteral(7))

# <codecell>

UnaryOpExpression('-', IntegerLiteral(7)).to_dict()

# <codecell>

class BinaryOpExpression(collections.namedtuple('BinaryOpExpression', ('lhs', 'op', 'rhs'))):
    def to_dict(self):
        return { 'type': 'BinaryOpExpression', 'lhs': self.lhs.to_dict(), 'op': self.op, 'rhs': self.rhs.to_dict() }

# <codecell>

BinaryOpExpression(lhs=IntegerLiteral(6), op='-', rhs=IntegerLiteral(7))

# <codecell>

BinaryOpExpression(lhs=IntegerLiteral(6), op='-', rhs=IntegerLiteral(7)).to_dict()

# <codecell>


