#%% 
from database_helper import Database 
import csv
import datetime
import time
import pandas as pd




data_dir = '/Volumes/boot420/Users/alessiogandelli/data_social_dynamics/'
location_file =  data_dir + 'locationeventpertime.csv'
touch_file = data_dir + 'touchevent.csv'
notification_file = data_dir + 'notificationevent.csv'
application_file =data_dir + 'applicationevent.csv'
screen_file = data_dir + 'PhoneEvents/screenevent.csv'


db_file = data_dir + 'sd.db'
db = Database(db_file)



# %%
def csv_to_db_many(csv_file, table_name, create_query, clean_row, insert_query):
    db.query("drop table if exists {}".format(table_name))

    with open(csv_file) as l:
        csv_reader = csv.reader(l, delimiter=',')
        line_count = 0
        buffer = []
        for row in csv_reader:
            if line_count == 0:
                db.execute(create_query)

            else:

                buffer.append(clean_row(row))
                                                                                    # insert data every 1000 rows
                if len(buffer) == 10000:
                    db.execute_many(insert_query, buffer)
                    buffer = []
                    db.commit()
                
                if  line_count % 1000000 == 0:
                    print(line_count, 'lines processed','time:', time.time() - start)
                  

            
            line_count += 1
        db.execute_many(insert_query, buffer)
        
        print('Processed {} lines.'.format(line_count))




#%%  socio e time diary 
df_td = pd.read_stata('/Users/alessiogandelli/Desktop/social dynamics lab/project/data/td_ita.dta')
df_socio = pd.read_stata('/Users/alessiogandelli/Desktop/social dynamics lab/project/data/sociopsicodemo ITA.dta')

df_socio['userid'] = df_socio['userid'].astype(int)

df_socio = df_socio.drop(['token', 'w1_idpilot', 'pilot' ], axis=1)
df_socio.rename(columns={'w1_A01': 'gender', 'cohort': 'age'}, inplace=True)
db.from_pandas(df_socio, 'socio')


df_td['id'] = df_td['id'].astype(int)
df_diary = df_td.filter(['id', 'date_not','first2w','week','what', 'travel_fromto', 'travel_medium', 'sport', 'where', 'withw', 'mood'])
df_diary.rename(columns={'id': 'userid','date_not': 'timestamp', 'travel_fromto': 'travel', 'where': 'where', 'withw': 'withwho'}, inplace=True)
df_diary['date'] = df_diary['timestamp'].dt.date
df_diary['time'] = df_diary['timestamp'].dt.time

# manca tutta la parte di filtraggio dei 50 utenti con maggior numero di no information cheè stato erroneamente cancellato 

db.from_pandas(df_diary, 'diary')


# %% 
# ### LOCATION #####################################################
start = time.time()

create_location_table = "CREATE TABLE location (timestamp DATETIME, date DATETIME, time text, userid INTEGER, suburb TEXT, city TEXT, region TEXT, moving INTEGER, fclass0 TEXT, code0 TEXT, name0 TEXT)"
insert_location_query = 'INSERT INTO location VALUES(?,?,?,?,?,?,?,?,?,?,?)'
clean_location_row = lambda row: [datetime.datetime.strptime(row[0], '%Y%m%d%H%M%S%f'), datetime.datetime.strptime(row[0], '%Y%m%d%H%M%S%f').date(), str(datetime.datetime.strptime(row[0], '%Y%m%d%H%M%S%f').time()), row[2], row[7], row[8], row[9], row[10], row[11], row[12], row[13]]

csv_to_db_many(location_file, 'location', create_location_table, clean_location_row , insert_location_query)
end = time.time()
print((end - start)/60)



# %%
# ### TOUCH #####################################################

start = time.time()

create_touch_table = "CREATE TABLE touch (timestamp DATETIME, date DATETIME, time TEXT, userid INTEGER)"
insert_touch_query = 'INSERT INTO touch VALUES(?,?,?,?)'
clean_touch_row = lambda row: [datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f'), datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f').date(), str(datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f').time()), row[1]]

csv_to_db_many(touch_file, 'touch', create_touch_table, clean_touch_row , insert_touch_query)
end = time.time()
print((end - start)/60)



# %% 
##### APPLICATION #####################################################
 
start = time.time()

create_application_table = "CREATE TABLE application (timestamp DATETIME, date DATETIME, time TEXT, userid INTEGER, application TEXT)"
insert_application_query = 'INSERT INTO application VALUES(?,?,?,?,?)'
clean_application_row = lambda row: [datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f'), datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f').date(), str(datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f').time()), row[1], row[4]]

csv_to_db_many(application_file, 'application', create_application_table, clean_application_row , insert_application_query)
end = time.time()
print((end - start)/60)



# %% 
# ### NOTIFICATION #####################################################


start = time.time()


create_notification_table = "CREATE TABLE notification (timestamp DATETIME, date DATETIME, time TEXT, userid INTEGER, nontificationid INTEGER, source TEXT, isclearable INTEGER, isongoing INTEGER, status TEXT )"
insert_notification_query = 'INSERT INTO notification VALUES(?,?,?,?,?,?,?,?,?)'
clean_notification_row = lambda row: [datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f'), datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f').date(), str(datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f').time()), row[1], row[4], row[7], row[5], row[6], row[8]]

csv_to_db_many(notification_file, 'notification', create_notification_table, clean_notification_row , insert_notification_query)

end = time.time()
print((end - start)/60)
# %%
###### SCREEN #####################################################
start = time.time()


create_screen_table = "CREATE TABLE screen (timestamp DATETIME, date DATETIME, time TEXT, userid INTEGER, status TEXT)"
insert_screen_query = 'INSERT INTO screen VALUES(?,?,?,?,?)'
clean_screen_row = lambda row: [datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f'), datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f').date(), str(datetime.datetime.strptime(row[3], '%Y%m%d%H%M%S%f').time()), row[1], row[4]]

csv_to_db_many(screen_file, 'screen', create_screen_table, clean_screen_row , insert_screen_query)

end = time.time()
print((end - start)/60)
# %%

##### yardstick #####################################################
df1 = pd.DataFrame()
import datetime

start = datetime.datetime(2020, 11, 13, 5)
end = datetime.datetime(2020, 12, 12, 6)
ids = pd.DataFrame(range(0,266))
ids.columns = ['userid']

df1['timestamp']= pd.date_range(start, end, freq='1min')
df1['year'] = df1['timestamp'].dt.year
df1['month'] = df1['timestamp'].dt.month
df1['day'] = df1['timestamp'].dt.day
df1['hour'] = df1['timestamp'].dt.hour
df1['minute'] = df1['timestamp'].dt.minute
df1.drop('timestamp', axis=1, inplace=True)

df1.merge(ids, how='cross')

