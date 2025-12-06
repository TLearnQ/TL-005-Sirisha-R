import json
import yaml

def load_and_clean(path):
    # Load YAML or JSON
    data = yaml.safe_load(open(path))

    cleaned = {}

    for k, v in data.items():
        key = k.lower()

        if isinstance(v, dict):
            sub = {}
            for a, b in v.items():
                sub[a.lower()] = b
            cleaned[key] = sub
        else:
            cleaned[key] = v

    return cleaned

cleaned_data = load_and_clean("output.yaml")

with open("output.json", "w") as f:
    json.dump(cleaned_data, f, indent=4)
