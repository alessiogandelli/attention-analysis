#%%
from database_helper import Database
import pandas as pd
import datetime
from venn import venn
import matplotlib.pyplot as plt
db = Database('/Users/alessiogandelli/data_social_dynamics/social_dynamics.sqlite')
import json

#read userid from json file
with open('/Users/alessiogandelli/Desktop/attention-analysis/data/userids.json') as f:
    userids = json.load(f)['userid_ww']

# %%

query = "select userid, date, time, timestamp ,what, where2, withwho from diary where userid in {} ".format(tuple(userids))

df = pd.read_sql(query, db.connection)

df.value_counts('what')
# change 



# %%
df = df[df['date'] == '2020-11-20'].groupby(['timestamp', 'what']).size().unstack(fill_value = 0)

# %%
df.plot(kind = 'area', stacked = True, figsize = (20, 10), title = 'Diary events per minute')
# %%
# %%

# %%
df.index = pd.to_datetime(df.index)
df.plot(kind = 'area', stacked = True, figsize = (20, 10), title = 'Diary events per minute').legend(loc='center left',bbox_to_anchor=(1.0, 0.5));
plt.xticks(rotation = 90)
#add one tick per hour 
#plt.xticks(ticks = df.index[::60], labels = df.index[::60])


# %% from geopandas to cr


