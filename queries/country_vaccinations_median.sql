WITH processed as(
    SELECT country,date,vaccine_number,count,
        MAX(count) OVER (PARTITION BY country) as number_of_rows
    FROM
    (
        WITH temptable as(
            SELECT country,date,vaccine_number,PERCENT_RANK() OVER (PARTITION BY country ORDER BY country asc,vaccine_number asc) as relative_rank
            FROM country_vaccination_stats
        )
        SELECT country,date,vaccine_number,relative_rank,ROW_Number() OVER (PARTITION BY country ORDER BY relative_rank) as count
        FROM temptable
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