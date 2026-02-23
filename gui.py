import config, os, search_parse, search_youtube, json_file, device_info
from nicegui import app as nicegui_app, ui, run
from contextlib import contextmanager
from fastapi import FastAPI

print('\n'*20)
print('*'*40+'\nGUI: STARTING APPLICATION...\n'+'*'*40)
try:
    config.init()
    VERBOSE = config.VERBOSE
except (TypeError, AttributeError):
    VERBOSE = True
    ui.navigate.to('/no-lead')

ENVIRONMENT = os.environ.get('ENVIRONMENT','local')
WORKING_DIR = os.environ.get('WORKING_DIR','public/')

TITLE = 'YouTube Recycle Bin'

app = FastAPI()

@nicegui_app.on_page_exception
def error_page(exception: Exception) -> None:
    common_header()
    gui_style()
    with ui.column().classes('absolute-center items-center gap-8 w-auto'):
        ui.icon('error_outline', size='xl').style('color: gray')
        ui.label(f'Encountered an issue...').classes('text-2xl').style('color: gray')
        ui.code(str(exception)).classes('w-auto')
        ui.button('Try Again',on_click=lambda:ui.navigate.to('/')).classes('w-40px justify-self-center')

@ui.page('/no-lead')
def raise_filenotfound_error():
    gui_style()
    if not config.lds:
       raise FileNotFoundError(f'Could not find leads file in \'{WORKING_DIR}\'...')
    else:
        ui.navigate.to('/')

@ui.page('/rate-limit')
def raise_ratelimit_error():
    gui_style()
    raise ConnectionError('Couldn\'t reach YouTube...')

@ui.page('/search-error')
def raise_search_error():
    gui_style()
    if 'params' not in nicegui_app.storage.user or not nicegui_app.storage.user['params']['st']:
        gui_init()
        raise TypeError(f'Had trouble using lead \'{nicegui_app.storage.user['lead']}\'...')
    else:
        ui.navigate.to('/')

@ui.page('/404')
def not_found_page():
    gui_style()
    common_header()

@contextmanager
def disable(button: ui.button):
    button.disable()
    try:
        yield
    finally:
        button.enable()

def gui_style():
    ui.query('body').style(f'background-color: dark_page text: xl')
    ui.colors(primary='#212121', secondary='#1D1D1D', accent="#FF0033", dark_page='#111111')
    ui.dark_mode(True)

def gui_init():
    if config.lds:
        if VERBOSE: print("GUI: FOUND LEADS...")
        if 'results'    not in nicegui_app.storage.user: nicegui_app.storage.user['results'] = False
        if 'last_search'not in nicegui_app.storage.user: nicegui_app.storage.user['last_search'] = [0,"",0]
        if 'cat'        not in nicegui_app.storage.user: nicegui_app.storage.user['cat']     = 'old'
        if 'lvt'        not in nicegui_app.storage.user: nicegui_app.storage.user['lvt']     = 100
        nicegui_app.storage.user['lead'], nicegui_app.storage.user['params'] = search_parse.randomize_lead(nicegui_app.storage.user['cat'])
        nicegui_app.storage.user['allow_try_again'], nicegui_app.storage.user['allow_search'], nicegui_app.storage.user['cat_lock'] = True, True, True
        nicegui_app.storage.user['lead_lock'] = False
    else:
        ui.navigate.to('/no-lead')

class YouTubeLink(ui.link):
    def __init__(self, target = '', text = 'Go to Youtube', new_tab = True):
        super().__init__(text, f'https://www.youtube.com/results?search_query={target}', new_tab)
        ui.add_css('''
            .ext[href^="http"]::after {
                                content: "";
                display: inline-block;
                width: 0.8em;
                height: 0.8em;
                margin-left: 0.25em;

                background-size: 100%;
                background-image: url('/external-link-26.png');
                filter: invert(100%);
            }
        ''')
        self.classes('text-accent ext w-40px')

def set_icon_button(button_element,state):
    if state:
        button_element.set_icon('lock')
    else:
        button_element.set_icon('lock_open')

def lock_cat(button_element):
    nicegui_app.storage.user['cat_lock'] = not nicegui_app.storage.user['cat_lock']
    set_icon_button(button_element,nicegui_app.storage.user['cat_lock'])

def lock_lead(button_element):
    nicegui_app.storage.user['lead_lock'] = not nicegui_app.storage.user['lead_lock']
    set_icon_button(button_element,nicegui_app.storage.user['lead_lock'])

