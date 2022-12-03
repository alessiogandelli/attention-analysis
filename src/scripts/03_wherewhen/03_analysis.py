#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
# cast tuple index to datatime

types = {'what': 'str', 'apps': 'str', 'age' : 'int64', 'gender' : 'str', 'nationality' : 'str' , 
        'department': 'str', 'degree' : 'str', 'notification': 'str', 'what' : 'str', 'apps' : 'str', }

df = pd.read_csv('/Users/alessiogandelli/dev/uni/attention-analysis/src/scripts/03_wherewhen/merged_data.csv', 
                dtype= types, parse_dates=['day'])

# reorder columns
df = df[['userid', 'day', 'hour', 'min', 'what', 'touches', 'apps', 'notification', 'age',
       'gender', 'nationality', 'department', 'degree', 'Extraversion', 'Agreeableness',
       'Conscientiousness', 'Neuroticism', 'Openness']]


# %%
''' most used apps '''




top_apps  = df['apps'].value_counts()
top_apps.head(10).plot(kind = 'bar', figsize = (20, 10), title = 'Most used apps', colormap = 'tab20')
#plt.xticks(rotation = 45)

# remove com. from the label 

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(sum(top_apps)))
# rotation of x axis labels

#%%
df.groupby(['hour', 'min', 'what']).count().plot(kind = 'area')




#%%
# groupby df by what and get  the  top 3 apps 
df.groupby(['what', 'apps']).count()['touches']




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
