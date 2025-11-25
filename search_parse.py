import rand_gens as rg
from re import findall
import config, copy

def params():
    print('-'*40)
    print("PAR: REFRESHING PARAMETERS...")
    print(f'PAR: CURRENT CATEGORY: {config.cat}...')
    config.cat_lds = config.lds[config.cat]
    if not config.ld or config.ld not in list(config.cat_lds):
      config.ld = rg.random_choice(config.cat_lds)
    print(f'PAR: CURRENT LEAD: {config.ld}...')
    config.date_eval = config.time_eval = False
    config.st = copy.deepcopy(config.cat_lds[config.ld])
    print(f'PAR: RAW SEARCH TERM: {config.st}')

    if isinstance(config.st,list):
        prm = config.st
        config.st = config.st.pop(0)
        print(f'PAR: PARAMETERS: {prm}')
    else:
        prm = False

    hex_eval, config.rh = findall(r'\$+', config.st), []
    if hex_eval:
        for n in range(len(hex_eval)):
            config.rh.append(rg.rNh(len(hex_eval[n])))
            print(f'PAR: RANDOM HEX FOR {hex_eval[n]}: {config.rh[n]}')
            config.st = config.st.replace(str(hex_eval[n]),str(config.rh[n]))

    num_eval, config.rn = findall(r'\#+', config.st), []
    if num_eval:
        for n in range(len(num_eval)):
            if prm:
                config.rn.append(str(rg.ri(prm[n][0],prm[n][1])).zfill(len(str(prm[n][1]))))
            else:
                config.rn.append(rg.rNd(len(num_eval[n])))
            
            print(f'PAR: RANDOM NUMBER FOR {num_eval[n]}: {config.rn[n]}')
            config.st = config.st.replace(num_eval[n],str(config.rn[n]))
    
    year_eval = findall(r'Y{2,}',config.st)
    if prm and year_eval:
        rd_dt = rg.random_date(prm[0],"today")
    elif config.cat == "low":
        rd_dt = rg.random_date("youtube",2008)
    else:
        rd_dt = rg.random_date("youtube","today")

    if year_eval:
        config.date_eval = True
        config.rd_y = rd_dt.year
        print(f'PAR: RANDOM YEAR FOR {year_eval[0]}: {config.rd_y}')
        config.st = config.st.replace(str(year_eval[0]),str(config.rd_y))
    else:
        config.rd_y='2005'

    Mmonth_eval = findall(r'Month',config.st)
    if Mmonth_eval:
        config.date_eval = True
        config.rd_mm = rd_dt.strftime("%B")
        print(f'PAR: RANDOM MONTH NAME FOR {Mmonth_eval[0]}: {config.rd_mm}')
        config.st = config.st.replace(str(Mmonth_eval[0]),str(config.rd_mm))
    else:
        config.rd_mm = 'April'

    month_eval = findall(r'M{2}',config.st)
    if month_eval:
        config.date_eval = True
        config.rd_m = str(rd_dt.month).zfill(len(month_eval[0]))
        print(f'PAR: RANDOM MONTH FOR {month_eval[0]}: {config.rd_m}')
        config.st = config.st.replace(str(month_eval[0]),str(config.rd_m))
    else:
        config.rd_m = '04'

    day_eval = findall(r'D{2}',config.st)
    if day_eval:
        config.date_eval = True
        config.rd_d = str(rd_dt.day).zfill(len(day_eval[0]))
        print(f'PAR: RANDOM DAY FOR {day_eval[0]}: {config.rd_d}')
        config.st = config.st.replace(str(day_eval[0]),str(config.rd_d))
    else:
        config.rd_d = '23'

    hour_eval = findall(r'H{2}',config.st)
    if hour_eval:
        config.time_eval = True
        config.rd_h = str(rd_dt.hour).zfill(len(hour_eval[0]))
        print(f'PAR: RANDOM HOUR FOR {hour_eval[0]}: {config.rd_h}')
        config.st = config.st.replace(str(hour_eval[0]),str(config.rd_h))
    else:
        config.rd_h = '10'

    minute_eval = findall(r'(?:Mi){2}',config.st)
    if minute_eval:
        config.time_eval = True
        config.rd_mi = str(rd_dt.minute).zfill(int(len(minute_eval[0])/2))
        print(f'PAR: RANDOM MINUTE FOR {minute_eval[0]}: {config.rd_mi}')
        config.st = config.st.replace(str(minute_eval[0]),str(config.rd_mi))
    else:
        config.rd_mi = '27'

    second_eval = findall(r'S{2}',config.st)
    if second_eval:
        config.time_eval = True
        config.rd_s = str(rd_dt.second).zfill(len(second_eval[0]))
        print(f'PAR: RANDOM SECOND FOR {second_eval[0]}: {config.rd_s}')
        config.st = config.st.replace(str(second_eval[0]),str(config.rd_s))
    else:
        config.rd_s = str(rg.ri(0,59)).zfill(2)

    if config.date_eval:
        config.date_picker = f'{str(config.rd_y)}-{str(config.rd_m)}-{str(config.rd_d)}'
        if Mmonth_eval: config.rd_mm=rd_dt.strftime("%m")

    if config.time_eval:
        config.time_picker = f'{str(config.rd_h)}:{str(config.rd_mi)}'
    
    print(f'PAR: NEW SEARCH TERM: {config.st}')


def cat_select(cat):
    print('^'*40)
    config.cat = cat
    config.cat_lds = config.lds[cat]
    print(f'PAR: SELECTED CATEGORY: {config.cat}...')
    config.cat_key = config.cat_lds.keys()
    if not config.ld or config.ld not in list(config.cat_key):
        config.ld = rg.random_choice(config.cat_lds)
        print(f'PAR: FORCED RANDOM LEAD FROM \'{config.cat}\': \"{config.ld}\"...')
    params()

def lead_select(lead):
    print('^'*40)
    config.ld = lead
    print(f'PAR: SELECTED LEAD: {config.ld}...')
    params()

def randomize_cat():
    print('?'*40)
    config.cat = list(config.cats)[(rg.ri(0,len(list(config.cats))-1))]
    print(f'PAR: RANDOM CATEGORY: {config.cat}...')
    config.ld = rg.random_choice(config.cat_lds)
    print(f'PAR: RANDOM LEAD: {config.ld}...')
    params()

def randomize_lead():
    print('?'*40)
    config.cat_lds = config.lds[config.cat]
    config.ld = rg.random_choice(config.cat_lds)
    print(f'PAR: RANDOM LEAD FROM \'{config.cat}\': \"{config.ld}\"...')
    params()