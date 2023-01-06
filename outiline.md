- csv to sqlite 
- clean the data
- sqlite to csv yardstick

- analysis 









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







