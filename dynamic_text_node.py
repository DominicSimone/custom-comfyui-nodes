import random

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

    def find_bracket_pairs(self, string):
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

    def resolve_template_choices(self, string):
        choice_vars = {}
        position_vars = {}
        working_string = string

        bracket_pairs = self.find_bracket_pairs(string)

        i = 0
        for bracket_pair in bracket_pairs:

            start_index = bracket_pair[0]
            end_index = bracket_pair[1]

            template = working_string[start_index:end_index + 1]

            before_replace_length = len(working_string)
            chosen_option = ''

            if template.startswith("<$"):
                choices = template[2:-1].split("|")
                var_name = choices[0]
                if var_name in choice_vars:
                    chosen_option = choice_vars[var_name]
                else:
                    chosen_option = random.choice(choices[1:])
                    choice_vars[var_name] = chosen_option

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
                    chosen_option = choices[chosen_position + 1]

            else:
                choices = template[1:-1].split("|")
                chosen_option = random.choice(choices)

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
        random.seed(seed)
        modified_prompt = self.resolve_template_choices(string_field)
        print(f"Dynamic Text ({seed}): {modified_prompt}")
        return (modified_prompt,)

NODE_CLASS_MAPPINGS = {
    "DynamicText": DynamicText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicText": "Dynamic Text"
}
