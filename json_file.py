import json
from os import getenv
from dotenv import load_dotenv

load_dotenv()

working_dir = getenv('WORKING_DIR','docs')

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
    
def save(fl,ti='docs/result'):
    with open(ti+'.json', "w") as file:
        json.dump(fl, file, indent=4)

def leads():
    return(load(f'{working_dir}/leads.json','file'))

def readme():
    fl = f'{working_dir}/README.md'
    try:
        with open(fl, "r", encoding="utf-8") as file:
            readme_content = file.read()
        print("JF: FOUND README...")
        return readme_content

    except FileNotFoundError:
        print(f"JF: Error: The file '{fl}' was not found.")
        return ''