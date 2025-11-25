import config, os, search_parse, search_youtube, json_file
from nicegui import app, ui
from dotenv import load_dotenv
from contextlib import contextmanager

print('\n'*20)
print('*'*40+'\nGUI: STARTING APPLICATION...\n'+'*'*40)
try:
    config.init()
except (TypeError, AttributeError):
    ui.navigate.to('/no-lead')

cat_btn, lead_btn, lvt_btn = config.cat, config.ld, config.lvt

load_dotenv()

environment = os.getenv('ENVIRONMENT','local')
working_dir = os.getenv('WORKING_DIR','docs')
app.add_static_files(f"/docs", f"{working_dir}")

title = 'YouTube Recycle Bin'

@app.on_page_exception
def timeout_error_page(exception: Exception) -> None:
    common_header()
    with ui.column().classes('absolute-center items-center gap-8 w-auto'):
        ui.icon('error_outline', size='xl').style('color: gray')
        ui.label(f'Encountered an issue...').classes('text-2xl').style('color: gray')
        ui.code(str(exception)).classes('w-auto')
        ui.button('Try Again',on_click=lambda:ui.navigate.to('/')).classes('w-40px justify-self-center')

@ui.page('/no-lead')
def raise_filenotfound_error():
    if not config.lds:
       raise FileNotFoundError('Could not find leads file in \'{working_dir}\'...')
    else:
        ui.navigate.to('/')

@ui.page('/rate-limit')
def raise_ratelimit_error():
    raise ConnectionError('Couldn\'t reach YouTube...')

@ui.page('/search-error')
def raise_search_error():
    if not config.st:
        config.results=False
        search_parse.randomize_lead()
        gui_load_cards.refresh()
        raise TypeError(f'Had trouble using lead \'{config.ld}\'...')
    else:
        ui.navigate.to('/')

@contextmanager
def disable(button: ui.button):
    button.disable()
    try:
        yield
    finally:
        button.enable()

def gui_find_leads():
    global enable_try_again, enable_search, lead_lock, cat_lock, verbose
    if config.lds:
        print("GUI: FOUND LEADS...")
        enable_try_again = enable_search = cat_lock = True
        lead_lock = False
        verbose = True
    else:
        ui.navigate.to('/no-lead')

def get_params():
    config.cat, config.ld = cat_btn, lead_btn
    try:
        search_parse.params()
    except (IndexError, TypeError):
        ui.navigate.to('/search-error')
    gui_update_params.refresh()

@ui.refreshable
def gui_update_params():
    global date_picker, time_picker
    if config.rh:
        for r in config.rh:
            ui.input(label='X'*len(r),value=r).classes('max-w-15').set_enabled(False)

    if config.rn:
        for r in config.rn:
            if config.prm:
                rmin, rmax = config.prm[0][0], config.prm[0][1]
            else:
                rmin = 0
                rmax = 9999
            ui.number(label='X'*len(r),value=r,min=rmin,max=rmax).classes('max-w-15').set_enabled(False)

    if config.date_eval:
        date_picker = config.date_picker
        if config.prm:
            date_after = f' (after {config.prm[0]})'
        else:
            date_after = ''
        ui.date_input(label=f'Date{date_after}', value=date_picker).bind_value(globals(),'date_picker').classes('w-auto max-w-38').set_enabled(False)

    if config.time_eval:
        time_picker = config.time_picker
        ui.time_input(label='Time', value=time_picker).bind_value(globals(),'time_picker').classes('max-w-32').set_enabled(False)

def gui_randomize():
    global lead_lock, enable_try_again, cat_btn, lead_btn
    enable_try_again = True
    print('?'*40+'\nGUI: RANDOMIZING...')
    if not cat_lock:
        lead_lock = False
        search_parse.randomize_cat()
        cat_btn, lead_btn = config.cat, config.ld
        gui_lead_header.refresh()
    else:
        if not lead_lock:
            search_parse.randomize_lead()
            lead_btn = config.ld
            gui_lead_header.refresh()
        else:
            get_params()

async def gui_search_youtube(button: ui.button) -> None:
    with disable(button):
        config.cat, config.ld, config.lvt = cat_btn, lead_btn, lvt_btn
        try:
            await search_youtube.search()
        except (ConnectionError, KeyError):
            ui.navigate.to('/rate-limit')
        searched_term.refresh()
        gui_load_cards.refresh()

