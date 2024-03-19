from schema import Schema, And, Use, Optional, SchemaError
from typing import Dict
from kg_core.utils.hash import Sha512Hash
import datetime, json
from kg_core.utils.log import Logger

log = Logger("Journal")

LlmEntrySchema_v1 = Schema({
    'version': 1,
    'hash': And(Use(str)),
    'prompt': {
        'message': And(Use(str)),
    },
    'completion' : {
        'message': And(Use(str)),
    },
    'meta': {
        'timestamp' : And(Use(str)),
        'model': And(Use(str)),
        'parameters' : And(Use(dict)),
        'prompt_id' : And(Use(str)),
        'prompt_vars' : And(Use(dict)),
        Optional('prev_hash'): And(Use(str)),
    }
})

LlmEntrySchema_v2 = Schema({
    'version': 2,
    'hash': And(Use(str)),
    'prompt': {
        'message': And(Use(str)),
    },
    'completion' : {
        'message': And(Use(str)),
    },
    'meta': {
        'timestamp' : And(Use(str)),
        'model': And(Use(str)),
        'parameters' : And(Use(dict)),
        'prompt_id' : And(Use(str)),
        'prompt_vars' : And(Use(dict)),
        'promt_hash' : And(Use(str)),
        'completion_hash' : And(Use(str)),
        Optional('prev_hash'): And(Use(str)),
        Optional('misc'): And(Use(str)),
    }
})

def check(schema: Schema, conf):
    try:
        schema.validate(conf)
        return True
    except SchemaError as se:
        log.error(se)
        return False
        

class LlmEntry:

    def __init__(self, dict):
        schema = None
        if dict['version'] == 1:
            schema = LlmEntrySchema_v1
        elif dict['version'] == 2:
            schema = LlmEntrySchema_v2
        else:
            raise Exception('Invalid LlmEntry version')
        
        if check(schema, dict):
            self.entry = dict
        else:
            raise Exception('Invalid LlmEntry')
        

    def get(self):
        return self.entry
    
    
    def __str__(self):
        return json.dumps(self.entry, indent=2)


def build_llmEntry_v1(model:str, prompt:str, completion:str, parameters: dict, prompt_id: str, prompt_vars: Dict[str, str], prev_hash: str=None, timestamp: datetime = None) -> LlmEntry:
    hash = Sha512Hash(model+prompt)
    dict = {
        'version': 1,
        'hash': hash,
        'prompt': {
            'message': prompt,
        },
        'completion' : {
            'message': completion,
        },
        'meta': {
            'timestamp' : datetime.datetime.now(),
            'model': model,
            'parameters' : parameters,
            'prompt_id' : prompt_id,
            'prompt_vars' : prompt_vars
        }
    }
    if prev_hash:
        dict['meta']['prev_hash'] = prev_hash
    if timestamp:
        dict['meta']['timestamp'] = timestamp
    return LlmEntry(dict)

def build_llmEntry_v2(model:str, prompt:str, completion:str, parameters: dict, prompt_id: str, prompt_vars: Dict[str, str], prev_hash: str=None, timestamp: datetime = None, misc ={}) -> LlmEntry:
    hash = Sha512Hash(model+prompt+completion)
    dict = {
        'version': 2,
        'hash': hash,
        'prompt': {
            'message': prompt,
        },
        'completion' : {
            'message': completion,
        },
        'meta': {
            'timestamp' : datetime.datetime.now(),
            'model': model,
            'parameters' : parameters,
            'prompt_id' : prompt_id,
            'prompt_vars' : prompt_vars,
            'promt_hash' : Sha512Hash(prompt),
            'completion_hash' : Sha512Hash(completion),
            'misc' : misc
        }
    }
    if prev_hash:
        dict['meta']['prev_hash'] = prev_hash
    if timestamp:
        dict['meta']['timestamp'] = timestamp
    return LlmEntry(dict)