import json
network_devices = []

def handle(request):
    try:
        parts = request.split(" ", 2)
        method = parts[0]
        path = parts[1]
        data = json.loads(parts[2]) if len(parts) == 3 else None
    except:
        return "Error: Malformed request"


    if method == "GET":
        if path == "/items":
            return network_devices
        
        if path == "/items/count":
            return {"total": len(network_devices)}
        
        return "Error: Unknown GET path"

    if method == "POST":
        if path == "/items":
            if not data or "title" not in data:
                return "Error: Missing 'title'"
            
            network_devices.append(data)
            return {"message": "api added", "item": data}
        
        return "Error: Unknown POST path"
    return f"Error: Unsupported method {method}"


