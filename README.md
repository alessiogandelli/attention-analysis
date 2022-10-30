# attention-analysis
social dynamics lab project


data have been collected in november-december 2020

# storing the data 
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
  "MExtraversion" REAL,
  "MAgreeableness" REAL,
  "MConscientiousness" REAL,
  "MNeuroticism" REAL,
  "MOpenness" REAL,
  "Pconformity" REAL,
  "Ptradition" REAL,
  "Pbenov" REAL,
  "Punivers" REAL,
  "Pself" REAL,
  "Pstim" REAL,
  "Phedon" REAL,
  "Pachieve" REAL,
  "Ppower" REAL,
  "Psecurity" REAL,
  "Popen" REAL,
  "Pselfenh" REAL,
  "Pselftran" REAL,
  "Pconserv" REAL,
  "Mconformity" REAL,
  "Mtradition" REAL,
  "Mbenov" REAL,
  "Munivers" REAL,
  "Mself" REAL,
  "Mstim" REAL,
  "Mhedon" REAL,
  "Machieve" REAL,
  "Mpower" REAL,
  "Msecurity" REAL,
  "Mopen" REAL,
  "Mselfenh" REAL,
  "Mselftran" REAL,
  "Mconserv" REAL,
  "Pexcitements" REAL,
  "Psuprapersonal" REAL,
  "Pinteractive" REAL,
  "Ppromotion" REAL,
  "Pexistence" REAL,
  "Pnormative" REAL,
  "Linguistic" REAL,
  "Logicmath" REAL,
  "Spatial" REAL,
  "Bodykines" REAL,
  "Musical" REAL,
  "Interpersonal" REAL,
  "Intrapersonal" REAL,
  "Environmental" REAL,
  "Spiritual" REAL
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

#  i can do some queries to check data integrity 

There are a total of 252 unique users 

number of users for each dataset: 

questionnaries -> 249 users 
time-diary     -> 241 
application    -> 234 users 54 million rows
screen         -> 234 users 13 mln rows
location       -> 221 users 1.9 mln rows
touch          -> 201 users 130 mln rows 
notification   -> 183 users 6.7 mln rows



There are 169 users that shared all the data 
There are 18 users missing all the sensors 

after discarding this 18 users there is 1 user missing time diary and 2 missing questionnaires 

After filtering these users

There are 231 users with socio, td , application and screen 

62 users miss data from at least one sensor
13 miss location data 
33 miss touch data 
49 miss location data 

