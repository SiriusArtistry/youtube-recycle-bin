from nicegui import app, ui, context
import json_file as jf
import rand_gens as rg
from random import randint
from re import findall
from youtube_search import YoutubeSearch
from dotenv import load_dotenv
import os, traceback

load_dotenv()

environment = os.getenv('ENVIRONMENT','local')
working_dir = os.getenv('WORKING_DIR','files')

print('\n'*20)
print('*'*40+'\nSTARTING APPLICATION...\n'+'*'*40)

@app.on_page_exception
def timeout_error_page(exception: Exception) -> None:
    common_header()
    with ui.column().classes('absolute-center items-center gap-8'):
        ui.icon('error_outline', size='xl').style('color: gray')
        ui.label(f'{exception}').classes('text-2xl').style('color: gray')
        try_btn = ui.button('Try Again',on_click=lambda:ui.navigate.to('/')).classes('w-full justify-self-center')
        

app.add_static_files(f"/files", f"{working_dir}")
lds = jf.load(f'{working_dir}/leads.json')

@ui.page('/no-lead')
def raise_filenotfound_error():
    if not lds:
       raise FileNotFoundError('Could not find leads file in {working_dir}...')
    else:
        ui.navigate.to('/')

@ui.page('/rate-limit')
def raise_ratelimit_error():
    raise ConnectionError('Couldn\'t reach YouTube...')

@ui.page('/search-error')
def raise_search_error():
    if not st:
        results=False
        randomize()
        load_cards.refresh()
        raise TypeError(f'Had trouble using lead {ld}...')
    else:
        ui.navigate.to('/')

