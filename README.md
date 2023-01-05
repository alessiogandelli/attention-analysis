# attention-analysis
social dynamics lab project

the goal of this project is to get insight on how students use their phones, the data have been collected in the context of a bigger [project](https://www.internetofus.eu/)

data have been collected in november-december 2020


# dataset 

https://www.internetofus.eu/wp-content/uploads/sites/38/2021/08/2021-Datascientia-LivePeople-WeNet2020.pdf

the data have been collected mainly in 3 ways 
## questionnaires 
socio demographic data and big 5 personality traits 

## time diary 
a notification on their phone asked what they are doing every half an hour for the first 2 weeks and every hour for the last two weeks 

##  phone sensors 
many sensor recorded the data but i was interested only in few of them:

- application: the application that is in foreground
- touch: every touch on the screen is recorded 
- notification: every notification received  




## schema  
after converting the csv data into a sqlite 

```
CREATE TABLE application (timestamp DATETIME, date DATETIME, time TEXT, userid INTEGER, application TEXT);

CREATE TABLE touch (timestamp DATETIME, date DATETIME, time TEXT, userid INTEGER);

CREATE TABLE location (timestamp DATETIME, date DATETIME, time text, userid INTEGER, suburb TEXT, 
city TEXT, region TEXT, moving INTEGER, fclass0 TEXT, code0 TEXT, name0 TEXT);

CREATE TABLE notification (timestamp DATETIME, date DATETIME, time TEXT, userid INTEGER, nontificationid INTEGER, source TEXT, isclearable INTEGER, isongoing INTEGER, status TEXT );

CREATE TABLE IF NOT EXISTS "socio" (
"userid" INTEGER,
  "gender" TEXT,
  "nationality" TEXT,
  "department" TEXT,
  "age" TEXT,
  "degree" TEXT,
  "Extraversion" REAL,
  "Agreeableness" REAL,
  "Conscientiousness" REAL,
  "Neuroticism" REAL,
  "Openness" REAL,
);
CREATE TABLE IF NOT EXISTS "diary" (
"userid" INTEGER,
  "timestamp" TIMESTAMP,
  "first2w" TEXT,
  "week" TEXT,
  "what" TEXT,
  "travel" TEXT,
  "travel_medium" TEXT,
  "sport" TEXT,
  "where" TEXT,
  "withwho" TEXT,
  "mood" TEXT,
  "date" DATE,
  "time" TIME
);

```


# workflow 

## data import to sqlite
The data from sensor arrived in a big csv file that needed to be cleaned, but since the size is around some GB the first thing i have done was to import all the data in a SQLite database in order to have a common structure and to have the ability to query only the needed data without having all the data in RAM.

## cleaning

### app names 
the app names both in application ans notification were the android packahe name that needed to be converted into a more readable name, the heuristic i used were to remove all the occurence of string like  com, it, org, google, samsung, huawei, etc. and to keep only the last part of the string, for example com.google.android.youtube -> youtube

### age field 
in the sociodemographic the age field was a cohort of age, i converted it into a number

### time diary
There were more than 30 possible values for the what field, i grouped them into 5 categories:
- sleeping 
- food related 
- entertainment
- work/class 
- other
- missing

### users selection 

there were 252 users in the dataset, but only 169 of them shared all the data, i decided to work only with these 161 users, to achieve this I used some set operation on the different users id for each

this was not enough, in fact due to some problems there were users that showd no data for some sensor or just few, especially in the time diary there were a consistent group of people that answered just few times, i decided to discard these users, the final number of users is
i dropped the first 20 users with no diary 

141 users and 14% of missing time diary 

## yardstick 
the next step was to aggregate the data in order to have a more compact representation of the data. in fact for some sensors we have many entries per second and this granurality was not needed. the new dataset have one entry per second per user, so i can have all the data in a 8 million lines csv file.

```





















#  i can do some queries to check data integrity 

There are a total of 252 unique users 

number of users for each dataset: 
```
questionnaries -> 249 users 
time-diary     -> 241 
application    -> 234 users 54 million rows
screen         -> 234 users 13 mln rows
location       -> 221 users 1.9 mln rows
touch          -> 201 users 130 mln rows 
notification   -> 183 users 6.7 mln rows
```


There are 169 users that shared all the data 
There are 18 users missing all the sensors 

after discarding this 18 users there is 1 user missing time diary and 2 missing questionnaires 

After filtering these users

There are 231 users with socio, td , application and screen 

62 users miss data from at least one sensor 
13 miss location data 
33 miss touch data 
49 miss location data 


## time diary 
there are 1114 entries for each users in 29 days from 13-11-20 to 11-12-20 
850 for the first 2 weeks
264 from the second 2 weeks

## touch

## application 
attention, there are 34 students that are in the dataset by actually there is no data about the application 

the data is not consistent among the days, excluding the outliers, the numebr of users  is changing every day with a decresing trend

13th of november there are 221 useful id
11th of december there are 145 useful id 

142 user have application data everyday 






