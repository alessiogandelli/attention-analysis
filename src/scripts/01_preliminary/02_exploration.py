#%%
from database_helper import Database
import pandas as pd
import datetime
from venn import venn
import matplotlib.pyplot as plt
db = Database('/Users/alessiogandelli/data_social_dynamics/social_dynamics.sqlite')
import json


#%%
# get data from db and cast to set 

td_userid = db.query("select distinct userid from diary")
socio_userid = db.query("select distinct userid from socio")
loc_userid = db.query("select distinct userid from location")
not_userid = db.query("select distinct userid from notification")
app_userid = db.query("select distinct userid from application")
touch_userid = db.query("select distinct userid from touch")
screen_userid = db.query("select distinct userid from screen")

td_userid = set([i[0] for i in td_userid])
socio_userid = set([i[0] for i in socio_userid])
loc_userid = set([i[0] for i in loc_userid])
not_userid = set([i[0] for i in not_userid])
app_userid = set([i[0] for i in app_userid]) 
touch_userid = set([i[0] for i in touch_userid])
screen_userid = set([i[0] for i in screen_userid])

#%%
app_userid = app_userid - userid_noapp # computed later in the notebook
# some set operations
all_userid = td_userid | socio_userid | loc_userid | not_userid | app_userid | touch_userid | screen_userid

td_missing = all_userid - td_userid
socio_missing = all_userid - socio_userid
loc_missing = all_userid - loc_userid
not_missing = all_userid - not_userid
app_missing = all_userid - app_userid 
touch_missing = all_userid - touch_userid
screen_missing = all_userid - screen_userid

missing_all_sensors = loc_missing & not_missing & app_missing & touch_missing & screen_missing

some_sensors_userid = all_userid - missing_all_sensors # remove missing all sensors 


useful_td_missing = some_sensors_userid - td_userid
useful_socio_missing = some_sensors_userid - socio_userid
useful_touch_missing = some_sensors_userid - touch_userid

useful_userid = some_sensors_userid - useful_td_missing - useful_socio_missing - useful_touch_missing # remove missing from td and socio
discarded_userid = useful_td_missing | useful_socio_missing | useful_touch_missing |missing_all_sensors # remove useful

useful_loc_missing = useful_userid - loc_userid
useful_not_missing = useful_userid - not_userid
useful_app_missing = useful_userid - app_userid
useful_screen_missing = useful_userid - screen_userid

useful_all_sensors = useful_userid - useful_loc_missing - useful_not_missing - useful_app_missing - useful_screen_missing

userid_ww = useful_userid - useful_screen_missing - useful_loc_missing 
userid_ext = useful_userid - useful_not_missing - useful_screen_missing
userid_app = useful_userid - useful_app_missing

# create dataframe with userid_ww ,userid_ext, userid_app
userids = {'userid_ww':list(userid_ww), 'userid_ext':list(userid_ext), 'userid_app':list(userid_app)}
#save on json
with open('/Users/alessiogandelli/Desktop/attention-analysis/data/userids.json', 'w') as fp:
    json.dump(userids, fp)






# print the results
print('\nthere are '+str(len(td_userid))+ ' users with diary data')
print('there are '+str(len(socio_userid))+ ' users with socio data')
print('there are '+str(len(loc_userid))+ ' users with location data')
print('there are '+str(len(not_userid))+ ' users with notification data')
print('there are '+str(len(app_userid))+ ' users with application data')
print('there are '+str(len(touch_userid))+ ' users with touch data')
print('there are '+str(len(screen_userid))+ ' users with screen data')


print('\nthere are '+str(len(td_missing))+ ' users with missing time diary')
print('there are '+str(len(socio_missing))+ ' users with missing socio')
print('there are '+str(len(loc_missing))+ ' users with missing location')
print('there are '+str(len(not_missing))+ ' users with missing notification')
print('there are '+str(len(app_missing))+ ' users with missing application')
print('there are '+str(len(touch_missing))+ ' users with missing touch')
print('there are '+str(len(screen_missing))+ ' users with missing screen')

print( '\nthere are '+str(len(missing_all_sensors)+len(useful_td_missing) + len(useful_socio_missing)+ len(useful_touch_missing)) +' users with missing all sensors data or time diary or socio or touch')


print('from the remaining '+str(len(useful_userid))+' users, '+str(len(useful_loc_missing))+' have missing location data')
print('from the remaining '+str(len(useful_userid))+' users, '+str(len(useful_not_missing))+' have missing notification data')
print('from the remaining '+str(len(useful_userid))+' users, '+str(len(useful_app_missing))+' have missing application data')
print('from the remaining '+str(len(useful_userid))+' users, '+str(len(useful_touch_missing))+' have missing touch data')
print('from the remaining '+str(len(useful_userid))+' users, '+str(len(useful_screen_missing))+' have missing screen data')

print('\nFor When and when questions, we can use '+str(len(userid_ww))+' users')
print('For internal or external questions, we can use '+str(len(userid_ext))+' users')
print('For Application questions, we can use '+str(len(userid_app))+' users')