def common_header():
    global main_header
    ui.add_head_html('''
        <style>
            /* For Chrome, Safari, Edge, Opera */
            input[type="number"]::-webkit-outer-spin-button,
            input[type="number"]::-webkit-inner-spin-button {
                -webkit-appearance: none;
                margin: 0;
            }

            /* For Firefox */
            input[type="number"] {
                -moz-appearance: textfield;
            }
        </style>
            ''')
    reveal = 'reveal' if device_info.is_mobile() else ''
    with ui.header().props(f'{reveal}').classes(replace='gap-4 row items-center min-h-14 px-4 grid-rows-1 grid-flow-col absolue-full') as main_header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white').classes('md:px-0')
        # ui.label('YouTube Recycle Bin')
        with ui.link(target='/'):
            ui.interactive_image(f'{WORKING_DIR}YTRB_logo_beta.png').style('max-width: 100px').classes('display:block')

    with ui.left_drawer(value=False).classes('bg-dark disable-scrollbar').props('width=60') as left_drawer:
        ui.space()
        with ui.link(target='https://github.com/zauberzeug/nicegui',new_tab=True):
            with ui.interactive_image('https://nicegui.io/logo.png').classes('w-full h-auto invert'):
                ui.tooltip('Built with NiceGUI').props('delay="1000" anchor="center right" self="center left"')
        with ui.link(target='https://github.com/SiriusArtistry/youtube-recycle-bin',new_tab=True):
            with ui.interactive_image(f'{WORKING_DIR}github-mark-white.png').classes('w-full h-auto'):
                ui.tooltip('Source code on Github').props('delay="1000" anchor="center right" self="center left"')
        with ui.link(target='/about'):
            with ui.icon('info',color='white', size='25px'):
                ui.tooltip('About').props('delay="1000" anchor="center right" self="center left"')