if lds: 
    print("Found leads...")
    cats = lds.keys()
    cat = 'old'
    ld = 'IMG'
    st = ''
    lvt = 100
    date_eval = False
    time_eval = False
    max_results=300
    abs_max_results = 5000
    enable_try_again = True
    enable_search = True
    cat_lock = True
    lead_lock = False
    results=False
    verbose = True

    @ui.refreshable
    def params_needed():
        global st, date_picker, date_eval, time_picker, time_eval
        date_eval, time_eval = False, False
        print('-'*40)
        print("REFRESHING PARAMETERS...")
        st = cat_lds[ld]
        print(f'RAW SEARCH TERM: {st}')
        if isinstance(st,list):
            prm = st
            try:
                st = st.pop(0)
            except IndexError:
                ui.navigate.to('/search-error')
            if verbose: print(f'PARAMETERS: {prm}')
        else:
            prm = False

        try:
            hex_eval = findall(r'\$+', st)
        except TypeError:
            ui.navigate.to('/search-error')
            return False
        if hex_eval:
            rh = rg.rNh(len(hex_eval[0]))
            ui.input(value=rh).classes('max-w-15').set_enabled(False)
            if verbose: print(f'RANDOM HEX FOR {hex_eval[0]}: {rh}')
            st = st.replace(str(hex_eval[0]),str(rh))   
  
        num_eval = findall(r'\#+', st)
        if num_eval:
            for n in range(len(num_eval)):
                if prm:
                    rn = str(randint(prm[n][0],prm[n][1])).zfill(len(str(prm[n][1])))
                else:
                    rn = rg.rNd(len(num_eval[n]))
                ui.number(value=rn).classes('max-w-15').set_enabled(False)
                if verbose: print(f'RANDOM NUMBER FOR {num_eval[n]}: {rn}')
                st = st.replace(num_eval[n],str(rn))

        year_eval = findall(r'Y{2,}',st)

        if prm and year_eval:
            rd_dt = rg.random_date(prm[0],"today")
        elif cat == "low":
            rd_dt = rg.random_date("youtube",2008)
        else:
            rd_dt = rg.random_date("youtube","today")

        if year_eval:
            date_eval = True
            rd_y = rd_dt.year
            if verbose: print(f'RANDOM YEAR FOR {year_eval[0]}: {rd_y}')
            st = st.replace(str(year_eval[0]),str(rd_y))
        else:
            rd_y='2005'

        month_eval = findall(r'M{2}',st)
        if month_eval:
            date_eval = True
            rd_m = str(rd_dt.month).zfill(len(month_eval[0]))
            if verbose: print(f'RANDOM MONTH FOR {month_eval[0]}: {rd_m}')
            st = st.replace(str(month_eval[0]),str(rd_m))
        else:
            rd_m = '04'

        Mmonth_eval = findall(r'Month',st)
        if Mmonth_eval:
            date_eval = True
            rd_mm = rd_dt.strftime("%B")
            if verbose: print(f'RANDOM MONTH NAME FOR {Mmonth_eval[0]}: {rd_mm}')
            st = st.replace(str(Mmonth_eval[0]),str(rd_mm))
        else:
            rd_mm = 'April'

        day_eval = findall(r'D{2}',st)
        if day_eval:
            date_eval = True
            rd_d = str(rd_dt.day).zfill(len(day_eval[0]))
            if verbose: print(f'RANDOM DAY FOR {day_eval[0]}: {rd_d}')
            st = st.replace(str(day_eval[0]),str(rd_d))
        else:
            rd_d = '23'

        hour_eval = findall(r'H{2}',st)
        if hour_eval:
            time_eval = True
            rd_h = str(rd_dt.hour).zfill(len(hour_eval[0]))
            if verbose: print(f'RANDOM HOUR FOR {hour_eval[0]}: {rd_h}')
            st = st.replace(str(hour_eval[0]),str(rd_h))
        else:
            rd_h = '10'

        minute_eval = findall(r'(?:Mi){2}',st)
        if minute_eval:
            time_eval = True
            rd_mi = str(rd_dt.minute).zfill(int(len(minute_eval[0])/2))
            if verbose: print(f'RANDOM MINUTE FOR {minute_eval[0]}: {rd_mi}')
            st = st.replace(str(minute_eval[0]),str(rd_mi))
        else:
            rd_mi = '27'

        second_eval = findall(r'S{2}',st)
        if second_eval:
            time_eval = True
            rd_s = str(rd_dt.second).zfill(len(second_eval[0]))
            if verbose: print(f'RANDOM SECOND FOR {second_eval[0]}: {rd_s}')
            st = st.replace(str(second_eval[0]),str(rd_s))
        else:
            rd_s = str(randint(0,59)).zfill(2)

        if date_eval:
            if Mmonth_eval: rd_m=rd_dt.strftime("%m")
            date_picker = f'{str(rd_y)}-{str(rd_m)}-{str(rd_d)}'
            ui.date_input(value=date_picker).bind_value(globals(),'date_picker').classes('max-w-32').set_enabled(False)

        if time_eval:
            time_picker = f'{str(rd_h)}:{str(rd_mi)}'
            ui.time_input(value=time_picker).bind_value(globals(),'time_picker').classes('max-w-32').set_enabled(False)
        
        print(f'NEW SEARCH TERM: {st}')

    @ui.refreshable
    def lead_select():
        global cat_lds, cat_key, ld, enable_try_again
        enable_try_again = True
        cat_lds = lds[cat]
        cat_key = cat_lds.keys()
        if not ld or ld not in list(cat_key):
            ld = rg.random_choice(cat_lds)
        with ui.button(icon='lock_open', on_click=lambda: lock_lead(lead_lock_btn)).props('flat color=white') as lead_lock_btn:
            ui.tooltip('Lock Lead').props('delay="1000"')
        with ui.select(options=list(cat_key), with_input=True,on_change=lambda: params_needed.refresh()).bind_value(globals(),'ld') as led_btn:
            ui.tooltip('Lead').props('delay="1000"')

    def randomize():
        global cat, ld, lead_lock, enable_try_again
        enable_try_again = True
        print('?'*40+'\nRANDOMIZING...')
        if not cat_lock:
            lead_lock = False
            cat = list(cats)[(randint(0,len(list(cats))-1))]
            print(f'New cat: {cat}...')
            ld = rg.random_choice(cat_lds)
            print(f'Choosing lead from \'{cat}\': \"{ld}\"...')
            lead_select.refresh()
        else:
            if not lead_lock:
                ld = rg.random_choice(cat_lds)
                print(f'Choosing lead from \'{cat}\': \"{ld}\"...')
            else:
                params_needed.refresh()
                # lead_select.refresh()
        # params_needed.refresh()

    async def search_youtube(button: ui.button, num_results=max_results) -> None:
        global results, lv_results, st, lvt, app
        # button.disable()
        s_term = st
        if cat == "new":
            s_filter = "&sp=CAI%253D"
        elif cat == "old":
            s_filter = "&sp=CAMSAhAB"
        elif cat == "low":
            s_term = s_term + " Before:2008"

        # url = f'https://www.youtube.com/results?search_query={s_term}{s_filter}'

        print('%'*40)
        print('SEARCHING YOUTUBE...')
        try:
            results = YoutubeSearch(s_term, num_results).to_dict()
        except ConnectionError:
            ui.navigate.to('/rate-limit')

        lv_results = []
        print(f'Found {len(results)} videos matching \'{s_term}\'...')
        for result in results:
            rt = result['title']
            rv = result['views']
            if not isinstance(rv,int):
                rvi = int(rv.replace(',','').replace(' views','').replace(' view','').replace('No','0'))
            else:
                rvi = int(rv)
            ru = result['publish_time']

            if rvi < lvt + 1:
                lv_results.append(result)

            print('-'*40)
            print(f'Title:\t\t{rt}')
            print(f'Views:\t\t{rv}')
            print(f'Uploaded:\t{ru}')

        print(f'Found {len(lv_results)} videos with less than {lvt} views...')
        print('-'*40)

        results = lv_results
        # app.storage.browser['results'] = results

        # jf.save(results)
        # jf.save(lv_results,'files/lv_result')

        # results = jf.load('files/lv_result.json')
        # print(f'Loaded {len(results)} videos...')
        # button.enable()
        searched_term.refresh()
        load_cards.refresh()    

    async def try_again():
        global enable_try_again
        more_results = 0
        enable_try_again = False
        load_cards.refresh()
        while not results and more_results<abs_max_results-(max_results):
            more_results += 300
            print(f"Setting max results to {max_results+more_results}...")
            await search_youtube(max_results+more_results)

    @ui.refreshable
    def load_cards():
        if results:
            for result in results:
                if result['thumbnails']:
                    tmb = result['thumbnails'][0]
                ti = result['title']
                if len(ti) > 64:
                    ti = ti[:61] + "..."
                ds = result['long_desc']
                ch = result['channel']
                vw = result['views']
                up = result['publish_time']
                lnk = 'https://youtube.com' + result['url_suffix']
                with ui.link(target=lnk,new_tab='true').classes('text-primary !no-underline justify-center').style('max-width: 500px;'):
                    with ui.card().tight().props('bordered flat').style('max-width: 500px;'):
                        ui.image(tmb).classes('aspect-180/101; max-h-280px max-w-500px')
                        with ui.card_section():
                            ui.label(ti).style('color: white; font-weight: 1000')
                            with ui.row().style('color: white'):
                                ui.label(vw)
                                ui.label(up)
                            ui.label(ch).style('color: grey')
                            ui.label(ds)
        else:
            if results == False:
                with ui.column().classes('absolute-center w-xl'):
                    ui.space()
                    ui.label('Welcome to the YouTube Recycle Bin').style('font-size: 200%')
                    ui.label('🎲 Randomize and 🔎 Search to get started...')
            else:
                with ui.column().classes('absolute-center w-1fr'):
                    ui.space()
                    info = f'Nothing here for {st} with less than {format(int(lvt),',')} views...'
                    info = info.replace('less than 0','no').replace('1 videos', '1 video')
                    ui.label(info).style('color: gray').classes('w-full justify-center')
                    try_btn = ui.button('Try Again',on_click=lambda: try_again()).classes('w-full justify-self-center').set_enabled(enable_try_again)

    @ui.refreshable
    def searched_term():
        if results:
            with ui.row().classes(replace='row items-center w-[100%] no-wrap').style('background-color: black; margin: 0; padding: 0; display: flex;'):
                info = f'Found {len(lv_results)} videos matching {st} with less than {format(int(lvt),',')} views...'
                info = info.replace('less than 0','no').replace('1 videos', '1 video')
                ui.label(info)

    def set_icon_button(button_element,state):
        if state:
            button_element.set_icon('lock')
        else:
            button_element.set_icon('lock_open')

    def lock_cat(button_element):
        global cat_lock
        cat_lock = not cat_lock
        set_icon_button(button_element,cat_lock)

    def lock_lead(button_element):
        global lead_lock
        lead_lock = not lead_lock
        set_icon_button(button_element,lead_lock)

    def common_header():
        global main_header
        with ui.header().classes(replace='row items-center min-h-14').style('gap: 5px') as main_header:
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
            # ui.label('YouTube Recycle Bin')
            with ui.link(target='/'):
                ui.interactive_image('/files/YTRB_logo_beta.png').style('max-width: 100px')
            

        with ui.footer(value=False) as footer:
            ui.label('Footer')

        with ui.left_drawer(value=False).classes('bg-blue-100 disable-scrollbar').props('width=60 bordered') as left_drawer:
            ui.space()
            with ui.link(target='https://github.com/zauberzeug/nicegui',new_tab=True):
                ui.interactive_image('https://nicegui.io/logo.png').classes('w-full h-auto') # Example image from URL
            with ui.link(target='https://github.com/SiriusArtistry/youtube-recycle-bin',new_tab=True):
                ui.interactive_image('/files/github-mark-white.png').classes('w-full h-auto')

        ui.query('body').style(f'background-color: black')
        ui.colors(primary='#555')
