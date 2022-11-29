SELECT  touch.userid,
        touch.day ,  
        touch.hour,
        touch.min, 
        touch.sec,  
        touch.touches,
        diary.what
FROM 
(select  touch.userid, 
        strftime('%d-%m', touch.timestamp) as day,  
        strftime('%H', touch.timestamp) as hour, 
        strftime('%M', touch.timestamp) as min, 
        strftime('%S', touch.timestamp) as sec,  
        count(*) as touches
from touch
group by touch.userid, 
        strftime('%d-%m', touch.timestamp), 
        strftime('%H', touch.timestamp), 
        strftime('%M', touch.timestamp), 
        strftime('%S', touch.timestamp) 
)as touch
left join diary 
        on touch.userid = diary.userid AND 
        touch.day = strftime('%d-%m', diary.timestamp) AND 
        touch.hour = strftime('%H', diary.timestamp) AND 
        touch.min  = strftime('%M', diary.timestamp)

SELECT year, month, day, hour ,min, diary.what 
FROM yd
LEFT JOIN diary 
ON  yd.year =  strftime('%Y', diary.timestamp) AND
    yd.month =   strftime('%m', diary.timestamp) AND
    yd.day =   strftime('%d', diary.timestamp) AND
    yd.hour =   strftime('%H', diary.timestamp) AND
    yd.min =   strftime('%M', diary.timestamp) AND
    yd.userid = diary.userid

