import copy


def generate_prompt(template: str, replace_dict: dict):
    prompt = copy.deepcopy(template)
    for k, v in replace_dict.items():
        prompt = prompt.replace(k, str(v))
    return prompt