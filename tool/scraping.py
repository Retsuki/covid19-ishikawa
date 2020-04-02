import os
import re
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
h1_contents = tmp_contents.find_all('h1')
all_contents_list = h1_contents[0].find_next_siblings()

def data_shaping(date):
    m = re.match(r'[0-9]+月[0-9]+日', date)
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

table = str.maketrans('（１）', '(1)')
all_contents = ""
now_date = ""
now_age = ""
new_text = ""
new_text_list = []
infect_count = 0
for i in all_contents_list:
    text = i.get_text().translate(table)
    text2 = text.replace("\xa0", "").replace("\r\n", "").replace(" ", "").replace("\u3000", "").replace("\n", "")
   
    if "(1)年代" in text2:
        text_age = re.findall("[0-9]+", text2)[-1]
        age.append(text_age)
    elif "(2)性別" in text2:
        text_sex = text2[5:]
        sex.append(text_sex)
    elif "(3)居住地" in text2:
        text_residence = text2[6:]
        residence.append(text_residence)
        
    if "症状・経過" in text2:
        
        # 新たなlistの要素を作る
        new_text_list.append("empty")
        
        # 初期設定
        if now_age == "":
            now_age = text2 + "check"
            new_text += text2
            infect_count += 1
            continue
            
        # now_ageとtext2の内容が違うのであれば
        # (1)Save ever data
        # (2)Delete ever data
        # (3)Add new data
        if now_age != text2:
            new_text_list[infect_count-1] = new_text # (1)
            new_text = "" # (2)
            new_text += text2 # (3)
            infect_count += 1
            continue
    
    if 0 < infect_count:
        if "(5)行動歴" in text2:
            continue
        new_text += text2
        

new_text_list[infect_count-1] = new_text

for i in new_text_list:
    target_index = i.find("陽性と判明")
    result = i[:target_index]
    s = re.findall(r'[0-9]+月[0-9]+日', result)
    new_data = data_shaping(s[-1])
    date.append(new_data)

c = collections.Counter(date)

df['date'] = date
df['居住地'] = residence
df['年代'] = age
df['性別'] = sex

patients_df = df.sort_values('date').reset_index(drop=True)
patients_df.to_csv('./tool/downloads/patients_data/patients.csv', index=False)

# 日付データの作成
today = datetime.datetime.now()
this_year = today.year
this_month = today.month
this_day = today.day
this_hour = today.hour
this_minute = today.minute
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
df.to_csv('./tool/downloads/each_data/{}_{}.csv'.format(this_year, this_month), index=False)

# 各csvを連結
csv_files = glob.glob('./tool/downloads/each_data/*.csv')
each_csv = []
for i in csv_files:
    each_csv.append(pd.read_csv(i))
df = pd.concat(each_csv).reset_index(drop=True)

patients_summary_df = df.sort_values("日付").reset_index(drop=True)
patients_summary_df.to_csv("./tool/downloads/final_data/total.csv", index=False)

# patientsデータの作成
patients_df_dict = patients_df.to_dict('index')
data1 = [ patients_df_dict.get(i) for i in range(len(patients_df_dict)) ]

# patients_summaryデータの作成
patients_summary_df_dict = patients_summary_df.to_dict('index')
data2 = [ patients_summary_df_dict.get(i) for i in range(len(patients_summary_df)) ]

update_at = "{}/{}/{} {}:{}".format(this_year, this_month, this_day, this_hour, this_minute)
data_json = {
    "lastUpdate": update_at,
    "patients": {
        "date": update_at,
        "data": data1
    },
    "patients_summary": {
        "date": update_at,
        "data": data2
    }
}

with open('./data/data.json', 'w') as f:
    json.dump(data_json, f, indent=4, ensure_ascii=False)