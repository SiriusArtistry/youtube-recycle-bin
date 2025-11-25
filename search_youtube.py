from youtube_search import YoutubeSearch
import config

num_results = 300
max_results = 5000

async def search(num_results=num_results):
    if config.cat == "new":
        sf = "&sp=CAI%253D"
    elif config.cat == "old":
        sf = "&sp=CAMSAhAB"
    elif config.cat == "low":
        config.st = config.st + " Before:2008"

    print('%'*40)
    print(f'SYT: SEARCHING YOUTUBE FOR {num_results} VIDEOS...')

    all_results = YoutubeSearch(config.st, num_results).to_dict()

    lv_results = []
    print(f'SYT: FOUND {len(all_results)} VIDEOS MATCHING \'{config.st}\'...')
    for result in all_results:
        rt = result['title']
        rv = result['views']
        if not isinstance(rv,int):
            rvi = int(rv.replace(',','').replace(' views','').replace(' view','').replace('No','0'))
        else:
            rvi = int(rv)
        ru = result['publish_time']

        if rvi < config.lvt + 1:
            lv_results.append(result)

        print('-'*40)
        print(f'Title:\t\t{rt}')
        print(f'Views:\t\t{rv}')
        print(f'Uploaded:\t{ru}')

    print('-'*40)
    print(f'SYT: FOUND {len(lv_results)}/{len(all_results)} VIDEOS WITH LESS THAN {config.lvt} VIEWS...')
    print('%'*40)

    config.results = lv_results
    return

async def try_again():
    config.results = False
    more_results = 0
    while not config.results and more_results<max_results-(num_results):
        more_results += 300
        print(f"SYT: SETTING MAX RESULTS TO: {num_results+more_results}...")
        await search(num_results+more_results)
    return