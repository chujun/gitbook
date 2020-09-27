select state,sum(duration) as Total_R,
    round(100*sum(duration)/
        (select sum(duration) from information_schema.profiling
        where query_id=@query_id),2) as Pct_R,
    count(*) as Calls,
    sum(duration)/count(*) as "R/Call"
from information_schema.profiling
where query_id=@query_id
group by state
order by Total_R desc;