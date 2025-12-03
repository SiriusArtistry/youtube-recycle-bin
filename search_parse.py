import rand_gens as rg
from re import findall
import config as cfg

def params(cat, ld=False):
    if cfg.VERBOSE: print('-'*40)
    if cfg.VERBOSE: print("PAR: REFRESHING PARAMETERS...")
    if cfg.VERBOSE: print(f'PAR: CURRENT CATEGORY: {cat}...')
    cat_lds = cfg.lds[cat]
    if not ld or ld not in list(cat_lds):
      ld = rg.random_choice(cat_lds)
    date_eval = time_eval = False
    ld_v = cat_lds[ld]
    if cfg.VERBOSE: print(f'PAR: CURRENT LEAD: {ld}: {ld_v}...')
    if isinstance(ld_v,list):
        prm = ld_v[1]
        ld_v = ld_v[0]        
        if cfg.VERBOSE: print(f'PAR: PARAMETERS: {prm}')
    else:
        prm = {}

    hex_eval, rh = findall(r'\$+', ld_v), []
    if hex_eval:
        for n in range(len(hex_eval)):
            rh.append(rg.rNh(len(hex_eval[n])))
            if cfg.VERBOSE: print(f'PAR: RANDOM HEX FOR {hex_eval[n]}: {rh[n]}')

    num_eval, rn = findall(r'\#+', ld_v), []
    if num_eval:
        for n in range(len(num_eval)):
            if 'between' in prm:
                if any(isinstance(el, list) for el in prm['between']):
                    A = prm['between'][n][0]
                    B = prm['between'][n][1]
                else:
                    A = prm['between'][0]
                    B = prm['between'][1]
                rn.append(str(rg.ri(A,B)).zfill(len(str(B))))
            else:
                rn.append(rg.rNd(len(num_eval[n])))
            
            if cfg.VERBOSE: print(f'PAR: RANDOM NUMBER FOR {num_eval[n]}: {rn[n]}')
    
    year_eval = findall(r'Y{2,}',ld_v)
    A, B = "youtube", "today"
    if 'after' in prm and year_eval:
        A = prm['after']
    if 'before' in prm and year_eval:
        B = prm['before']
    if cat == "low":
        B = 2008
    
    rd_dt = rg.random_date(A,B)

    if year_eval:
        date_eval = True
        rd_y = rd_dt.year
        if cfg.VERBOSE: print(f'PAR: RANDOM YEAR FOR {year_eval[0]}: {rd_y}')
    else:
        rd_y='2005'

    Mmonth_eval = findall(r'Month',ld_v)
    if Mmonth_eval:
        date_eval = True
        rd_mm = rd_dt.strftime("%B")
        if cfg.VERBOSE: print(f'PAR: RANDOM MONTH NAME FOR {Mmonth_eval[0]}: {rd_mm}')
    else:
        rd_mm = 'April'

    month_eval = findall(r'M{2}',ld_v)
    if month_eval:
        date_eval = True
        rd_m = str(rd_dt.month).zfill(len(month_eval[0]))
        if cfg.VERBOSE: print(f'PAR: RANDOM MONTH FOR {month_eval[0]}: {rd_m}')
    else:
        rd_m = '04'

    day_eval = findall(r'D{2}',ld_v)
    if day_eval:
        date_eval = True
        rd_d = str(rd_dt.day).zfill(len(day_eval[0]))
        if cfg.VERBOSE: print(f'PAR: RANDOM DAY FOR {day_eval[0]}: {rd_d}')
    else:
        rd_d = '23'

    hour_eval = findall(r'H{2}',ld_v)
    if hour_eval:
        time_eval = True
        rd_h = str(rd_dt.hour).zfill(len(hour_eval[0]))
        if cfg.VERBOSE: print(f'PAR: RANDOM HOUR FOR {hour_eval[0]}: {rd_h}')
    else:
        rd_h = '10'

    minute_eval = findall(r'(?:Mi){2}',ld_v)
    if minute_eval:
        time_eval = True
        rd_mi = str(rd_dt.minute).zfill(int(len(minute_eval[0])/2))
        if cfg.VERBOSE: print(f'PAR: RANDOM MINUTE FOR {minute_eval[0]}: {rd_mi}')
    else:
        rd_mi = '27'

    second_eval = findall(r'S{2}',ld_v)
    if second_eval:
        time_eval = True
        rd_s = str(rd_dt.second).zfill(len(second_eval[0]))
        if cfg.VERBOSE: print(f'PAR: RANDOM SECOND FOR {second_eval[0]}: {rd_s}')
    else:
        rd_s = str(rg.ri(0,59)).zfill(2)

    if date_eval:
        date_picker = f'{str(rd_y)}-{str(rd_m)}-{str(rd_d)}'
        if Mmonth_eval: rd_mm=rd_dt.strftime("%m")
    else: date_picker = ''

    if time_eval:
        time_picker = f'{str(rd_h)}:{str(rd_mi)}'
    else: time_picker = ''
    
    term_params = {"rh": rh,"rn": rn,"prm":prm,
                   "hex_eval":hex_eval,"num_eval":num_eval,
                   "date_eval":[date_eval, year_eval, Mmonth_eval, month_eval, day_eval],
                   "time_eval":[time_eval, hour_eval, minute_eval, second_eval],
                   "date":[rd_y,rd_mm,rd_m,rd_d],"time":[rd_h,rd_mi,rd_s]}
    
    st = search_term(cat, ld, term_params)

    gui_params =  {"st":st,"rh": rh,"rn": rn,"prm":prm,
                "date_eval": [date_eval,date_picker],"time_eval": [time_eval,time_picker]}
    
    return gui_params