@ui.page('/')
def main_page():
    if VERBOSE: print('.'*40+'\nGUI: MAIN PAGE')
    if VERBOSE: print(f'USER: {nicegui_app.storage.browser['id']}')
    gui_style()
    gui_init()
    common_header()

    @ui.refreshable
    def gui_lead_header():
        global lead_lock_btn
        nicegui_app.storage.user['allow_try_again'] = True
        with ui.button(icon='lock_open', on_click=lambda: lock_lead(lead_lock_btn)).props('flat color=white') as lead_lock_btn:
            ui.tooltip('Lock Lead').props('delay="1000"')
        with ui.select(label='Lead',options=list(config.lds[nicegui_app.storage.user['cat']].keys()),\
                    with_input=True,on_change=lambda: gui_lead_select()).bind_value(nicegui_app.storage.user,'lead')\
                        .classes('w-500px text-white'):
            ui.tooltip('Lead').props('delay="1000"')
                
        gui_update_params.refresh()

    def gui_lead_select():
        nicegui_app.storage.user['params'] = search_parse.lead_select(nicegui_app.storage.user['cat'],nicegui_app.storage.user['lead'])
        gui_update_params.refresh()

    def gui_cat_select():
        nicegui_app.storage.user['lead'], nicegui_app.storage.user['params'] = search_parse.cat_select(nicegui_app.storage.user['cat'])
        gui_lead_header.refresh()

    def get_params():
        try:
            nicegui_app.storage.user['params'] = search_parse.params(nicegui_app.storage.user['cat'],nicegui_app.storage.user['lead'])
        except (IndexError, TypeError):
            ui.navigate.to('/search-error')
        gui_update_params.refresh()

    @ui.refreshable
    def gui_update_params():
        nicegui_app.storage.user['params'] = search_parse.params(nicegui_app.storage.user['cat'],nicegui_app.storage.user['lead'])
        if nicegui_app.storage.user['params']['rh']:
            for r in nicegui_app.storage.user['params']['rh']:
                ui.input(label='X'*len(r),value=r).classes('max-w-15').set_enabled(False)

        if nicegui_app.storage.user['params']['rn']:
            i=0
            for r in nicegui_app.storage.user['params']['rn']:
                if 'between' in nicegui_app.storage.user['params']['prm']:
                    b = nicegui_app.storage.user['params']['prm']['between']
                    if any(isinstance(el, list) for el in b):
                        A = b[i][0]
                        B = b[i][1]
                        i+=1
                    else:
                        A = b[0]
                        B = b[1]
                    rmin, rmax = A, B
                else:
                    rmin = 0
                    rmax = 9999
                ui.number(label='X'*len(r),value=r,min=rmin,max=rmax)\
                    .classes('max-w-15').set_enabled(False)

        if nicegui_app.storage.user['params']['date_eval'][0]:
            date_picker = nicegui_app.storage.user['params']['date_eval'][1]
            if 'after' in nicegui_app.storage.user['params']['prm']:
                date_after = f' (after {nicegui_app.storage.user['params']['prm']['after']})'
            else:
                date_after = ''
            ui.date_input(label=f'Date{date_after}', value=date_picker)\
                .classes('w-auto max-w-38').set_enabled(False)\
            # .bind_value_from(date_picker)

        if nicegui_app.storage.user['params']['time_eval'][0]:
            time_picker = nicegui_app.storage.user['params']['time_eval'][1]
            ui.time_input(label='Time', value=time_picker).classes('max-w-32').set_enabled(False)
                # .bind_value_from(time_picker)\
    
    @ui.refreshable
    def gui_searched_term():
        if int(nicegui_app.storage.user['last_search'][0])>0:
            with ui.row().classes(replace='row items-center w-[100%] no-wrap').style('margin: 0; padding: 0; display: flex;'):
                info = f'Found {nicegui_app.storage.user['last_search'][0]} videos matching \'{nicegui_app.storage.user['last_search'][1]}\' with less than {format(nicegui_app.storage.user['last_search'][2],',')} views...\t'
                info = info.replace('less than 0','no').replace('1 videos', '1 video')
                ui.label(info)
                ui.space()
                YouTubeLink(nicegui_app.storage.user['last_search'][1])
    
    @ui.refreshable
    def gui_load_cards():
        global try_again_row
        if nicegui_app.storage.user['results'] and isinstance(nicegui_app.storage.user['results'],list):
            if VERBOSE: print(f"GUI: FETCHING RESULTS...")
            for result in nicegui_app.storage.user['results']:
                if result['thumbnails']:
                    tmb = result['thumbnails'][0]
                ti = result['title']
                if len(ti) > 50:
                    ti = ti[:47] + "..."
                ds = result['long_desc']
                ch = result['channel']
                vw = result['views']
                up = result['publish_time']
                lnk = 'https://youtube.com' + result['url_suffix']
                with ui.link(target=lnk,new_tab='true').classes('text-primary !no-underline justify-center').style('max-width: 500px;'):
                    with ui.card().tight().props('flat').style('max-width: 500px;').classes('bg-secondary'):
                        ui.image(tmb).classes('aspect-180/101; max-h-280px max-w-500px')
                        with ui.card_section():
                            ui.label(ti).style('color: white; font-weight: 1000')
                            with ui.row().style('color: grey'):
                                ui.label(vw)
                                ui.label(up)
                            ui.label(ch).classes('text-accent')
                            ui.label(ds)
        else:
            if nicegui_app.storage.user['results'] == False or not isinstance(nicegui_app.storage.user['results'],list):
                if VERBOSE: print(f"GUI: NO RESULTS, NEW INSTANCE...")
                with ui.column().classes('absolute-center w-3/4'):
                    ui.space()
                    ui.label('Welcome to the YouTube Recycle Bin').style('font-size: 200%')
                    ui.label('🎲 Randomize and 🔎 Search to get started...')
            else:
                if VERBOSE: print(f"GUI: NO RESULTS, NO MATCH...")
                with ui.column().classes('absolute-center w-7/8').style(replace=''):
                    ui.space()
                    ui.icon('help_outline', size='xl').style('color: gray')
                    with ui.row(wrap=False):
                        info = f'Nothing here for \'{nicegui_app.storage.user['last_search'][1]}\' with less than {format(nicegui_app.storage.user['last_search'][2],',')} views...\t'
                        info = info.replace('less than 0','no').replace('1 videos', '1 video')
                        ui.label(info).style('color: gray').classes('w-3/5 justify-center')
                        ui.space()
                        YouTubeLink(nicegui_app.storage.user['last_search'][1])
                    with ui.row() as try_again_row:
                        ui.button('Try Again',on_click=lambda e: gui_try_again(e.sender)).classes('w-40px justify-self-center').set_enabled(nicegui_app.storage.user['allow_try_again'])

    async def gui_search_youtube(button: ui.button) -> None:
        with disable(button):
            try:
                nicegui_app.storage.user['results'] = await run.cpu_bound(search_youtube.search,nicegui_app.storage.user['cat'], nicegui_app.storage.user['params']['st'], nicegui_app.storage.user['lvt'])
            except (ConnectionError, KeyError):
                ui.navigate.to('/rate-limit')
            gui_load_cards.refresh()
            nicegui_app.storage.user['last_search'] = [len(nicegui_app.storage.user['results']),nicegui_app.storage.user['params']['st'],int(nicegui_app.storage.user['lvt'])]
            gui_searched_term.refresh()

    async def gui_try_again(button: ui.button) -> list:
        global try_again_row
        nicegui_app.storage.user['allow_try_again'] = False
        with disable(button):
            with try_again_row:
                ui.spinner(size='lg', color='accent')
            try:
                nicegui_app.storage.user['results'] = await run.cpu_bound(search_youtube.try_again,nicegui_app.storage.user['cat'], nicegui_app.storage.user['params']['st'], nicegui_app.storage.user['lvt'])
            except (ConnectionError, KeyError):
                ui.navigate.to('/rate-limit')
            nicegui_app.storage.user['last_search'] = [len(nicegui_app.storage.user['results']),nicegui_app.storage.user['params']['st'],int(nicegui_app.storage.user['lvt'])]
            gui_load_cards.refresh()

    def gui_randomize():
        nicegui_app.storage.user['allow_try_again'] = True
        if VERBOSE: print('?'*40+'\nGUI: RANDOMIZING...')
        if not nicegui_app.storage.user['cat_lock']:
            nicegui_app.storage.user['lead_lock'] = False
            nicegui_app.storage.user['cat'], nicegui_app.storage.user['lead'], nicegui_app.storage.user['params'] = search_parse.randomize_cat()
            gui_lead_header.refresh()
        else:
            if not nicegui_app.storage.user['lead_lock']:
                nicegui_app.storage.user['lead'], nicegui_app.storage.user['params'] = search_parse.randomize_lead(nicegui_app.storage.user['cat'])
                gui_lead_header.refresh()
            else:
                get_params()

    with main_header:
        with ui.button(on_click=lambda: gui_randomize(), icon='casino').props('flat color=white'):
            ui.tooltip('Randomize').props('delay="1000"')
        with ui.button(icon='lock', on_click=lambda: lock_cat(cat_lock_btn)).props('flat color=white') as cat_lock_btn:
            ui.tooltip('Lock Category').props('delay="1000"')
        with ui.select(options=list(config.cats),on_change=lambda: gui_cat_select()).bind_value(nicegui_app.storage.user,'cat'):
            ui.tooltip('Category').props('delay="1000"')
        
        gui_lead_header()
        get_params()
        gui_update_params()

        ui.space()
        with ui.number(label='Views',value=nicegui_app.storage.user['lvt'],precision=0,min=0).bind_value(nicegui_app.storage.user,'lvt').classes('max-w-15 disable-scrollbars'):
            ui.tooltip('Max Viewcount').props('delay="1000"')
        with ui.button(icon='search',on_click=lambda e:gui_search_youtube(e.sender)).props('flat color=accent') as search_btn:
            ui.tooltip('Search').props('delay="1000"')

    gui_searched_term()

    with ui.grid().classes('w-full').style('grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))'):
        gui_load_cards()

    return {'Hello':'World'}

@ui.page('/about')
def about_page():
    gui_style()
    common_header()
    with main_header:
        ui.space()
        with ui.button(icon='search',on_click=lambda: ui.navigate.to('/')).props('flat color=accent'):
            ui.tooltip('Search').props('delay="1000"')
    with ui.column().classes('justify-center h-full'):
        ui.markdown(json_file.readme())
        ui.space()
        ui.label(nicegui_app.storage.browser['id']).style('color: gray')
        ui.label(device_info.get_device_info()).style('color: gray')

if VERBOSE: print(f'GUI: Running in environment \'{ENVIRONMENT}\'')
if not ENVIRONMENT == 'local':
    @app.get('/')
    def read_root():
        return {'Hello': 'World'}
    ui.run_with(app=app,title=TITLE,favicon=f'{WORKING_DIR}favicon.ico',storage_secret=TITLE)
else:
    nicegui_app.add_static_files(f"/{WORKING_DIR}", f"{WORKING_DIR}")
    ui.run(title=TITLE,storage_secret=TITLE)