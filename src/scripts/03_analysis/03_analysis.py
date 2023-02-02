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
# cast tuple index to datatime
data_folder = '/Users/alessiogandelli/dev/uni/attention-analysis/data/'
plot_folder = '/Users/alessiogandelli/dev/uni/attention-analysis/plots/'
#%%

''' LOAD DATA '''
#df.to_pickle(data_folder + 'study_analysis.pkl')

df = pd.read_pickle(data_folder + 'study_analysis.pkl')



''' APPLICATION'''
# %%

# most used apps 
top_apps  = df['apps'].value_counts()

top_apps.head(10).plot(kind = 'barh', figsize = (5, 3), title = 'Most used apps', colormap = 'tab20')
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(sum(top_apps)))
plt.xlabel('share of usage (%)')

# save plot
plt.savefig(plot_folder + 'top_apps.png', dpi=300, bbox_inches='tight')

# %%
# how many users have installed each app
n_users = df['userid'].nunique()
user_installed_apps = df.groupby('apps')['userid'].nunique().sort_values(ascending=False).head(10)
user_installed_apps.plot(kind = 'bar', figsize = (5, 5), title = 'Most installed apps', colormap = 'tab20')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(n_users))
# rotate x labels
plt.xticks(rotation=30)

# save plot
plt.savefig(plot_folder + 'top_installed_apps.png', dpi=300, bbox_inches='tight')

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

# save plot
plt.savefig(plot_folder + 'top_notification.png', dpi=300, bbox_inches='tight')

#%%
#tree map with top_notif 
import squarify

# drop rows the one that contains the word system
top_notif = top_notif[~top_notif.index.str.contains('system')]
top_notif = top_notif[~top_notif.index.str.contains('vodafone')]
top_notif = top_notif[~top_notif.index.str.contains('cc.pacer')]
  



plt.figure(figsize=(9, 9))
squarify.plot(sizes=top_notif.head(10), label=top_notif.head(10).index, alpha=.7, color = sns.color_palette("tab20", 10), text_kwargs={'fontsize':14})
plt.axis('off')

# save plot
plt.savefig(plot_folder + 'top_notification_tree.png', dpi=300, bbox_inches='tight')

#df= df[~df['notification'].str.contains('system')]

# group by user and count application per day


#%%




#%%

#average numer or notification per app per hour per user 




'''WHAT'''

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

#using hours as x axis and all the activities as y axis

ax = df_what.plot(kind='area', stacked=True, figsize=(10, 6), colormap = 'tab20', title = 'What people do at different hours of the day')

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
#x ticks frequency 5 to 24 and 24 to 4 
#plt.xticks(np.arange(0, 24, 2))

# put legend outside the plot wit a bigger size 
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 15})



# save plot
plt.savefig(plot_folder + 'what.png', dpi=300, bbox_inches='tight')




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