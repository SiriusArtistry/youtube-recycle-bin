import search_term as st
import webbrowser

category = 'old'

s_term = st.search_term(category,verbose=True)

if category == "new":
    s_filter = "&sp=CAI%253D"
elif category == "old":
    s_filter = "&sp=CAMSAhAB"
elif category == "low":
    s_filter = " Before:2008"

url = f'https://www.youtube.com/results?search_query={s_term}{s_filter}'

print(url)
# webbrowser.open(url, new=0, autoraise=True)