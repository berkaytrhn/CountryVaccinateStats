# CountryVaccinateStats
Technical Assesment Task For An Internship Application

## question_1.py

Filling the missing data in "country_vaccination_stats.csv" for each country according to their minimum vaccination number and saving it as "imputed_country_vaccination_stats.csv"

## question_2.py

Find top three countries which have highest median daily vaccinations from "imputed_country_vaccination_stats.csv".


## question_3.py

Find number of vaccinations done in specific date from "imputed_country_vaccination_stats.csv".

## question_4.py

Filling the missing data in "country_vaccination_stats.csv" for each country according to their median value of vaccination number and only sql is used unlike question_1.py and values updated on "dailyVaccinations.db" database with relevant queries.

## question_5.py

Created a database which contains "Device_Type" and "Stats_Access_Link" columns. Program extracts actual link information from Stats_Access_Link column and appends it to "hyperLink.db" as a new column named "purified_link" 
  Example : 
```shell 
    initial link :  <url>http://ABC5.xyz.com</url>
    purified link : ABC5.xyz.com
``` 
