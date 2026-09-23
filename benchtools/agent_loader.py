'''
Agent loader is used to execute the Agent module provided by the user to load
the custom agent into BenchTools execution.
User must use an adapter in the module to link the custom agent with BenchTools
'''

import sys
import importlib
from pathlib import Path

def load_agent_from_module(module_path, module_name="my_agent"):
    module_path = Path(module_path)
    parent_dir = str(module_path.parent)

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    mod = importlib.util.module_from_spec(spec)

    sys.path.insert(0, parent_dir)    # so sibling imports within module respolve resolve
    try:
        spec.loader.exec_module(mod)  # runs provided agent module
    finally:
        sys.path.remove(parent_dir)   # clean up regardless of success/failure

    return mod.agent                  # an Agent instance 