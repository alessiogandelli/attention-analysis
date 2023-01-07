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
# %%# get only 30 november data 
sig128 = df[df['userid'] == 128]
sig128_study = sig128[sig128['what'] == 'Study/workgroup']
sig128_study = sig128_study[sig128_study['day'] == '2020-11-30']


# this but for every user  


    

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
