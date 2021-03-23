import numpy as np 
import pandas as pd 



def fillEmptyColumns(null_df,df):
    minValuesGrouped = df.groupby(["country"])["daily_vaccinations"].min().reset_index()
    print(minValuesGrouped)
    for country in null_df["country"]:
        relatedValue = minValuesGrouped.loc[minValuesGrouped["country"] == country]["daily_vaccinations"]
        print(relatedValue.values[0], "\n********")
        #have the minimum values, finally insert values to relevant columns of dataframe 
       
        



file = pd.read_csv("./country_vaccination_stats.csv",sep=",")
dataFrame = pd.DataFrame(file)




nullVaccineCountries = dataFrame[dataFrame[dataFrame.columns[2]].isnull()].reset_index()
print(nullVaccineCountries)

fillEmptyColumns(nullVaccineCountries,dataFrame)