#%%
# visualize missing users 

venn({'missing location': useful_loc_missing, 'missig notification': useful_not_missing, 'missing app' : useful_app_missing})
venn({'all users': all_userid, 'complete data' : useful_all_sensors, 'discarded users' : discarded_userid })


#%%
##  table by table exploration ############################


###### diary  ############################
df = pd.read_sql_query("select * from diary", db.connection)
df = df.loc[df['userid'].isin(useful_userid)]
df = df.loc[df['userid'].isin(useful_userid)]

df[df['first2w'] == 'First two weeks' ].groupby('userid').count().sort_values('userid')
df[df['first2w'] != 'First two weeks' ].groupby('userid').count().sort_values('userid')

df.groupby('date').count().plot(type='bar', figsize=(20,10))

#count unique users by date
df.groupby('date').nunique().plot(type='bar', figsize=(20,10))

########################  touch  grouped by hour
df = pd.read_sql_query("select count(userid) from touch group by strftime( '%H', timestamp) " , db.connection)
df.plot(kind='bar')

# toutch grouped by day
df = pd.read_sql_query("select  strftime( '%m', timestamp) ,strftime( '%d', timestamp), count(distinct userid) from touch group by strftime( '%m', timestamp), strftime( '%d', timestamp) " , db.connection)


#%%
#  notification  ############################

#  notification grouped by userid
df = pd.read_sql_query("select  userid, count(nontificationid) from notification group  by userid  " , db.connection)
df.sort_values('count(nontificationid)') .plot(kind='bar', figsize=(20,10))

# notification  grouped by hour
df = pd.read_sql_query("select  count(nontificationid) from notification group  by strftime( '%H', timestamp)  " , db.connection)
df.plot(kind='bar', figsize=(20,10))

# notification grouped by minute
df = pd.read_sql_query("select  count(nontificationid) from notification group  by strftime( '%M', timestamp)  " , db.connection)
df.plot(kind='bar', figsize=(20,10))



#%%
#  application  ############################

#  application grouped by day
query_app = "select date, count(distinct application) , count(distinct userid) from app where userid in"+ str(tuple(useful_userid))+"group by date " 
df = pd.read_sql_query(query_app, db.connection).sort_values('date')
df.set_index('date')['count(distinct userid)'].plot(kind='bar', figsize=(20,10))


query_app_user = "select userid, count(distinct application) as n_apps, count(distinct date) as n_days  from app where userid in "+ str(tuple(useful_userid))+" group by userid "
df = pd.read_sql_query(query_app_user, db.connection).sort_values('userid')
userid_noapp = set(df[df['n_apps'] == 1]['userid']) # id of users without apps 

print( 'there are '+ str(len(userid_noapp))+ ' users with only one application')

#get all application of a specific user excluding ilog, launcher and  
query_app = "select userid, date, time, application from app where userid = 111"
#df = pd.read_sql_query(query_app, db.connection).sort_values('date')
df.query('application != "com.huawei.android.launcher" & application != "" & application != "it.unitn.disi.witmee.sensorlog"')
df.value_counts('application')


#%%
#  screen  ############################

query_screen = "select  date, count(distinct userid) as n_user, status from screen group by date "
df = pd.read_sql_query(query_screen , db.connection)
df.set_index('date')['n_user'].plot(kind='bar', figsize=(20,10))

# how many screen off and on 
query_screen = "select  status, count(status)from screen group by status "
df = pd.read_sql_query(query_screen , db.connection)
df

# how many screen off and on per userid
query_screen = "select  userid, sum(CASE status WHEN 'SCREEN_ON' then 1 else 0 end) as n_on, sum(CASE status WHEN 'SCREEN_ON' then 0 else 1 end) as n_off from screen group by userid "
#df = pd.read_sql_query(query_screen , db.connection)
df['diff'] =  (df['n_off'] - df['n_on'])
df


#%%
#  location  ############################

#  location grouped by day
df = pd.read_sql_query("select strftime( '%m', timestamp), strftime( '%d', timestamp), count(distinct userid)from location  group by strftime( '%m', timestamp), strftime( '%d', timestamp)  " , db.connection)
df.set_index(['strftime( \'%m\', timestamp)','strftime( \'%d\', timestamp)']).plot(kind='bar',figsize=(20,10))


# location grouped by userid
df = pd.read_sql_query("select userid, count(timestamp) from location group by userid  " , db.connection)
df.sort_values(['count(timestamp)']).plot(kind='bar', figsize=(20,10))

#count  the number of users that have less than 100 entries 
print(df[df['count(timestamp)'] < 100].count()['userid'], 'users have less than 100 entries')
print(df[df['count(timestamp)'] < 1000].count()['userid'], 'users have less than 1000 entries')
print(df[df['count(timestamp)'] < 10000].count()['userid'], 'users have less than 10000 entries')

#  mean 
print(round(df['count(timestamp)'].mean()), '-> mean number of entries per user')

# max columns 
pd.set_option('display.max_columns', 10)