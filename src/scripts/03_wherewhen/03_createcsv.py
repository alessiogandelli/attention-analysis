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

# in the next cell we query  the databse to get the data grouped by minute
# we get yardstick, time diary, touches and socio demographic data


''' get yardstick'''

query = "select * from yd where userid in {} ".format(tuple(userids))
df_yd = pd.read_sql(query, db.connection)
df_yd['day'] = pd.to_datetime(df_yd[['year', 'month', 'day']])
df_yd = df_yd[['userid', 'day', 'hour', 'min']]
df_yd = df_yd.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]'})


''' get time diary  '''
#%%
query = "select * from diary where userid in {} ".format(tuple(userids))
df_diary = pd.read_sql(query, db.connection)
df_diary = df_diary[['timestamp', 'userid', 'what']]

df_diary['timestamp'] = pd.to_datetime(df_diary['timestamp'])
df_diary['day'] = df_diary['timestamp'].dt.date
df_diary['hour'] = df_diary['timestamp'].dt.hour
df_diary['min'] = df_diary['timestamp'].dt.minute
df_diary = df_diary.drop('timestamp', axis=1)
df_diary = df_diary.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]'})

# merge sleeping and i will go to sleep 
df_diary['what'] = df_diary['what'].replace('I will go to sleep', 'Sleeping')
df_diary['what'] = df_diary['what'].replace('Rest/nap/anything', 'Sleeping')

df_diary['what'] = df_diary['what'].replace('Eating', 'Food-related')
df_diary['what'] = df_diary['what'].replace('Cooking', 'Food-related')

df_diary['what'] = df_diary['what'].replace('Watching/TV/YouTube', 'Entertainment')
df_diary['what'] = df_diary['what'].replace('FreeTime_culture', 'Entertainment')
df_diary['what'] = df_diary['what'].replace('FreeTime_sports', 'Entertainment')
df_diary['what'] = df_diary['what'].replace('I am at the cinema/theater/hospital/church', 'Entertainment')
df_diary['what'] = df_diary['what'].replace('Listeningmusic/Reading', 'Entertainment')
df_diary['what'] = df_diary['what'].replace('I will participate in sports activities', 'Entertainment')

df_diary['what'] = df_diary['what'].replace('No information', 'Missing')
df_diary['what'] = df_diary['what'].replace('Expired', 'Missing')

df_diary['what'] = df_diary['what'].replace('Lecture', 'Work/Class')
df_diary['what'] = df_diary['what'].replace('Work/Other', 'Work/Class')
df_diary['what'] = df_diary['what'].replace('I am starting classes/lessons/lab', 'Work/Class')
df_diary['what'] = df_diary['what'].replace('I have a work/study meeting', 'Work/Class')

df_diary['what'] = df_diary['what'].replace('on foot', 'Moving')
df_diary['what'] = df_diary['what'].replace('TravelPubTrans', 'Moving')
df_diary['what'] = df_diary['what'].replace('Drive/bike/car', 'Moving')







#%%

'''touch events'''


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
''' application events '''


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

df_app = df_app[df_app['apps'].str.contains('launcher') == False]
df_app = df_app[df_app['apps'] != '']
df_app = df_app[df_app['apps'] != 'com.miui.home' ]
df_app = df_app[df_app['apps'] != 'it.unitn.disi.witmee.sensorlog' ]


#replace app  names that cointsns call with call 
# drop every column except timestamp userid and what 

#%%
''' socio demographics '''

query = "select * from socio where userid in {} ".format(tuple(userids))
df_socio = pd.read_sql(query, db.connection)
df_socio = df_socio[['userid', 'age', 'gender', 'nationality', 'department', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness', 'degree']]

#%%
''' notification '''

query = '''select userid,
                date(timestamp) as day,  
                strftime('%H', timestamp) as hour, 
                strftime('%M', timestamp) as min, 
                source as notification 
        from notification 
        group by 
                userid, 
                date(timestamp), 
                strftime('%H', timestamp), 
                strftime('%M', timestamp)'''

df_notif = pd.read_sql(query, db.connection)
df_notif = df_notif.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]'})


df['day'] = df['day'].astype('datetime64[ns]')

#%%



''' join tables yardstick app and time diary '''



df = df_yd.merge(df_diary, on = ['userid','day', 'hour', 'min'], how = 'left')
df = df.merge(df_touch, on = ['userid','day', 'hour', 'min'], how = 'left')
df = df.merge(df_app, on = ['userid','day', 'hour', 'min'], how = 'left')
df = df.merge(df_socio, on = ['userid'], how='left')
df = df.merge(df_notif, on = ['userid','day', 'hour', 'min'], how = 'left')


df.astype({'hour': 'int64', 'min': 'int64', 'day': 'datetime64[ns]', 'age': 'int64', 'apps': 'str', 'gender': 'str'})
#%%
# to csv 
# sort and reset index fixing the missing values 

df = df.sort_values(['userid','day', 'hour', 'min'])
df['id'] = range(len(df))
df = df.set_index('id')
df['what'] = df['what'].fillna(method='ffill')
df['touches'] = df['touches'].fillna(0).astype('int64')


df['apps'] = df['apps'].str.replace('com\.', '')
df['apps'] = df['apps'].str.replace('org\.', '')
df['apps'] = df['apps'].str.replace('net\.', '')
df['apps'] = df['apps'].str.replace('it\.', '')
df['apps'] = df['apps'].str.replace('android', '')
df['apps'] = df['apps'].str.replace('google', '')
df['apps'] = df['apps'].str.replace('sec', '')
df['apps'] = df['apps'].str.replace('samsung', '')
df['apps'] = df['apps'].str.replace('\.app', '')
df['apps'] = df['apps'].str.replace('\.\.', '.')
df['apps'] = df['apps'].str.replace('^\.', '', regex=True)
df['apps'] = df['apps'].str.replace('\.$', '', regex=True)

df['notification'] = df['notification'].str.replace('com\.', '')
df['notification'] = df['notification'].str.replace('org\.', '')
df['notification'] = df['notification'].str.replace('net\.', '')
df['notification'] = df['notification'].str.replace('it\.', '')
df['notification'] = df['notification'].str.replace('android', '')
df['notification'] = df['notification'].str.replace('google', '')
df['notification'] = df['notification'].str.replace('sec', '')
df['notification'] = df['notification'].str.replace('samsung', '')
df['notification'] = df['notification'].str.replace('\.app', '')
df['notification'] = df['notification'].str.replace('\.\.', '.')
df['notification'] = df['notification'].str.replace('^\.', '', regex=True)
df['notification'] = df['notification'].str.replace('\.$', '', regex=True)

df['age'] = df['age'].astype('str')
df['age'] = df['age'].replace('17-18', '18', regex=False)
df['age'] = df['age'].replace('25-26', '25', regex=False)
df['age'] = df['age'].replace('27-30', '29', regex=False)
df['age'] = df['age'].replace('31+', '31', regex=False)
df['age'] = df['age'].astype('int64')











df.to_csv('merged_data.csv', index = False)



#%%

# p2 plots n the same figure 







#%%




# %%
#import csv filek 
df = pd.read_csv('merged_data.csv')
# %%


'''a typical day'''

df_area = df_diary[df_diary['day'] == '2020-11-20'].groupby(['hour','min', 'what']).size().unstack(fill_value = 0)

df_area.plot(kind = 'area', stacked = True, figsize = (20, 10), title = 'Diary events per minute', colormap = 'tab20')
plt.xticks(rotation = 90)
# y axis  in percentage 
import matplotlib.ticker as mtick
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(160))
