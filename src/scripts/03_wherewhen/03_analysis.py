#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import json
import seaborn as sns
from scipy import stats 
# cast tuple index to datatime
#%%
with open('/Users/alessiogandelli/dev/uni/attention-analysis/data/userids.json') as f:
        userids = json.load(f)

userid_ww = set(userids['userid_ww'])
userid_ext =  set(userids['userid_ext'])
userid_app = set(userids['userid_app'])

complete = userid_ww & userid_ext & userid_app



types = {'what': 'category', 'apps': 'category', 'age' : 'int64', 'gender' : 'category', 'nationality' : 'category' , 
        'department': 'category', 'degree' : 'category', 'notification': 'category', 'what' : 'category', 'apps' : 'category', }

df = pd.read_csv('/Users/alessiogandelli/dev/uni/attention-analysis/src/scripts/03_wherewhen/merged_data.csv', 
                dtype= types, parse_dates=['day'])

# reorder columns
df = df[['userid', 'day', 'hour', 'min', 'what', 'touches', 'apps', 'notification', 'age',
       'gender', 'department', 'degree', 'Extraversion', 'Agreeableness',
       'Conscientiousness', 'Neuroticism', 'Openness']]

# get only userid in complete 
df = df[df['userid'].isin(complete)]



no_diary = df[df['what'] == 'Missing'].groupby('userid')['what'].count().sort_values(ascending=False).head(20).index.tolist()

#drop no_diary users
df = df[~df['userid'].isin(no_diary)]



''' APPLICATION'''
# %%

# most used apps 
top_apps  = df['apps'].value_counts()
top_apps.head(10).plot(kind = 'barh', figsize = (10, 5), title = 'Most used apps', colormap = 'tab20')
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(sum(top_apps)))
plt.xlabel('share of usage (%)')

# %%
# how many users have installed each app
n_users = df['userid'].nunique()
user_installed_apps = df.groupby('apps')['userid'].nunique().sort_values(ascending=False).head(10)
user_installed_apps.plot(kind = 'bar', figsize = (5, 5), title = 'Most installed apps', colormap = 'tab20')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(n_users))
# rotate x labels
plt.xticks(rotation=30)


'''NOTIFICATION'''
#%% 

# distribution of notification per user
df_notif_user = df.groupby(['userid','day'])['notification'].count().groupby('userid').mean()
plt.xlabel('average notifications per day')
plt.ylabel('density')
ax = sns.kdeplot(df_notif_user, fill=True, color="g")

# most frequent notification
top_notif = df['notification'].value_counts()
top_notif.head(10).plot(kind = 'barh', figsize = (7, 5), title = 'Most frequent notification', colormap = 'tab20')
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(sum(top_notif)))
plt.xlabel('share of notification (%)')
plt.ylabel('source')

#%%
#tree map with top_notif 
import squarify

# drop rows the one that contains the word system
top_notif = top_notif[~top_notif.index.str.contains('system')]
top_notif = top_notif[~top_notif.index.str.contains('vodafone')]
top_notif = top_notif[~top_notif.index.str.contains('cc.pacer')]
  



plt.figure(figsize=(10, 10))
squarify.plot(sizes=top_notif.head(10), label=top_notif.head(10).index, alpha=.7, color = sns.color_palette("tab20", 10), text_kwargs={'fontsize':14})
plt.axis('off')
plt.show()

df= df[~df['notification'].str.contains('system')]

# group by user and count application per day





#%%

#average numer or notification per app per hour per user 




'''WHAT'''
#%%

# for each hour get the 3 what with highest count value
what_hour = df.groupby(['what', 'hour'])['userid'].count()

# move first 5  hours to the end

# conder only first 2 weeks 
df = df[df['day'] < '2019-10-15']



#plot sleeping 
ax = what_hour.loc['Sleeping'].plot(kind = 'line', figsize = (10, 5), title = 'Sleeping', color = 'g')
what_hour.loc['Food-related'].plot(kind = 'line', figsize = (10, 5), title = 'Food-related', color = 'r', ax = ax)
what_hour.loc['Entertainment'].plot(kind = 'line', figsize = (10, 5), title = 'Entertainment', color = 'b', ax = ax)
what_hour.loc['Study/workgroup'].plot(kind = 'line', figsize = (10, 5), title = 'Study/workgroup', color = 'y', ax = ax)
what_hour.loc['Missing'].plot(kind = 'line', figsize = (10, 5), title = 'Missing', color = 'k', ax = ax)

#legend
ax.legend(['Sleeping', 'Food-related', 'Entertainment', 'Study/workgroup', 'Missing'])

#title
ax.set_title('What people do at different hours of the day')

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(sum(what_hour)/24))

#x ticks frequency
plt.xticks(np.arange(6, 24, 2))
#%%
# stacked area chart with seaborn 



df_what = df.groupby(['what', 'hour'])['userid'].count().reset_index()
df_what = df_what.pivot(index='hour', columns='what', values='userid')
df_what = df_what.fillna(0)
df_what['total'] = df_what.sum(axis=1)
df_what = df_what.divide(df_what['total'], axis=0).drop('total', axis=1)

# reodrder columns
df_what = df_what[[ 'Missing', 'Sleeping','Entertainment', 'Work/Class',  'Study/workgroup','Food-related','Break_coffee', 'Householdcare/Shopping',
       'Inchat/e-mail/seekingInternet',
       'Personalcare', 'Phone/Videocalling', 'Social media',
       'Sociallife/Happy Hour',  'Moving',
       'Others']]

#move first 5 rows to the end
#df_what = df_what.iloc[5:].append(df_what.iloc[:5])



ax = df_what.plot( kind='area', stacked=True, figsize=(20, 10), colormap = 'tab20', title = 'What people do at different hours of the day')

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
#x ticks frequency
plt.xticks(np.arange(0, 24, 2))

# put legend outside the plot wit a bigger size 
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 15})


plt.show()




#%%
df_study = df[df['what'] == 'Study/workgroup']
#violin plot 
ax = sns.violinplot(x="hour", y="department", data=df_study, palette="muted", inner = 'quartile', scale = 'width', cut = 0)






#cluster users 
















#latent profile analysis

#%%
gp = df.groupby(['what','apps'])['touches'].count()
gp = gp.reset_index().sort_values(['what','touches'], ascending = False)

# drop rows where app is launcher 


# get top three for each what
gp = gp.groupby('what').head(3)
# %% most used apps by students 
gp = df.groupby(['apps'])['touches'].count()



# apps the user uses the most 
df.groupby(['userid','apps']).count().sort_values(['userid','touches'], ascending=False).groupby('userid').head(3)

# average minutes per day people use instagram 
df[df['apps'] == 'com.instagram.android'].groupby(['userid','day']).count().groupby('userid').mean()
# %%
# daily average minutes per app
df.groupby(['userid','apps','day']).count().groupby(['userid','apps']).mean().sort_values('touches', ascending=False).groupby('apps').head(3)


# %%