# Bindings for sub processes

from dataclasses import dataclass
import json
import subprocess
from ..bindings.binding import Binding

@dataclass
class BindingConfig:
    requirement: []
    name: str


# class BindingCreator:

#     def __init__(self, config_file):


#         self.config_file = config_file

#     def create_bindings(self):
#         # Read the configuration file and extract the necessary information
#         # to create the bindings
#         config = self.read_configuration()

#         # Logic to create bindings based on the configuration file
#         bindings = self.generate_bindings(config)

#         # Return the created bindings
#         return bindings

#     def read_configuration(self):
#         # Read the configuration file and extract the necessary information
#         # to create the bindings
#         with open(self.config_file, 'r') as f:
#             config = json.load(f)
#         return config

#     def generate_bindings(self, config):
#         # Logic to create bindings based on the configuration file
#         bindings = []

#         for binding_config in config['bindings']:
#             if binding_config['type'] == 'JAVA':
#                 # Logic to create JAVA bindings
#                 bindings.append(self.create_java_binding(binding_config))
#             elif binding_config['type'] == 'CPP':
#                 # Logic to create CPP bindings
#                 bindings.append(self.create_cpp_binding(binding_config))
#             elif binding_config['type'] == 'REST':
#                 # Logic to create REST bindings
#                 bindings.append(self.create_rest_binding(binding_config))
#             else:
#                 raise ValueError(f"Unsupported binding type: {binding_config['type']}")

#         return bindings

#     def create_java_binding(self, binding_config):
#         # Logic to create JAVA bindings
#         # ...
#         java_binding = {
#             'name': binding_config['name'],
#             'run': self.execute_java_binding
#         }
#         return java_binding

#     def create_cpp_binding(self, binding_config):
#         # Logic to create CPP bindings
#         # ...
#         cpp_binding = {
#             'name': binding_config['name'],
#             'run': self.execute_cpp_binding
#         }
#         return cpp_binding

#     def create_rest_binding(self, binding_config):
#         # Logic to create REST bindings
#         # ...
#         rest_binding = {
#             'name': binding_config['name'],
#             'run': self.execute_rest_binding
#         }
#         return rest_binding

#     def execute_cpp_binding(self):
#         # Logic to execute CPP binding
#         print("Executing CPP binding...")

#     def execute_rest_binding(self):
#         # Logic to execute REST binding
#         print("Executing REST binding...")

#     def execute_java_binding(self):
#         # Logic to execute JAVA binding
#         java_program = "path/to/java/program.jar"  # Replace with the actual path to your JAVA program
#         subprocess.run(["java", "-jar", java_program])

# # Example configuration for the join operation of Linux
# config = {
#     'bindings': [
#         {
#             'name': 'JavaBinding',
#             'type': 'JAVA'
#         },
#         {
#             'name': 'CppBinding',
#             'type': 'CPP'
#         },
#         {
#             'name': 'RestBinding',
#             'type': 'REST'
#         }
#     ]
# }

# binding_creator = BindingCreator('config.json')
# bindings = binding_creator.generate_bindings(config)

# # Execute the bindings
# for binding in bindings:
    
#     print(f"Running {binding['name']} binding...")
    
#     binding['run']()

#     # Example configuration for the join operation of Linux
#     config = {
#         'bindings': [
#             {
#                 'name': 'JavaBinding',
#                 'type': 'JAVA'
#             },
#             # ...
#         ]
#     }

#     # ...

#     # Execute the JAVA binding
#     java_binding = next(binding for binding in bindings if binding['name'] == 'JavaBinding')
#     print(f"Running {java_binding['name']} binding...")
#     java_binding['run']()
