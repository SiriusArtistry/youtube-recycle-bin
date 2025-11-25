import json_file as jf

def init():
    global ld, lds, cat, cats, cat_lds, cat_key, st, prm, lvt, results, \
        rh, rn, rd_y, rd_m, rd_d, rd_h, rd_mi, rd_s, \
        time_eval, date_eval, date_picker, time_picker
    
    lds = jf.leads()
    cats = lds.keys()
    print("CFG: GOT ALL LEADS...")
    ld = ''
    cat = 'old'
    cat_lds = lds[cat]
    print(f"CFG: GOT LEADS FROM CATEGORY {cat}...")
    st = ''
    prm = ''
    results = False
    cat_key = cat_lds.keys()
    lvt = 100
    rh = []
    rn = []
    date_picker = ''
    time_picker = ''