select  touch.userid, 
        date(touch.timestamp) as day,  
        strftime('%H', touch.timestamp) as hour, 
        strftime('%M', touch.timestamp) as min, 
        count(*) as touches
from (select * from touch LIMIT 1000) as touch

group by touch.userid, 
        date(touch.timestamp), 
        strftime('%H', touch.timestamp), 
        strftime('%M', touch.timestamp)


select  app.userid,
        date(app.timestamp) as day,  
        strftime('%H', app.timestamp) as hour, 
        strftime('%M', app.timestamp) as min, 
        application as apps
from (select * from application LIMIT 1000) as app

group by app.userid, 
        date(app.timestamp), 
        strftime('%H', app.timestamp), 
        strftime('%M', app.timestamp)