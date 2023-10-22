import random
import json
import os
from typing import Tuple

class DynamicText:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "string_field": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "execute"

    CATEGORY = "utils"


    def flatten_templates(self, templates: list[dict[str, list[str]]]): 
        flat = {}

        for template_collection in templates:
            for template_name in template_collection:
                flat[template_name] = template_collection[template_name]

        return flat

    def parse_json_files(self, directory):
        # Check if the directory exists
        if not os.path.exists(directory):
            print(f"The directory '{directory}' does not exist.")
            return None

        # Get a list of all files in the directory
        files = [f for f in os.listdir(directory) if f.endswith('.json')]

        # Check if there are any JSON files in the directory
        if not files:
            print(f"No JSON files found in '{directory}'.")
            return None

        # Initialize an empty list to store the parsed JSON data
        json_data = []

        # Loop through each JSON file, read, and parse it
        for file in files:
            file_path = os.path.join(directory, file)
            with open(file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    json_data.append(data)
                    print(f"Successfully parsed '{file}'.")
                except json.JSONDecodeError as e:
                    print(f"Error parsing '{file}': {e}")

        return json_data

    def find_bracket_pairs(self, string) -> list[Tuple[int, int]]:
        stack = []
        pairs = []

        for i, char in enumerate(string):
            if char == "<":
                stack.append(i)
            elif char == ">":
                if stack:
                    start_index = stack.pop()
                    pairs.append((start_index, i))
                else:
                    raise ValueError("Unbalanced brackets: Closing bracket without corresponding opening bracket.")

        if stack:
            raise ValueError("Unbalanced brackets: Opening bracket without corresponding closing bracket.")

        return pairs

    def from_template(self, file_template: dict[str, list[str]], token: str) -> Tuple[int, str]:
        if token[1:] in file_template:
            template = file_template[token[1:]]
            i = random.randint(0, len(template) - 1)
            opt = template[i]
            return (i, opt)
        return (-1, token)

    def resolve_template_choices(self, string: str, file_templates: dict[str, list[str]]):
        choice_vars: dict[str, str] = {}
        position_vars: dict[str, int] = {}
        working_string: str = string

        bracket_pairs = self.find_bracket_pairs(string)

        i = 0
        for bracket_pair in bracket_pairs:

            start_index = bracket_pair[0]
            end_index = bracket_pair[1]

            template: str = working_string[start_index:end_index + 1]

            before_replace_length = len(working_string)
            chosen_option: str = ""

            # Reuse the same option as a previously labeled template or pick a random option and save the label for later reference
            if template.startswith("<$"):
                choices: list[str] = template[2:-1].split("|")
                var_name: str = choices[0]
                if var_name in choice_vars:
                    chosen_option = choice_vars[var_name]
                else:
                    chosen_option = self.from_template(file_templates, random.choice(choices[1:]))[1]
                    choice_vars[var_name] = chosen_option

            # Pick a known index or pick a random option and save the index for later reference
            elif template.startswith("<#"):
                choices = template[2:-1].split("|")
                num_choices = len(choices) - 1
                if num_choices >= 1:
                    pos_name = choices[0]
                    if pos_name in position_vars:
                        chosen_position = position_vars[pos_name] % num_choices
                    else:
                        chosen_position = random.randrange(0, num_choices)
                        position_vars[pos_name] = chosen_position
                    chosen_option = self.from_template(file_templates, choices[chosen_position + 1])[1]

            # Ignore this template
            elif template.startswith("<!"):
                chosen_option = ""

            # Pick a random option
            else:
                choices = template[1:-1].split("|")
                chosen_option = self.from_template(file_templates, random.choice(choices))[1]


            working_string = working_string.replace(template, chosen_option, 1)
            length_diff = before_replace_length - len(working_string)
            i = i + 1

            for index in range(i, len(bracket_pairs)):
                bracket_pair = bracket_pairs[index]
                if bracket_pair[0] > start_index:
                    bracket_pairs[index] = (bracket_pairs[index][0] - length_diff, bracket_pairs[index][1])
                if bracket_pair[1] > end_index:
                    bracket_pairs[index] = (bracket_pairs[index][0], bracket_pairs[index][1] - length_diff)

        return working_string


    def execute(self, string_field, seed):
        random.seed((seed % 100000) + (seed / 100000))
        templates = self.parse_json_files(os.path.join(os.getcwd(), "ComfyUI", "custom_nodes", "templates"))
        templates = self.flatten_templates(templates)
        modified_prompt = self.resolve_template_choices(string_field, templates)
        print(f"Dynamic Text v1.2 ({seed}): {modified_prompt}")
        return (modified_prompt,)

NODE_CLASS_MAPPINGS = {
    "DynamicText": DynamicText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicText": "Dynamic Text"
}
