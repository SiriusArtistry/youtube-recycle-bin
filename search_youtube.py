from youtube_search import YoutubeSearch
import search_term as st
import json_file as jf

category = 'old'
lvt = 100


s_term = st.search_term(category,verbose=True)

if category == "new":
    s_filter = "&sp=CAI%253D"
elif category == "old":
    s_filter = "&sp=CAMSAhAB"
elif category == "low":
    s_term = s_term + " Before:2008"

# url = f'https://www.youtube.com/results?search_query={s_term}{s_filter}'

results = YoutubeSearch(s_term, max_results=30).to_dict()
lv_results = []

for result in results:
    rt = result['title']
    rv = result['views']
    rvi = int(rv.replace(',','').replace(' views','').replace(' view','').replace('No','0'))
    ru = result['publish_time']

    if rvi < lvt:
        lv_results.append(result)

    print('-'*40)
    print(f'Title:\t\t{rt}')
    print(f'Views:\t\t{rv}')
    print(f'Uploaded:\t{ru}')

print(f'Found {len(results)} videos matching \'{s_term}\'...')
print(f'Found {len(lv_results)} videos with less than {lvt} views...')

jf.save(results)
jf.save(lv_results,'files/lv_result')