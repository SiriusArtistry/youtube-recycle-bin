import json_file as jf

def init():
    global lds, cats, lvt, VERBOSE
    
    VERBOSE = False
    lds = jf.leads()
    cats = lds.keys()
    if VERBOSE: print("CFG: GOT ALL LEADS...")