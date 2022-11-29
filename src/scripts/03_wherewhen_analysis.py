#%%
from database_helper import Database
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import json
db = Database('/Volumes/boot420/Users/alessiogandelli/data_social_dynamics/aaa.db')

#read userid from json file
with open('/Users/alessiogandelli/dev/uni/attention-analysis/data/userids.json') as f:
    userids = json.load(f)['userid_ww']

# %%

query = "select userid, date, time, timestamp ,what, where2, withwho from diary where userid in {} ".format(tuple(userids))

df = pd.read_sql(query, db.connection)

df.value_counts('what')
# change 



# %%
df = df[df['date'] == '2020-11-20'].groupby(['timestamp', 'what']).size().unstack(fill_value = 0)

# %%
df.plot(kind = 'area', stacked = True, figsize = (20, 10), title = 'Diary events per minute')
# %%
# %%

# %%
df.index = pd.to_datetime(df.index)
df.plot(kind = 'area', stacked = True, figsize = (20, 10), title = 'Diary events per minute').legend(loc='center left',bbox_to_anchor=(1.0, 0.5));
plt.xticks(rotation = 90)
#add one tick per hour 
#plt.xticks(ticks = df.index[::60], labels = df.index[::60])





#%%

query = '''SELECT diary.userid, year, month, day, hour, min, diary.what 
            FROM yd
            LEFT JOIN diary 
            ON  yd.year = strftime('%Y', diary.timestamp) AND
                yd.month = strftime('%m', diary.timestamp) AND
                yd.day = strftime('%d', diary.timestamp) AND
                yd.hour = strftime('%H', diary.timestamp) AND
                yd.userid = diary.userid order by diary.timestamp'''

df = pd.read_sql(query, db.connection)
# %%

# INIZIA DA QUI ####################################




query = "select * from yd where userid in {} ".format(tuple(userids))
df_yd = pd.read_sql(query, db.connection)
df_yd['day'] = pd.to_datetime(df_yd[['year', 'month', 'day']])
df_yd = df_yd[['userid', 'day', 'hour', 'min']]
df_yd = df_yd.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]'})




query = "select * from diary where userid in {} ".format(tuple(userids))
df_diary = pd.read_sql(query, db.connection)
df_diary = df_diary[['timestamp', 'userid', 'what']]

df_diary['timestamp'] = pd.to_datetime(df_diary['timestamp'])
df_diary['day'] = df_diary['timestamp'].dt.date
df_diary['hour'] = df_diary['timestamp'].dt.hour
df_diary['min'] = df_diary['timestamp'].dt.minute
df_diary = df_diary.drop('timestamp', axis=1)
df_diary = df_diary.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]'})




#%%
query ="""select  touch.userid, 
        date(touch.timestamp) as day,  
        strftime('%H', touch.timestamp) as hour, 
        strftime('%M', touch.timestamp) as min, 
        count(*) as touches
from touch
group by touch.userid, 
        date(touch.timestamp), 
        strftime('%H', touch.timestamp), 
        strftime('%M', touch.timestamp)

"""
df_touch = pd.read_sql(query, db.connection)
df_touch = df_touch.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]'})


#%%
# drop every column except timestamp userid and what 


#%%
# join tables 
df = df_yd.merge(df_diary, on = ['userid','day', 'hour', 'min'], how = 'left')
df = df.merge(df_touch, on = ['userid','day', 'hour', 'min'], how = 'left')


df = df.sort_values(['userid','day', 'hour', 'min'])
df['id'] = range(len(df))
df = df.set_index('id')
df['what'] = df['what'].fillna(method='ffill')
df['touches'] = df['touches'].fillna(0).astype('int64')



# %%
## fillna method ffill 
df['what'] = df['what'].fillna(method = 'ffill')

#set max rows to 1000
pd.set_option('display.max_rows', 1000)
# %%
