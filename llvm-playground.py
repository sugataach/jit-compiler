# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import llvm
import llvm.core as lc

# <codecell>

m = lc.Module.new('test')

# <codecell>

print m

# <codecell>

float32 = lc.Type.float()

# <codecell>

eval_func = lc.Type.function(float32, (float32,))

# <codecell>

f = m.add_function(eval_func, 'test1')

# <codecell>

print m

# <codecell>

bb = f.append_basic_block('entry')

# <codecell>

print m

# <codecell>

ib = lc.Builder.new(bb)

# <codecell>

add_2 = ib.fadd(f.args[0], lc.Constant.real(float32, 2.0))

# <codecell>

print m

# <codecell>

ib.ret(add_2)

# <codecell>

print m

# <codecell>

import llvm.ee as lee

# <codecell>

eb = lee.EngineBuilder.new(m)

# <codecell>

ee = eb.create()

# <codecell>

rv = ee.run_function(m.get_function_named('test1'), (lee.GenericValue.real(float32, 50) ,))

# <codecell>

rv.as_real(float32)

# <codecell>


