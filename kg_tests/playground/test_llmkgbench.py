from LlmKgBench.helper.turtleHelper import fixTurtle, normalizeGraph, diffNormalizedNtriples
from LlmKgBench.helper.statsHelper import calculate_precision_recall

def test_fixTurtle():

    with open('kg_tests/resources/rml/test.csv.rml.ttl','r') as turtle_file:
        turtle = turtle_file.read()

    fixed_turtle = fixTurtle(turtle, False, False)

    normalized_graph = normalizeGraph(fixed_turtle)

    print(normalized_graph)


def test_diffed():
    with open('kg_tests/resources/rml/test.nt','r') as nt1_file:
        nt1 = nt1_file.read()

    with open('kg_tests/resources/rml/test_broken_fixed.nt','r') as nt2_file:
        nt2 = nt2_file.read()

    optimal = normalizeGraph(nt1)    
    answer = normalizeGraph(nt2)

    prec, reca = calculate_precision_recall(answer.splitlines(), optimal.splitlines())
    print()
    print(prec)
    print(reca)
    pass