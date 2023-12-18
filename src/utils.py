from re import search
from os import path

def places_json(svg_path):
    if not path.exists("." + svg_path):
        print(svg_path)
    outter = []
            
    with open (svg_path) as file:
        cdoe = "^<rect class="  

        for i in file:
            if search(cdoe, i):
                inner = i.split()
                
                outter.append(getter(inner))

    result = {"items": {}}

    for item in outter:
        key1, key2, key3 = item
        if key1 not in result["items"]:
            result["items"][key1] = {}
        if key2 not in result["items"][key1]:
            result["items"][key1][key2] = {}
        result["items"][key1][key2][key3] = { "user" : None, "available" : True}

    return result

            
def getter(inner) -> list:
    values = []
    
    start, end = inner[1].find('"') + 1, inner[1].rfind('"')
    inner[1] = inner[1][start: end]
    start, end = inner[2].find('"') + 1, inner[2].rfind('"')
    inner[2] = inner[2][start: end]
    start, end = inner[3].find('"') + 1, inner[3].rfind('"')
    inner[3] = inner[3][start: end]

    values.append(inner[1])
    values.append(inner[3])
    values.append(inner[2])

    return values
    
