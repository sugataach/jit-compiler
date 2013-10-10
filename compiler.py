# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

from parsing import Expression, TokenStack
from lexing import lex
from astnodes import float32

# <codecell>

def parse_expression(text):
    return Expression(TokenStack(lex(text))).node

# <codecell>

import llvm.core as lc
import llvm.ee as lee

# <codecell>

class Context(object):
    def __init__(self, ib):
        self.ib = ib

# <codecell>

def add_expression_function(text, module, name = 'eval_expr'):
    expr = parse_expression(text)
    ret_type = lc.Type.float()
    fun_type = lc.Type.function(ret_type, ())
    f = module.add_function(fun_type, name)
    bb = f.append_basic_block('entry')
    ib = lc.Builder.new(bb)
    rv = expr.to_value(Context(ib))
    ib.ret(rv)
    return f

# <codecell>

Expression(TokenStack(lex('4*5+3*(2+1)'))).node

# <codecell>

def eval_expression(text):
    m = lc.Module.new('test')
    f = add_expression_function(text, m)
    eb = lee.EngineBuilder.new(m)
    ee = eb.create()
    rv = ee.run_function(f, ())
    return rv.as_real(float32)

# <codecell>

eval_expression('((2+5)*2+9) / 2')

# <codecell>


