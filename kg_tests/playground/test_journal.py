from kg_core.utils.journal import build_llmEntry_v1, build_llmEntry_v2
import json

def test_llm_entry_v1():
    
    entry = build_llmEntry_v1("gpt-3.5", "Say Hi!", "Hi", {"temperature": 0}, "say_hi_prompt", {"DATA": "./some/file"}).get()
    print(json.dumps(entry, indent=2, default=str))
    assert entry

    hash = entry['hash']
    chained_entry = build_llmEntry_v1("gpt-3.5", "How are you?", "Good, and you?", {"temperature": 0}, "how_are_prompt", {"DATA": "./some/file2"}, prev_hash=hash).get()
    print(json.dumps(chained_entry, indent=2, default=str))
    assert chained_entry

def test_llm_entry_v2():
    entry = build_llmEntry_v2("gpt-3.5", "Say Hi!", "Hi", {"temperature": 0}, "say_hi_prompt", {"DATA": "./some/file"}, misc={"key": "value"}).get()
    print(json.dumps(entry, indent=2, default=str))
    assert entry

    hash = entry['hash']
    chained_entry = build_llmEntry_v2("gpt-3.5", "How are you?", "Good, and you?", {"temperature": 0}, "how_are_prompt", {"DATA": "./some/file2"}, prev_hash=hash, misc={"key": "value"}).get()
    print(json.dumps(chained_entry, indent=2, default=str))
    assert chained_entry