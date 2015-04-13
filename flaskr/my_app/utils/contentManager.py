from pathlib import Path
import json

p = Path('../posts')
results = [] 

for x in p.iterdir():
    print(x)

def generateContent(p):
    r = []
    dfs = p.iterdir()
    for i in dfs:
        if i.is_dir():
            dir_dict = {}
            dir_dict['text'] = i.name
            res = generateContent(i)
            dir_dict['nodes'] = res
            r.append(dir_dict)
        else: # file
            file_dict = {}
            file_dict['text'] = i.name
            r.append(file_dict)
    return r

print(json.dumps(generateContent(p), indent=4))
