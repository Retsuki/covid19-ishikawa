import re
import time
import glob
import json
import requests
import datetime
import calendar
import collections
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


url = 'https://www.pref.ishikawa.lg.jp/kansen/coronakennai.html'
res = requests.get(url)
res.encoding = res.apparent_encoding
soup = BeautifulSoup(res.text, 'html.parser')

tmp_contents = soup.find(id='tmp_contents')

def data_shaping(date):
    m = re.match(r'[0-9]+月[0-9]+日', date_data)
    m_text = m.group()
    pos = re.split('[月日]', m_text)
    datetime_data = datetime.datetime(2020, int(pos[0]), int(pos[1]))
    date = datetime_data.strftime("%Y-%m-%d")
    return date

df = pd.DataFrame([], columns=['date', '居住地', '年代', '性別'])

date = []
residence = []
age = []
sex = []



h3_contents = tmp_contents.find_all('h3')

for i in range(len(h3_contents)):
    data_all = h3_contents[i].find_next_siblings()
    if i != len(h3_contents) - 1:
        data = data_all[:data_all.index(h3_contents[i+1])]
        age.append(data[0].text[-3:-1])
        sex.append(data[1].text[-2:])
        residence.append(data[2].text[-3:].strip())
        for n, j in enumerate(data):
            if '陽性と判明' in str(j):
                s = re.search(r'[0-9]+月[0-9]+日', str(j))
                date_data = s.group(0)
        new_date_data = data_shaping(date_data)
        date.append(new_date_data)
    else:
        data = data_all
        age.append(data[0].text[-3:-1])
        sex.append(data[1].text[-2:])
        residence.append(data[2].text[-3:].strip())
        for n, j in enumerate(data):
            if '陽性と判明' in str(j):
                s = re.search(r'[0-9]+月[0-9]+日', str(j))
                date_data = s.group(0)
        new_date_data = data_shaping(date_data)
        date.append(new_date_data)
        
            
c = collections.Counter(date)
df['date'] = date
df['居住地'] = residence
df['年代'] = age
df['性別'] = sex

patients_df = df.sort_values('date').reset_index(drop=True)
df.to_csv('/home/sakura/covid19-ishikawa/tool/downloads/patients_data/patients.csv', index=False)

# 日付データの作成
today = datetime.datetime.now()
this_year = today.year
this_month = today.month
this_day = today.day
today_info = datetime.datetime(this_year, this_month, 1)
start_date = today_info.strftime("%Y-%m-%d")
month_count = calendar.monthrange(this_year, this_month)[1]
date_column = pd.date_range(start_date, freq='D', periods=this_day)
subtotal_column = [0 for i in range(this_day)]

# 空のデータフレームの作成
progress_map = {'日付': date_column, '小計': subtotal_column}
df = pd.DataFrame(progress_map)

# 条件にマッチした日にデータを挿入
for num, i in enumerate(df.iloc[0:, 0]):
    for j in c.keys():
        if j in str(i):
            df.iloc[num, 1] = c[j]
            
# csv化
df.to_csv('/home/sakura/covid19-ishikawa/tool/downloads/each_data/{}_{}.csv'.format(this_year, this_month), index=False)

time.sleep(5)

# 各csvを連結
csv_files = glob.glob('/home/sakura/covid19-ishikawa/tool/downloads/each_data/*.csv')
each_csv = []
for i in csv_files:
    each_csv.append(pd.read_csv(i))
df = pd.concat(each_csv).reset_index(drop=True).sort_values('日付')

patients_summary_df = df.reset_index(drop=True)
print(patients_summary_df)
