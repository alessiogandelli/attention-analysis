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

types = {'what': 'category', 'apps': 'category', 'age' : 'int64', 'gender' : 'category', 'nationality' : 'category' , 'department': 'category', 'degree' : 'category', 'notification': 'category', 'what' : 'category', 'apps' : 'category', }
df = pd.read_csv(data_folder + 'merged_data.csv', dtype= types, parse_dates=['day'])

# reorder columns
df = df[['userid', 'day', 'hour', 'min', 'what', 'touches', 'apps', 'notification', 'age',
       'gender', 'department', 'degree', 'Extraversion', 'Agreeableness',
       'Conscientiousness', 'Neuroticism', 'Openness']]



# %%
# daily share of activities, globally users study 11% of their time
# and 5.5 percent they are at at clas 

df['what'].value_counts()/ sum(df['what'].value_counts())



#%%
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
df['what'].value_counts()


df = df[df['what'] == 'Study/workgroup']



# drop user 232
# %%
sig128 = df[df['userid'] == 1]

sig128_study = sig128[sig128['what'] == 'Study/workgroup']

# get only 30 november data 
sig128_study = sig128_study[sig128_study['day'] == '2020-11-30']

nophone = []
count = 0
# filter on the column apps the value that are not a category 
for touches in sig128_study['touches']:
    if touches == 0:
        count += 1
    elif count > 0 :
        nophone.append(count)
        count = 0

mean_nophone = np.mean(nophone)
mean_nophone
# this but for every user  

#%%
df_study = df[df['what'] == 'Study/workgroup'].head(10000)

students = {}
studentid = 0
nophone = []
count = 0

for i, row in df_study.iterrows():

    print(row['userid'], row['hour'], row['min'], count, touches)
    # process student 
    if row['userid'] != studentid:
        print('processing student: ', studentid, row['hour'], row['min'])
        students[studentid] = np.mean(nophone)
        nophone = []
        count = 0
        studentid = row['userid']


    if row['touches'] == 0:
        count += 1
    elif count > 0 :
        nophone.append(count)
        count = 0
    
# %%

count = 0

for i, row in df_study.iterrows():


    if row['touches'] == 0:
        count += 1
    elif count > 0 :
        nophone.append(count)
        count = 0

    df_study.loc[i, 'nophone'] = count


df_study[df_study['userid'] == 1]['nophone'].mean()

# from nophone column everytime there is 0 take the previous value and add to a list 
# then take the mean of the list

df_study


#%%

# most used apps while studying
apps = sig128_study.groupby('apps')['userid'].count().sort_values(ascending=False)

# plot his day 

# %%
sig128_study.groupby('day')['what'].count().plot(kind='bar')
# %%
# stacked area chart of what he does during the day
# %%
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
    average = np.mean(nophone)
    median = np.median(nophone)
    std = np.std(nophone)
    # store the result in the dictionary
    students[studentid] = {'average': average, 'median': median, 'std': std}
    print('mean: ', average, 'median: ', median, 'std: ', std)


# %%