else:
    ui.navigate.to('/no-lead')

@ui.page('/')
def main_page():
    print('.'*40)
    print("MAIN PAGE")
    global main_header
    ui.add_css('''
        @layer utilities{
            .disable-scrollbars::-webkit-scrollbar {
                background: transparent; /* Chrome/Safari/Webkit */
                width: 0px;
            display: none;
            }
    
            .disable-scrollbars {
                scrollbar-width: none !important; /* Firefox */
                -ms-overflow-style: none !important;  /* IE 10+ */
            }
        }
    ''')
    common_header()
    with main_header:
        with ui.button(on_click=lambda: randomize(), icon='casino').props('flat color=white'):
            ui.tooltip('Randomize').props('delay="1000"')
        with ui.button(icon='lock', on_click=lambda: lock_cat(cat_lock_btn)).props('flat color=white') as cat_lock_btn:
            ui.tooltip('Lock Category').props('delay="1000"')
        with ui.select(options=list(cats),on_change=lambda: lead_select.refresh()).bind_value(globals(),'cat') as cat_btn:
            ui.tooltip('Category').props('delay="1000"')
        lead_select()
        params_needed()
        ui.space()
        with ui.number(value=lvt,precision=0,min=0).bind_value(globals(),'lvt').classes('max-w-15 disable-scrollbars'):
            ui.tooltip('Max Viewcount').props('delay="1000"')
        with ui.button(icon='search',on_click=lambda:search_youtube(search_btn)).props('flat color=white') as search_btn:
            ui.tooltip('Search').props('delay="1000"')

    searched_term()

    with ui.grid().classes('w-full').style('grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))'):
        load_cards()    

@ui.page('/about')
def about_page():
    common_header()
    ui.label('Hello there')

print(f'Running in environment \'{environment}\'')
if not environment == 'local':
    ui.run_with(app,title='YouTube Video Graveyard',favicon='🪦')
else:
    ui.run()