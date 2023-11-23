import llm4kg_core.api_connector.openai as oaiYLA
import openai

openai.api_key = "" #Your openai API key
prompt = """### Instruction:
    Detect the format of the following input and answer only the mimetype.
    
    ### Input:
    {data}
    
    ### Response:
    """

data = """nconst  primaryName     birthYear       deathYear       primaryProfession       knownForTitles
    nm0000001       Fred Astaire    1899    1987    soundtrack,actor,miscellaneous  tt0050419,tt0031983,tt0072308,tt0053137
    nm0000002       Lauren Bacall   1924    2014    actress,soundtrack      tt0037382,tt0075213,tt0117057,tt0038355
    nm0000003       Brigitte Bardot 1934    NULL      actress,soundtrack,music_department     tt0056404,tt0057345,tt0049189,tt0054452
    nm0000004       John Belushi    1949    1982    actor,soundtrack,writer tt0072562,tt0077975,tt0078723,tt0080455
    nm0000005       Ingmar Bergman  1918    2007    writer,director,actor   tt0069467,tt0083922,tt0050976,tt0050986
    nm0000006       Ingrid Bergman  1915    1982    actress,soundtrack,producer     tt0038109,tt0038787,tt0034583,tt0036855
    nm0000007       Humphrey Bogart 1899    1957    actor,soundtrack,producer       tt0037382,tt0043265,tt0034583,tt0042593
    nm0000008       Marlon Brando   1924    2004    actor,soundtrack,director       tt0078788,tt0047296,tt0070849,tt0068646
    nm0000009       Richard Burton  1925    1984    actor,soundtrack,producer       tt0059749,tt0061184,tt0087803,tt0057877"""

OPENA_AI_MODEL = "gpt-3.5-turbo-instruct"
DEFAULT_TEMPERATURE = 0


def run():
    response = openai.Completion.create(
    model=OPENA_AI_MODEL,
    prompt=prompt.format(data=data),
    temperature=DEFAULT_TEMPERATURE,
    max_tokens=500,
    n=1,
    stop=None,
    presence_penalty=0,
    frequency_penalty=0.1
    )
    print(response["choices"][0]["text"]) # type: ignore


run()