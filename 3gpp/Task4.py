import json
from collections import defaultdict, Counter

with open("metadata.json") as f:
    all_metadata = json.load(f)
total_endpoints = 0
method_counter = Counter()
auth_methods = set()
endpoints_with_resp = 0
endpoints_missing_resp = 0
response_codes = set()
for api_name, meta in all_metadata.items():

    auth_methods.update(meta.get("securitySchemes", {}).keys())
    
    for path, methods in meta.get("paths", {}).items():
        total_endpoints += 1
        for method, details in methods.items():
            method_counter[method.upper()] += 1
        
            if details.get("responses"):
                endpoints_with_resp += 1
                response_codes.update(details["responses"].keys())
            else:
                endpoints_missing_resp += 1


coverage = (endpoints_with_resp / total_endpoints * 100) if total_endpoints else 0
summary = {
    "total_endpoints": total_endpoints,
    "http_method_distribution": dict(method_counter),
    "authentication_methods": list(auth_methods),
    "endpoints_with_responses": endpoints_with_resp,
    "endpoints_missing_responses": endpoints_missing_resp,
    "response_codes_encountered": list(response_codes),
    "coverage_percentage": round(coverage, 2)
}

with open("summary.json", "w") as f:
    json.dump(summary, f, indent=2)


analysis = f"""
3ggAPI Summary Report:
Total endpoints parsed: {total_endpoints}
HTTP method distribution: {dict(method_counter)}
Authentication methods used: {list(auth_methods)}
Endpoints with documented responses: {endpoints_with_resp}
Endpoints missing responses: {endpoints_missing_resp}
Response codes encountered: {list(response_codes)}

"""

with open("README.md", "w") as f:
    f.write(analysis)

print("summary.json and README.md generated successfully!")

