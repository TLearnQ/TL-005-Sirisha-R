import yaml
import json
import os
from urllib.request import urlopen
YAML_URLS = [
    "https://forge.3gpp.org/rep/all/5G_APIs/raw/REL-19/TS26512_M1_ContentProtocolsDiscovery.yaml",
    "https://forge.3gpp.org/rep/all/5G_APIs/raw/REL-19/TS29511_N5g-eir_EquipmentIdentityCheck.yaml",
    "https://forge.3gpp.org/rep/all/5G_APIs/raw/REL-19/TS29538_MSGG_N3GDelivery.yaml",
    "https://forge.3gpp.org/rep/all/5G_APIs/raw/REL-19/TS29518_Namf_AIoT.yaml",
    "https://forge.3gpp.org/rep/all/5G_APIs/raw/REL-19/TS29591_Nnef_DNAIMapping.yaml"
]

def load_yaml(url):
    try:
        if url.startswith("http"):
            with urlopen(url) as f:
                return yaml.safe_load(f)
        else:
            with open(url, 'r') as f:
                return yaml.safe_load(f)
    except Exception as e:
        print(f"Failed to load {url}: {e}")
        return None

def extract_metadata(spec):
    if not spec:
        return {}

    meta = {}
    info = spec.get("info", {})
    meta["title"] = info.get("title")
    meta["version"] = info.get("version")
    meta["description"] = info.get("description")
    servers = spec.get("servers", [])
    meta["servers"] = [s.get("url") for s in servers if isinstance(s, dict)]
    meta["tags"] = spec.get("tags", [])
    meta["paths"] = {}
    paths = spec.get("paths", {})
    for p, methods in paths.items():
        meta["paths"][p] = {}
        for method, details in methods.items():
            if not isinstance(details, dict):
                continue
            meta["paths"][p][method] = {
                "summary": details.get("summary"),
                "parameters": details.get("parameters"),
                "requestBody": bool(details.get("requestBody")),
                "responses": {}
            }
            responses = details.get("responses", {})
            for code, resp in responses.items():
               
                schema = None
                content = resp.get("content", {})
                for ctype, body in content.items():
                    if "schema" in body:
                        schema = body["schema"]
                        break
                meta["paths"][p][method]["responses"][code] = schema

    security_schemes = {}
    comps = spec.get("components", {})
    if "securitySchemes" in comps:
        for name, scheme in comps["securitySchemes"].items():
            security_schemes[name] = scheme
    meta["securitySchemes"] = security_schemes
    return meta
def main():
    all_metadata = {}
    for url in YAML_URLS:
        print(f"Processing {url} ...")
        spec = load_yaml(url)
        meta = extract_metadata(spec)
        all_metadata[os.path.basename(url)] = meta
    with open("metadata.json", "w") as f:
        json.dump(all_metadata, f, indent=2)
    print("Saved metadata.json")
if __name__ == "__main__":
    main()
