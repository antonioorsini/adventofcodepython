instructions = """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

instructions = instructions.split('\n')

for i in instructions:
    if i in ['']:
        instructions.remove(i)

import numpy as np

formulas = []
solutions = []
for line in instructions:
    formula = line.split('=>')
    inputs = formula[0].split(',')
    outputs = formula[1].split(',')

    formula = {}

    inputs = [i.strip() for i in inputs]
    inputs = [ {inp.split(' ')[1] : int(inp.split(' ')[0]) } for inp in inputs ]

    outputs = [i.strip() for i in outputs]
    outputs = [ {out.split(' ')[1] : - int(out.split(' ')[0]) } for out in outputs ]

    inout = inputs + outputs

    for form in inout:
        formula.update(form)

    if 'FUEL' not in formula:
        sols = 0
        if 'ORE' in formula.keys():
            sols = -formula['ORE']
            del formula['ORE']
    else:
        sols = 1
        del formula['FUEL']
    
    solutions.append(sols)


    formulas.append( formula )


elements = []
for formula in formulas:
    for spec in formula.keys():
        if spec not in elements:
            elements.append( spec )    

# rewrite formulas
formulas_complete = []
for formula in formulas:    
    formula_complete = np.zeros(len(elements))
    arrayidx = 0
    for element in elements:
        if element in formula.keys():
            formula_complete[arrayidx] =  int(formula[element] )
        else:
            formula_complete[arrayidx] =  int( 0 ) 
        arrayidx += 1

    formulas_complete.append(formula_complete)
print(np.array( formulas_complete ), np.array(solutions) )


solution = np.linalg.inv(np.array( formulas_complete )).dot(np.zeros(len(formulas_complete)))
print(solution)