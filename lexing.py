# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Lexical Analysis

# <markdowncell>

# Lexical analysis takes letters from a piece of source code and converts them into a stream of tokens which are values associated with a particular type. For example '3 + 4' might turn into the token (3, integer), ('', whitespace), (+, operator), (4, integer).

# <codecell>

simple_src = '4*6 + 9*(8-1)'

# <codecell>

import re

# <codecell>

from collections import namedtuple

# <markdowncell>

# A token is defined by it's name, a pattern which is used to match it and (optional) callable which converts from the textual value of the token into a value. If this callable is None then the raw textual value of the token is used.

# <codecell>

class TokenDef(namedtuple('TokenDef', ('name', 'pattern', 'value_filter'))):
    def __repr__(self):
        return 'TokenType.' + self.name

# <codecell>

class TokenType(object):
    _defs = [
        # operators
        TokenDef('plus', '+', None),
        TokenDef('minus', '-', None),
        TokenDef('asterisk', '*', None),
        TokenDef('slash', '/', None),
        
        # other punctuation
        TokenDef('left_paren', '(', None),
        TokenDef('right_paren', ')', None),
        
        # more complex tokens
        TokenDef('integer', re.compile('[0-9]+'), int),
        TokenDef('whitespace', re.compile('[ \t]+'), None),
    ]

# <codecell>

for def_ in TokenType._defs:
    setattr(TokenType, def_.name, def_)

# <codecell>

TokenType.integer

# <markdowncell>

# Define a `Token` as a tuple of type (an attribute of 'TokenType'), a value and the slice of the input which it covers.

# <codecell>

Token = namedtuple('Token', ('type', 'value', 'slice'))

# <markdowncell>

# Define a function to return the first token from a piece of text.

# <codecell>

def first_token(text, start=0):
    """Takes some text and an optional starting position within that string and
    returns a Token representing the longest match at the front of that 
    string starting from *start*."""
    
    match_text = text[start:]
    
    token = None
    token_text = None
    
    for type_ in TokenType._defs:
        name, pattern, value_filter = type_
        if pattern is None:
            continue
        elif isinstance(pattern, str):
            if not match_text.startswith(pattern):
                continue
            match_value = pattern
        else:
            match = pattern.match(match_text)
            if not match:
                continue
            match_value = match.group(0)
        
        # see if the match value is longer than the current token's match value
        if token_text is not None and len(token_text) >= len(match_value):
            continue
        
        token_text = match_value
        if value_filter is not None:
            match_value = value_filter(match_value)
        token = Token(type_, match_value, slice(start, start + len(token_text)))
        
    return token

# <codecell>

first_token(' ')

# <codecell>

first_token('6')

# <codecell>

first_token('68')

# <codecell>

first_token('68+')

# <codecell>

first_token('+')

# <markdowncell>

# The raw lexer repeatedly calls `first_token` on the text until all the text has been consumed.

# <codecell>

def lex_raw(text):
    start = 0
    while True:
        if start >= len(text):
            break
        
        token = first_token(text, start)
        yield token
        start = token.slice.stop

# <markdowncell>

# Check that `lex_raw` is giving correct output.

# <codecell>

list(lex_raw('8+9'))

# <codecell>

list(lex_raw('8 +9'))

# <codecell>

list(lex_raw('8 + 7 / (6-8)'))

# <markdowncell>

# Define the actual function which should be exported from this module.

# <codecell>

lex = lex_raw

# <markdowncell>

# Check that the lexer can lex some real source code.

# <codecell>

src = '5+6*(8-1)/2-5'

# <codecell>

list(lex(src))

# <codecell>


