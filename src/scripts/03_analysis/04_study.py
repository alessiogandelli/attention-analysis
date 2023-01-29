#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import json
import seaborn as sns
from scipy import stats 
# cast tuple index to datatime
data_folder = '/Users/alessiogandelli/dev/uni/attention-analysis/data/'
plot_folder = '/Users/alessiogandelli/dev/uni/attention-analysis/plots/'
#%%

''' LOAD DATA '''
#df.to_pickle(data_folder + 'study_analysis.pkl')

df = pd.read_pickle(data_folder + 'study_analysis.pkl')


# %%
# daily share of activities, globally users study 11% of their time
# and 5.5 percent they are at at clas 
df['what'].value_counts()/ sum(df['what'].value_counts())



#%%
''' STUDY SHARE ''' 
# % of time students study, remove people who study 100% or 0% of the time

# group by user and get global share of study/workgroup
user_share = df.groupby('userid')['what'].value_counts()/df.groupby('userid')['what'].count()

# put the what on the columns abd user on the index
user_share = user_share.unstack()
# select only study/workgroup and work/class
user_share = user_share[['Study/workgroup', 'Work/Class']]
user_share['total'] = user_share['Study/workgroup'] + user_share['Work/Class']

# remove people with 100% and 0% study time
user_share = user_share[(user_share['total'] != 0) & (user_share['total'] != 1)]
df = df[df['userid'].isin(user_share.index)]
#%%
'''GET ONLY STUDY TIME'''

df['what'].value_counts()
df = df[df['what'] == 'Study/workgroup']


#%%
'''ONE STUDENT'''
# user 128 on date 2020-11-30



sig128 = df[df['userid'] == 128]
sig128 = sig128[sig128['day'] == '2020-11-30']

# make 0 nan 
sig128['touches'] = sig128['touches'].replace(0, np.nan)

sig128.count()

# sig 128 on day studied n minutes 
study_time = sig128.count()['min']
notification = sig128.count()['notification']
touches = sig128.count()['touches']
touches_and_notific = sig128[sig128['touches'] >0].count()['notification']
most_used_app = sig128['apps'].value_counts().index[0]
most_used_app_time = sig128['apps'].value_counts()[0]
most_used_app2 = sig128['apps'].value_counts().index[1]
most_used_app_time2 = sig128['apps'].value_counts()[1]
most_used_app3 = sig128['apps'].value_counts().index[2]
most_used_app_time3 = sig128['apps'].value_counts()[2]

most_notific = sig128['notification'].value_counts().index[0]
most_notific_time = sig128['notification'].value_counts()[0]
most_notific2 = sig128['notification'].value_counts().index[1]
most_notific_time2 = sig128['notification'].value_counts()[1]
most_notific3 = sig128['notification'].value_counts().index[2]
most_notific_time3 = sig128['notification'].value_counts()[2]

# this as a dataframe row 
df_students = pd.DataFrame({'userid': 128, 'study_time': study_time, 'notification': notification, 'touches': touches, 'touches_and_notific': touches_and_notific, 'most_used_app': most_used_app, 'most_used_app_time': most_used_app_time, 'most_used_app2': most_used_app2, 'most_used_app_time2': most_used_app_time2, 'most_used_app3': most_used_app3, 'most_used_app_time3': most_used_app_time3, 'most_notific': most_notific, 'most_notific_time': most_notific_time, 'most_notific2': most_notific2, 'most_notific_time2': most_notific_time2, 'most_notific3': most_notific3}, index=[0])

# this but for all students 
df_students = pd.DataFrame(columns=['userid', 'study_time', 'notification', 'touches', 'touches_and_notific', 'most_used_app', 'most_used_app_time', 'most_used_app2', 'most_used_app_time2', 'most_used_app3', 'most_used_app_time3', 'most_notific', 'most_notific_time', 'most_notific2', 'most_notific_time2', 'most_notific3'])
df_students = df.set_index('userid')
df_students = df.groupby(['userid', 'day']).apply(lambda x: pd.Series({'study_time': x.count()['min'], 'notification': x.count()['notification'], 'touches': x.count()['touches'], 'touches_and_notific': x[x['touches'] >0].count()['notification'], 'most_used_app': x['apps'].value_counts().index[0], 'most_used_app_time': x['apps'].value_counts()[0], 'most_used_app2': x['apps'].value_counts().index[1], 'most_used_app_time2': x['apps'].value_counts()[1], 'most_used_app3': x['apps'].value_counts().index[2], 'most_used_app_time3': x['apps'].value_counts()[2], 'most_notific': x['notification'].value_counts().index[0], 'most_notific_time': x['notification'].value_counts()[0], 'most_notific2': x['notification'].value_counts().index[1], 'most_notific_time2': x['notification'].value_counts()[1], 'most_notific3': x['notification'].value_counts().index[2]}))

