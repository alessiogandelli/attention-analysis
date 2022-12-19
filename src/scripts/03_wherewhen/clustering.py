#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import json
import seaborn as sns
from scipy import stats 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
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

#%%



#touches = 0 to nan 
df['touches'] = df['touches'].replace(0, np.nan)

users_df = df.groupby(['userid'])[['touches', 'notification']].count()
users_df = users_df.merge(df[['userid','age','gender', 'department', 'degree']].drop_duplicates(), on='userid')
users_df = users_df[['age','gender','department', 'degree', 'touches', 'notification']]




#%%
# Normalize the features
X = StandardScaler().fit_transform(users_df)

# Create the KMeans model
kmeans = KMeans(n_clusters=4)

# Fit the model to the data
kmeans.fit(X)

# Add the predicted cluster labels to the dataframe
df['cluster'] = kmeans.predict(X)

Sum_of_squared_distances = []
K = range(1,10)
for num_clusters in K :
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X)
    Sum_of_squared_distances.append(kmeans.inertia_)

# Plot the elbow curve
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()





# %%https://towardsdatascience.com/clustering-on-numerical-and-categorical-features-6e0ebcf1cbad
import gower 
# cast gender department and degree to string 
users_df['gender'] = users_df['gender'].astype(str)
users_df['department'] = users_df['department'].astype(str)
users_df['degree'] = users_df['degree'].astype(str)

distance_matrix = gower.gower_matrix(users_df)

# %%

from sklearn import preprocessing
users_norm = users_df.copy()
scaler = preprocessing.MinMaxScaler()
users_norm[['age','touches', 'notification']] = scaler.fit_transform(users_norm[['age','touches', 'notification']])



# https://medium.com/analytics-vidhya/clustering-on-mixed-data-types-in-python-7c22b3898086
from kmodes.kprototypes import KPrototypes
kproto = KPrototypes(n_clusters=4, init='Cao', verbose=2)
clusters = kproto.fit_predict(users_norm, categorical=[1,2,3])


labels = pd.DataFrame(clusters)
labeledCustomers = pd.concat((users_df,labels),axis=1)
labeledCustomers = labeledCustomers.rename({0:'labels'},axis=1)

# swarn plot to see the distribution of the clusters
sns.swarmplot(x='labels', y='age', data=labeledCustomers)
sns.swarmplot(x='labels', y='degree', data=labeledCustomers)

plt.show()


#%% kmeans 

users_df = df.groupby(['userid'])[['touches', 'notification']].count()
users_df = users_df.merge(df[['userid','age', 'Extraversion',
       'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness']].drop_duplicates(), on='userid')
users_df = users_df[['age', 'Extraversion',
       'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness']]

# fillna with avg
users_df = users_df.fillna(users_df.mean())
# %%

# Normalize the features
X = StandardScaler().fit_transform(users_df)



Sum_of_squared_distances = []
K = range(1,10)
for num_clusters in K :
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X)
    Sum_of_squared_distances.append(kmeans.inertia_)

# Plot the elbow curve
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()
# %%
