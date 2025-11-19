import json

def load(fl,t='file'):
    if t=='file':
        try:
            with open(fl, 'r') as file:
                return json.load(file)

        except FileNotFoundError:
            print(f"Error: '{fl}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{fl}'. Check file format.")
            return None
    else:
        return json.loads(fl)
    
def save(fl,ti='files/result'):
    with open(ti+'.json', "w") as file:
        json.dump(fl, file, indent=4)