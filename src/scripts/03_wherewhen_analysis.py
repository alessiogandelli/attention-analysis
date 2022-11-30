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

# INIZIA DA QUI ####################################


''' get yardstick'''

query = "select * from yd where userid in {} ".format(tuple(userids))
df_yd = pd.read_sql(query, db.connection)
df_yd['day'] = pd.to_datetime(df_yd[['year', 'month', 'day']])
df_yd = df_yd[['userid', 'day', 'hour', 'min']]
df_yd = df_yd.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]'})


''' get time diary  '''

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

query = '''select  app.userid,
        date(app.timestamp) as day,  
        strftime('%H', app.timestamp) as hour, 
        strftime('%M', app.timestamp) as min, 
        application as apps 
        from application as app

    group by app.userid, 
            date(app.timestamp), 
            strftime('%H', app.timestamp), 
            strftime('%M', app.timestamp)'''

df_app = pd.read_sql(query, db.connection)
df_app = df_app.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]'})
# drop every column except timestamp userid and what 


#%%
# join tables 
df = df_yd.merge(df_diary, on = ['userid','day', 'hour', 'min'], how = 'left')
df = df.merge(df_touch, on = ['userid','day', 'hour', 'min'], how = 'left')
df = df.merge(df_app, on = ['userid','day', 'hour', 'min'], how = 'left')

df = df.sort_values(['userid','day', 'hour', 'min'])
df['id'] = range(len(df))
df = df.set_index('id')
df['what'] = df['what'].fillna(method='ffill')
df['touches'] = df['touches'].fillna(0).astype('int64')



df = df[df['apps'].str.contains('launcher') == False]
df = df[df['apps'] != '']
df = df[df['apps'] != 'com.miui.home' ]
df = df[df['apps'] != 'it.unitn.disi.witmee.sensorlog' ]





# %%
gp = df.groupby(['what','apps'])['touches'].count()
gp = gp.reset_index().sort_values(['what','touches'], ascending = False)

# drop rows where app is launcher 


# get top three for each what
gp = gp.groupby('what').head(3)
# %%