async def gui_try_again(button: ui.button) -> None:
    global enable_try_again
    enable_try_again = False
    with disable(button):
        await search_youtube.try_again()
        gui_load_cards.refresh()

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
                background-image: url("docs/external-link-26.png");
                filter: invert(100%);
            }
        ''')
        self.classes('text-accent ext w-40px')

@ui.refreshable
def gui_load_cards():
    if config.results:
        print(f"GUI: FETCHING RESULTS...")
        for result in config.results:
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
                with ui.card().tight().props('bordered flat').style('max-width: 500px;').classes('bg-secondary'):
                    ui.image(tmb).classes('aspect-180/101; max-h-280px max-w-500px')
                    with ui.card_section():
                        ui.label(ti).style('color: white; font-weight: 1000')
                        with ui.row().style('color: white'):
                            ui.label(vw)
                            ui.label(up)
                        ui.label(ch).style('color: grey')
                        ui.label(ds)
    else:
        if config.results == False:
            print(f"GUI: NO RESULTS, NEW INSTANCE...")
            with ui.column().classes('absolute-center w-3/4'):
                ui.space()
                ui.label('Welcome to the YouTube Recycle Bin').style('font-size: 200%')
                ui.label('🎲 Randomize and 🔎 Search to get started...')
        else:
            print(f"GUI: NO RESULTS, NO MATCH...")
            with ui.column().classes('absolute-center w-7/8').style(replace=''):
                ui.space()
                ui.icon('help_outline', size='xl').style('color: gray')
                with ui.row(wrap=False):
                    info = f'Nothing here for \'{config.st}\' with less than {format(int(config.lvt),',')} views...\t'
                    info = info.replace('less than 0','no').replace('1 videos', '1 video')
                    ui.label(info).style('color: gray').classes('w-3/5 justify-center')
                    ui.space()
                    YouTubeLink(config.st)
                ui.button('Try Again',on_click=lambda e: gui_try_again(e.sender)).classes('w-40px justify-self-center').set_enabled(enable_try_again)

@ui.refreshable
def searched_term():
    if config.results:
        with ui.row().classes(replace='row items-center w-[100%] no-wrap').style('margin: 0; padding: 0; display: flex;'):
            info = f'Found {len(config.results)} videos matching \'{config.st}\' with less than {format(int(config.lvt),',')} views...\t'
            info = info.replace('less than 0','no').replace('1 videos', '1 video')
            ui.label(info)
            ui.space()
            YouTubeLink(config.st)

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
    with ui.header().classes(replace='gap-4 row items-center min-h-14 px-4 grid-rows-1 grid-flow-col absolue-full') as main_header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white').classes('md:px-0')
        # ui.label('YouTube Recycle Bin')
        with ui.link(target='/'):
            ui.interactive_image('/docs/YTRB_logo_beta.png').style('max-width: 100px').classes('display:block')

    with ui.left_drawer(value=False).classes('bg-dark disable-scrollbar').props('width=60') as left_drawer:
        ui.space()
        with ui.link(target='https://github.com/zauberzeug/nicegui',new_tab=True):
            with ui.interactive_image('https://nicegui.io/logo.png').classes('w-full h-auto invert'):
                ui.tooltip('Built with NiceGUI').props('delay="1000" anchor="center right" self="center left"')
        with ui.link(target='https://github.com/SiriusArtistry/youtube-recycle-bin',new_tab=True):
            with ui.interactive_image('/docs/github-mark-white.png').classes('w-full h-auto'):
                ui.tooltip('Source code on Github').props('delay="1000" anchor="center right" self="center left"')
        with ui.link(target='/about'):
            with ui.icon('info',color='white', size='25px'):
                ui.tooltip('About').props('delay="1000" anchor="center right" self="center left"')

    ui.query('body').style(f'background-color: dark_page')
    ui.colors(primary='#212121', secondary='#1D1D1D', accent="#FF0033", dark_page='#111111')
    ui.dark_mode(True)

@ui.refreshable
def gui_lead_header():
    global lead_lock_btn, enable_try_again, lead_btn
    enable_try_again = True
    lead_btn = config.ld
    with ui.button(icon='lock_open', on_click=lambda: lock_lead(lead_lock_btn)).props('flat color=white') as lead_lock_btn:
        ui.tooltip('Lock Lead').props('delay="1000"')
    with ui.select(label='Lead',options=list(config.cat_key), with_input=True,on_change=lambda: gui_lead_select()).bind_value(globals(),'lead_btn').classes('w-500px text-white'):
        ui.tooltip('Lead').props('delay="1000"')
            
    gui_update_params.refresh()

def gui_lead_select():
    search_parse.lead_select(lead_btn)
    gui_update_params.refresh()

def gui_cat_select():
    search_parse.cat_select(cat_btn)
    gui_lead_header.refresh()

@ui.page('/')
def main_page():
    # global main_header
    print('.'*40+'\nGUI: MAIN PAGE')
    gui_find_leads()
    common_header()
    with main_header:
        with ui.button(on_click=lambda: gui_randomize(), icon='casino').props('flat color=white'):
            ui.tooltip('Randomize').props('delay="1000"')
        with ui.button(icon='lock', on_click=lambda: lock_cat(cat_lock_btn)).props('flat color=white') as cat_lock_btn:
            ui.tooltip('Lock Category').props('delay="1000"')
        with ui.select(options=list(config.cats),on_change=lambda: gui_cat_select()).bind_value(globals(),'cat_btn'):
            ui.tooltip('Category').props('delay="1000"')
        
        gui_lead_header()
        get_params()
        gui_update_params()

        ui.space()
        with ui.number(label='Views',value=config.lvt,precision=0,min=0).bind_value(globals(),'lvt_btn').classes('max-w-15 disable-scrollbars'):
            ui.tooltip('Max Viewcount').props('delay="1000"')
        with ui.button(icon='search',on_click=lambda e:gui_search_youtube(e.sender)).props('flat color=accent') as search_btn:
            ui.tooltip('Search').props('delay="1000"')

    searched_term()

    with ui.grid().classes('w-full').style('grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))'):
        gui_load_cards()

@ui.page('/about')
def about_page():
    common_header()
    with main_header:
        ui.space()
        with ui.button(icon='search',on_click=lambda: ui.navigate.to('/')).props('flat color=accent'):
            ui.tooltip('Search').props('delay="1000"')
    with ui.column().classes('justify-center'):
        ui.markdown(json_file.readme())

print(f'GUI: Running in environment \'{environment}\'')
if not environment == 'local':
    ui.run_with(app,title=title,favicon='♻️')
else:
    ui.run(title=title)