def search_term(cat, ld, params):
    st = cfg.lds[cat][ld]
    if cfg.VERBOSE: print(f'PAR: RAW SEARCH TERM: {st}')
    if isinstance(st,list):
        prm = st[1]
        st = st[0]
        if cfg.VERBOSE: print(f'PAR: PARAMETERS: {prm}')
    else:
        prm = {}

    if params['hex_eval']:
        for n in range(len(params['hex_eval'])):
            st = st.replace(str(params['hex_eval'][n]),str(params['rh'][n]))
    if params['num_eval']:
        for n in range(len(params['num_eval'])):
            st = st.replace(params['num_eval'][n],str(params['rn'][n]))

    if params['date_eval'][0]:
        for i in range(1,5):
            if params['date_eval'][i]:
                st = st.replace(str(params['date_eval'][i][0]),str(params['date'][i-1]))

    if params['time_eval'][0]:
        for i in range(1,4):
            if params['time_eval'][i]:
                st = st.replace(str(params['time_eval'][i][0]),str(params['time'][i-1]))

    if cfg.VERBOSE: print(f'PAR: NEW SEARCH TERM: {st}')
    return st


def lead_select(cat, lead):
    return (params(cat,lead))

def cat_select(cat):
    if cfg.VERBOSE: print('^'*40)
    cat_lds = cfg.lds[cat]
    if cfg.VERBOSE: print(f'PAR: SELECTED CATEGORY: {cat}...')
    ld = rg.random_choice(cat_lds)
    if cfg.VERBOSE: print(f'PAR: FORCED RANDOM LEAD FROM \'{cat}\': \"{ld}\"...') 
    return ld, params(cat,ld)

def randomize_cat():
    if cfg.VERBOSE: print('?'*40)
    cat = list(cfg.cats)[(rg.ri(0,len(list(cfg.cats))-1))]
    if cfg.VERBOSE: print(f'PAR: RANDOM CATEGORY: {cat}...')
    cat_lds = cfg.lds[cat]
    ld = rg.random_choice(cat_lds)
    if cfg.VERBOSE: print(f'PAR: RANDOM LEAD: {ld}...')
    return cat, ld, params(cat, ld)

def randomize_lead(cat):
    if cfg.VERBOSE: print('?'*40)
    if not cat in cfg.lds:
        cat = list(cfg.cats)[(rg.ri(0,len(list(cfg.cats))-1))]
    cat_lds = cfg.lds[cat]
    ld = rg.random_choice(cat_lds)
    if cfg.VERBOSE: print(f'PAR: RANDOM LEAD FROM \'{cat}\': \"{ld}\"...')
    return ld, params(cat,ld)