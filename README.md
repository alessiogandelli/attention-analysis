# attention-analysis
social dynamics lab project

the goal of this project is to get insight on how students use their phones, the data have been collected in the context of a bigger [project](https://www.internetofus.eu/)

data have been collected in november-december 2020


# dataset 

In 2020 all the unitn students were asked to participate in this study. The sample is composed by unitn students, mainly italians, android users that accepted to participate in the study under a monetary compensation.


more information about the data collection [here](https://www.internetofus.eu/wp-content/uploads/sites/38/2021/08/2021-Datascientia-LivePeople-WeNet2020.pdf)

the data have been collected mainly in 3 ways and for each students we have a lot of data, i'll talk only about the data that i used in this project.

## questionnaires 
socio demographic data such as departement, age, sex  and psychological data: diffrent indicators but i only consider big 5 personality traits 

## iLog
The students that accepted to participate in the study were asked to download an app named iLog that has been used to collect data from sensors and to ask the students to fill a time diary every day for 29 days.

the frequence of the time diary is every 30 minutes for the first 2 weeks and every hour for the last 2 weeks

### sensors 
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


# data preparation  
Here i describe the process of data preparation, starting from the raw data, passing to the cleaning and ending with the final dataset. The demographic and the time diary were already cleaned while the sesors data wer not so i had to do it by myself.


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


# analysis 

we start looking into general statistics on how students use their phones, the most used apps and the top installed and the top notification

then i looked at an aggregated time diary to see what people do during the day and turns out that the  longest activity is sleeping 20% and on average 11% studying 

now i want to focus on what people do when they study and see if i can group in different clusters and correlate with perdonality trait or demographics 

## study 

the first thing was to look at the self reported time diary and to remove outliers, i.e. people that reported they studied 100% of the time (1 user) and 0% (4 users)

we also have to take into account the period, in fact we are between november and december and how people study is not homegenous during the semester, I expect the ones with 'preappelli' in december study more than the others that have exams in january and febraury, since we do not have this information we have to be careful in the interpretation of the results, in fact if someone attending a spefic course is studyng more than other we cannot say that that course is more difficult or require ore effort but maybe there are different deadlines, for such analysis we need more longitudinal data

said that now i want to study the use of the phone during the study time, i.e. what people do when they study: 
-  what apps they use
- how many notifications they receive
- how many touches they do, etc.

the first metric I explore is  how frequently people touch their phone when they study, it turns out that there are few people that can study without touching their phones but most of them can't stay without more than 20 minutes. 
the mean is 25 min but the median is 5, this mean that probably sometimes they do no touch the phone for a long time and this increase the average 

then it is interesting to see which application are they using, because some of them may are using the calculator but others whastapp, we'll also see if the touch of the phone is related to a notification.


### applications 
Looking at this image we can see how with the first 4 apps ( whatsapp, instagram, youtube, chrome) we cover 50% of the time, then we have a long tail of apps that are used less than 1% of the time, this is not surprising since we have 1000 apps installed and we use just a few of them. 

![top apps](/plots/top_apps.png)

Looking at the most installed apps we can see the presence of gmail, which is not a very used app but today checking mail is necessary, taking into account akso that the university mail is a google account.

![top downloaded apps](/plots/top_installed_apps.png)

### notifications
Looking at notifications the presence of whatsapp is clear, but at the second place there is telegram which is not on the top download, but it is a very popular app, especially among students, where there are big groups and so receiveing many notification is normal. 

![top notifications](/plots/top_notification_tree.png)


### what 
In this figure we can see for each hour what people do 


![what](/plots/what.png)



# results 
## study 

students reported that they study on average 3.9 hours a day eith a std of 1.6 

now we look at how much on average passes between two notifications, there are 7 students out of 120 tha do not receive notification 










