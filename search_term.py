import sys
import json_file as jf
import rand_gens as rg
from random import randint
from re import findall

def search_term(cat,verbose=False):
    lds = jf.load('files\\leads.json')
    if lds: 
        if verbose: print("Found leads...")
    else: sys.exit()

    cats = lds.keys()
    if verbose: print(f'Categories: {list(cats)}...')

    if verbose: print(f'Choosing category \'{cat}\'...')

    cat_lds = lds[cat]
    if verbose: print(f'Found {len(cat_lds)} leads in category \'{cat}\'...')

    ld = rg.random_choice(cat_lds)
    if verbose: print(f'Choosing lead \"{ld}\"...')

    st = cat_lds[ld]
    if verbose: print(f'RAW SEARCH TERM: {st}')

    if isinstance(st,list):
        prm = st
        st = st.pop(0)
        if verbose: print(f'PARAMETERS: {prm}')
    else:
        prm = False

    num_eval = findall(r'\#+', st)
    if num_eval:
        for n in range(len(num_eval)):
            if prm:
                rn = str(randint(prm[n][0],prm[n][1])).zfill(len(str(prm[n][1])))
            else:
                rn = rg.rNd(len(num_eval[n]))
            if verbose: print(f'RANDOM NUMBER FOR {num_eval[n]}: {rn}')
            st = st.replace(num_eval[n],str(rn))

    hex_eval = findall(r'\$+', st)
    if hex_eval:
        rh = rg.rNh(len(hex_eval[0]))
        if verbose: print(f'RANDOM HEX FOR {hex_eval[0]}: {rh}')
        st = st.replace(str(hex_eval[0]),str(rh))


    year_eval = findall(r'Y{2,}',st)
    if year_eval:
        if prm:
            rd_dt = rg.random_date(prm[0],"today")
        elif cat == "low":
            rd_dt = rg.random_date("youtube",2008)
        else:
            rd_dt = rg.random_date("youtube","today")
        rd_y = rd_dt.year
        if verbose: print(f'RANDOM YEAR FOR {year_eval[0]}: {rd_y}')
        st = st.replace(str(year_eval[0]),str(rd_y))

    month_eval = findall(r'M{2}',st)
    if month_eval:
        rd_m = str(rd_dt.month).zfill(len(month_eval[0]))
        if verbose: print(f'RANDOM MONTH FOR {month_eval[0]}: {rd_m}')
        st = st.replace(str(month_eval[0]),str(rd_m))

    Mmonth_eval = findall(r'Month',st)
    if Mmonth_eval:
        rd_mm = rd_dt.strftime("%B")
        if verbose: print(f'RANDOM MONTH NAME FOR {Mmonth_eval[0]}: {rd_mm}')
        st = st.replace(str(Mmonth_eval[0]),str(rd_mm))

    day_eval = findall(r'D{2}',st)
    if day_eval:
        rd_d = str(rd_dt.day).zfill(len(day_eval[0]))
        if verbose: print(f'RANDOM DAY FOR {day_eval[0]}: {rd_d}')
        st = st.replace(str(day_eval[0]),str(rd_d))
            

    if verbose: print(f'FINAL SEARCH TERM: {st}')
    return st


