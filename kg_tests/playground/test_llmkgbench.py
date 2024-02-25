from LlmKgBench.helper.turtleHelper import fixTurtle

def test_fixTurtle():

    with open('llm4kg_tests/resources/rml/test.csv.rml_broken.ttl','r') as turtle_file:
        turtle = turtle_file.read()

    fixed_turtle = fixTurtle(turtle, False, False)
    print(fixed_turtle)
