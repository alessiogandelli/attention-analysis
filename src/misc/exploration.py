#%%
import pandas as pd

df_td = pd.read_stata('/Users/alessiogandelli/Desktop/social dynamics lab/project/data/td_ita.dta')
df_socio = pd.read_stata('/Users/alessiogandelli/Desktop/social dynamics lab/project/data/sociopsicodemo ITA.dta')

# %%


df_td['id'] = df_td['id'].astype(int)
df_socio['userid'] = df_socio['userid'].astype(int)
# %%
students = {}
for i, s in df_socio.iterrows():

    student = {}
    student['id'] = s['userid']
    student['uni'] = s['pilot']
    student['gender'] = s['w1_A01']
    student['department'] = s['department']
    student['age'] = s['cohort']
    student['degree'] = s['degree']
    student['extraversion'] = s['Extraversion']
    student['agreeableness'] = s['Agreeableness']
    student['conscientiousness'] = s['Conscientiousness']
    student['neuroticism'] = s['Neuroticism']
    student['openess'] = s['Openness']

    student['time_diary'] = []

    df = df_td[df_td['id'] == s['userid']]

    for j, td in df.iterrows():
        diary = {}
        diary['date'] = td['date_not'].date()
        diary['time'] = td['date_not'].time()
        diary['first2weeks'] = td['first2w']
        diary['weekday'] = td['week']
        diary['travel_medium'] = td['travel_medium']
        diary['what'] = td['what']
        diary['where'] = td['where2']
        diary['withw2'] = td['withw2']
        diary['mood'] = td['mood']
      
        student['time_diary'].append(diary)



    students[s['userid']] = student
    
# %%










from database_helper import Database 

db = Database('/Users/alessiogandelli/data_social_dynamics/social_dynamics.sqlite')

all_userid = list(range(0,265))

#%%

loc_userid = db.query("select distinct userid from location")
loc_userid = [i[0] for i in loc_userid]
loc_missing = set(all_userid) - set(loc_userid)

# %%
not_userid = db.query("select distinct userid from notification")
not_userid = [i[0] for i in not_userid]
not_missing = set(all_userid) - set(not_userid)
# %%

app_userid = db.query("select distinct userid from application")
app_userid = [i[0] for i in app_userid]
app_missing = set(all_userid) - set(app_userid)

# %%
touch_userid = db.query("select distinct userid from application")
touch_userid = [i[0] for i in touch_userid]
touch_missing = set(all_userid) - set(touch_userid)
# %%
all_missing = loc_missing.intersection(not_missing).intersection(app_missing).intersection(touch_missing)
loc_missing.union(touch_missing).union(not_missing).union(app_missing)