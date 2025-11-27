from youtube_search import YoutubeSearch
import config

num_results = 300
max_results = 5000

def search(cat, st, lvt, num_results=num_results):
    if cat == "new":
        sf = "&sp=CAI%253D"
    elif cat == "old":
        sf = "&sp=CAMSAhAB"
    elif cat == "low":
        st = st + " Before:2008"

    if config.VERBOSE: print('%'*40)
    if config.VERBOSE: print(f'SYT: SEARCHING YOUTUBE FOR {num_results} VIDEOS...')

    all_results = YoutubeSearch(st, num_results).to_dict()

    lv_results = []
    if config.VERBOSE: print(f'SYT: FOUND {len(all_results)} VIDEOS MATCHING \'{st}\'...')
    for result in all_results:
        rt = result['title']
        rv = result['views']
        if not isinstance(rv,int):
            rvi = int(rv.replace(',','').replace(' views','').replace(' view','').replace('No','0'))
        else:
            rvi = int(rv)
        ru = result['publish_time']

        if rvi < lvt + 1:
            lv_results.append(result)

        if config.VERBOSE: print('-'*40)
        if config.VERBOSE: print(f'Title:\t\t{rt}')
        if config.VERBOSE: print(f'Views:\t\t{rv}')
        if config.VERBOSE: print(f'Uploaded:\t{ru}')

    if config.VERBOSE: print('-'*40)
    if config.VERBOSE: print(f'SYT: FOUND {len(lv_results)}/{len(all_results)} VIDEOS WITH LESS THAN {lvt} VIEWS...')
    if config.VERBOSE: print('%'*40)

    return lv_results

def try_again(cat, st, lvt):
    lv_results = False
    more_results = 0
    while not lv_results and more_results<max_results-(num_results):
        more_results += 300
        if config.VERBOSE: print(f"SYT: SETTING MAX RESULTS TO: {num_results+more_results}...")
        lv_results = search(cat, st, lvt, num_results+more_results)
    return lv_results