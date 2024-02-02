from llm4kg_tasks.map.llm4rml import LLM4RML

llm4rml = LLM4RML({
    'input': 'examples/artist/artist-map.ttl',
    'output': 'examples/artist/artist-map.ttl',
    'name': 'llm4rml',
    'type': 'config generation'
})

llm4rml.run()