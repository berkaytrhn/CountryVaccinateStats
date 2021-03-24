-- CREATE VIEW null_values AS 
/* SELECT *,ROW_Number() over (ORDER BY country asc,vaccine_number asc) as index_number
FROM country_vaccination_stats as cvs
WHERE vaccine_number="None";
 */

--SELECT * FROM country_vaccination_stats ORDER BY country ASC, vaccine_number ASC;

SELECT * FROM country_vaccination_stats;



WITH Indexed as(
    SELECT country,vaccine_number,ROW_Number() over(ORDER BY country asc,vaccine_number asc) as index_number
    FROM country_vaccination_stats
)
SELECT country,index_number
FROM Indexed
WHERE vaccine_number="None";




SELECT *

FROM 

(SELECT *
 FROM country_vaccination_stats 
ORDER BY country asc,vaccine_number asc) 
GROUP BY country;

-------
SELECT * FROM country_vaccination_stats ORDER BY country asc,vaccine_number asc;

WITH processed as(
    SELECT country,date,vaccine_number,count,
        MAX(count) OVER (PARTITION BY country) as number_of_rows
    FROM
    (
        WITH mything as(
            SELECT country,date,vaccine_number,PERCENT_RANK() OVER (PARTITION BY country ORDER BY country asc,vaccine_number asc) as relative_rank
            FROM country_vaccination_stats
        )
        SELECT country,date,vaccine_number,relative_rank,ROW_Number() OVER (PARTITION BY country ORDER BY relative_rank) as count
        FROM mything
    )
)SELECT country, avg(vaccine_number) as median_vaccination
FROM processed
WHERE
        CASE 
            WHEN (number_of_rows-1)%2=0 THEN
                (count = (number_of_rows/2)+1 OR count = number_of_rows/2)
            ELSE
                count = CAST(((number_of_rows-1)/2)as INT)+1
        END
GROUP BY country;
--------



SELECT * 
FROM country_vaccination_stats 
WHERE country like 'C%' AND country like '%a';

/* 
SELECT country,date,vaccine_number,count,number_of_rows,
    CASE 
        WHEN number_of_rows % 2=0 THEN 
            (
                SELECT AVG(vaccine_number)
                FROM processed
                WHERE count = (number_of_rows/2)+1 OR count = number_of_rows/2
            )
        ELSE
            (
                SELECT AVG(vaccine_number)
                FROM processed
                WHERE count =  CAST((number_of_rows/2)as INT) OR count = CAST((number_of_rows/2)as INT)+1 OR count = CAST((number_of_rows/2)as INT)+2
            )
        END median
FROM processed
GROUP BY country; */

WITH stats as(
    SELECT 
        country,    
        AVG(vaccine_number) OVER (PARTITION BY country) as average,
        MIN(vaccine_number) OVER (PARTITION BY country) as minimum,
        SUM(vaccine_number) OVER (PARTITION BY country) as summation,
        COUNT(vaccine_number) OVER (PARTITION BY country) as count 
    FROM country_vaccination_stats
)
SELECT country,average,minimum,summation,count 
FROM stats 
GROUP BY country;

