import yaml
import json
import os
import logging
from urllib.request import urlopen
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
)
parser_logger =logging.getLogger("parser")
client_logger = logging.getLogger("client")
summary_logger=logging.getLogger("summary")
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
                data = yaml.safe_load(f)
        else:
            with open(url, "r") as f:
                data = yaml.safe_load(f)
        parser_logger.info(f"YAML file loaded successfully: {url}")
        return data
    except FileNotFoundError as e:
        parser_logger.error(f"YAML file not found: {url} | ExceptionCode=FILE_NOT_FOUND")
    except yaml.YAMLError as e:
        parser_logger.error(f"YAML parse error: {url} | ExceptionCode=YAML_PARSE_ERROR")
    except Exception as e:
        parser_logger.error(f"Unexpected error loading YAML: {url} | ExceptionCode=UNKNOWN_ERROR")
    return None
def extract_metadata(spec, source_file):
    if not spec:
        parser_logger.error(f"Empty or invalid spec: {source_file} | ExceptionCode=INVALID_SPEC")
        return {}
    meta = {}
    try:
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
        comps = spec.get("components", {})
        meta["securitySchemes"] = comps.get("securitySchemes", {})
        parser_logger.info(f"Metadata extracted successfully: {source_file}")
        return meta
    except Exception as e:
        parser_logger.error(f"Parsing failure for {source_file} | ExceptionCode=PARSING_FAILURE")
        return {}
def main():
    all_metadata = {}
    for url in YAML_URLS:
        spec = load_yaml(url)
        metadata = extract_metadata(spec, url)
        if metadata:
            all_metadata[os.path.basename(url)] = metadata
        else:
            parser_logger.error(f"Missing or invalid metadata for {url} | ExceptionCode=MISSING_METADATA")
    try:
        with open("metadata.json", "w") as f:
            json.dump(all_metadata, f, indent=2)
        summary_logger.info("Summary generation completed successfully")
    except Exception as e:
        summary_logger.error(f"Failed to write metadata.json | ExceptionCode=WRITE_ERROR")
if __name__ == "__main__":
    main()
