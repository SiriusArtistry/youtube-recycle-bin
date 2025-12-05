import json,os

BACKEND_DIR = os.environ.get('BACKEND_DIR','docs/')

def load(fl,t='file'):
    if t=='file':
        try:
            with open(fl, 'r') as file:
                return json.load(file)

        except FileNotFoundError:
            print(f"JF: Error: '{fl}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"JF: Error: Could not decode JSON from '{fl}'. Check file format.")
            return None
    else:
        return json.loads(fl)
    
def save(fl,ti=f'{BACKEND_DIR}result'):
    with open(ti+'.json', "w") as file:
        json.dump(fl, file, indent=4)

def leads():
    fl = f'{BACKEND_DIR}leads.json'
    path = os.path.join(os. getcwd(), fl)
    return(load(path,'file'))

def readme():
    fl = f'{BACKEND_DIR}README.md'
    path = os.path.join(os. getcwd(), fl)
    try:
        with open(path, "r", encoding="utf-8") as file:
            readme_content = file.read()
        print("JF: FOUND README...")
        return readme_content

    except FileNotFoundError:
        print(f"JF: Error: The file '{fl}' was not found.")
        return ''