## in df_students we have for each studet for each day some statistics about the study that day 

# average study time

#%%
'''PHONE TOUCH FREQUENCY'''
# in the following part of code  i compute the average numebr of minute 
# students do not touch the phone when they claim thay are studying


# from df_study compute the average lenght of streak of 0 in the touches column for each user 
df_grouped = df.groupby('userid')
students = {}

# iterate through each group
for studentid, group in df_grouped:
    # initialize the counter
    print('computing student ',studentid)
    count = 0
    # initialize the list to store the counter values
    nophone = []
    # iterate through each row in the group
    for i, row in group.iterrows():
        # if touches is 0, increment the counter
        if row['touches'] == 0:
            count += 1
        elif count > 0 :
            nophone.append(count)
            count = 0
    # calculate the mean of the counter values
    try: 
        average = np.mean(nophone)
        median = np.median(nophone)
        std = np.std(nophone)
        max_streak = np.max(nophone)
    except:
        average = 0
        median = 0
        std = 0
        max_streak = 0
    # store the result in the dictionary


    students[studentid] = {'average': average, 'median': median, 'std': std, 'max_streak': max_streak, 'nophone': nophone}
    print('mean: ', average, 'median: ', median, 'std: ', std, 'max_streak: ', max_streak)


## add to user share 
stats_phone = pd.DataFrame.from_dict(students, orient='index')
user_share = user_share.join(stats_phone)
rename = {'Study/workgroup': 'study', 'Work/Class': 'class', 
            'average': 'average_no_phone', 'median': 'median_no_phone', 'std': 'std_no_phone'}
user_share = user_share.rename(columns=rename)
#save csv 
user_share.to_csv(data_folder + 'study_stats.csv')
# %%
# read csv 
user_share = pd.read_csv(data_folder + 'study_stats.csv', index_col=0)

#remove nan 
user_share = user_share.dropna()
# drop user 112 and 86 
user_share = user_share.drop([112, 86])

# %%

all_nophone = [item for sublist in students.values() for item in sublist['nophone']]
# get only data < 60
some_nophone = [x for x in all_nophone if x < 60]

plt.figure(figsize=(10, 5))
plt.hist(some_nophone, bins=60)
plt.title('Distribution of the number of minutes without phone')
plt.xlabel('minutes')
plt.ylabel('frequency')
plt.savefig(plot_folder + 'no_touches_streak_lt60.png')



# %%
all_nophone = [item for sublist in students.values() for item in sublist['nophone']]

# plot with log on x 
plt.figure(figsize=(10, 5))
plt.hist(all_nophone, bins=60, log=True)
plt.title('Distribution of the number of minutes without phone for student 1')
plt.xlabel('minutes')
plt.ylabel('frequency')
plt.savefig(plot_folder + 'plots/no_touches_streak_log.png')

# %%
# get all phone quantities





'''RESULTS'''

# general stats about stufyng 

user_mean = df.groupby(['userid', 'day']).count().reset_index().groupby(['userid']).mean()

(user_mean['hour']/60).describe()

# histogram of study time
plt.figure(figsize=(10, 5))
plt.hist((user_mean['hour']/60), bins=10)
plt.title('Distribution of the number of minutes spent studying')
plt.xlabel('hours')
plt.ylabel('frequency')
plt.savefig(plot_folder + 'hist_study.png')

# %%
user_mean['min/not'] = user_mean['hour'] / user_mean['notification']
# remove inf 
user_mean = user_mean.replace([np.inf, -np.inf], np.nan)
user_mean = user_mean.dropna()
# histogram of time between notifications
plt.figure(figsize=(10, 5))
plt.hist(user_mean['min/not'], bins=100)
plt.title('Distribution of the number of minutes between notifications')
plt.xlabel('minutes')
plt.ylabel('frequency')
plt.savefig(plot_folder + 'hist_notific.png')


user_mean['min/not'].describe()
# mean 24 but  median is 6, this means that for half of the students 
# the time between notifications is less than 6 minutes

#get percentile of people that study more than 45 min 

#%%
# there is a big long tail so we have to focus onthe 90th percentile 
threshold = user_mean['min/not'].quantile(0.9)
# this value is 50 this means that 90% of the students receive at leat a noti
# every 50 minutes
# find all students withoin 90th percentile

notification_90 = user_mean[user_mean['min/not'] < threshold]['min/not']

# histogram of time between notifications
plt.figure(figsize=(10, 5))
plt.hist(notification_90, bins=50)
plt.title('Distribution of the number of minutes between notifications')
plt.xlabel('minutes')
plt.ylabel('frequency')
plt.savefig(plot_folder + 'hist_notific_90.png')




# %%
