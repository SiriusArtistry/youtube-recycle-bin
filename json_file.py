import json
from os import getenv
from dotenv import load_dotenv

load_dotenv()

WORKING_DIR = getenv('WORKING_DIR','public')

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
    
def save(fl,ti=f'{WORKING_DIR}/result'):
    with open(ti+'.json', "w") as file:
        json.dump(fl, file, indent=4)

def leads():
    return(load(f'{WORKING_DIR}/leads.json','file'))

def readme():
    fl = f'{WORKING_DIR}/README.md'
    try:
        with open(fl, "r", encoding="utf-8") as file:
            readme_content = file.read()
        print("JF: FOUND README...")
        return readme_content

    except FileNotFoundError:
        print(f"JF: Error: The file '{fl}' was not found.")
        return ''