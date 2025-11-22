from random import randrange, randint, choice
from datetime import timedelta, datetime

def random_choice(input):
    return choice(list(input.keys()))

def date_range():
    return '2025-04-23 - '+datetime.strptime(datetime.now(), '%Y-%m-%d')

def random_date(start, end):
    if start == "youtube":
        start = datetime.strptime('4/23/2005 12:00 AM', '%m/%d/%Y %I:%M %p')
    if end == "today":
        end = datetime.now()
    if isinstance(start,int):
        start = datetime.strptime(f'1/1/{start} 12:00 AM', '%m/%d/%Y %I:%M %p')
    if isinstance(end,int):
        end = datetime.strptime(f'1/1/{end} 12:00 AM', '%m/%d/%Y %I:%M %p')

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def rNd(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return str(randint(0, range_end)).zfill(n)

def rNh(n):
    return str(hex(randint(0,16**n)).upper()[2:]).zfill(n)