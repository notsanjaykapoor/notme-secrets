import importlib
import os
import re


def list_schemas(module_name="services.anthropic.tools") -> list[dict]:
    """
    Get list of claude tools.

    Dynamically load tool schemas from the specified module root.
    """
    tools_list = []

    module_dir = module_name.replace(".", "/")
    module_files = os.listdir(module_dir)

    module_files = [name for name in module_files if re.match(r"^tool_.*.py$", name)]

    for module_file in module_files:
        # remove .py from module_file
        module_file = re.sub(r"(\.py)", "", module_file)
        module_path = f"{module_name}.{module_file}"
        module = importlib.import_module(module_path)

        # add schema to list
        tools_list.extend(module.schemas())

    return tools_list
    