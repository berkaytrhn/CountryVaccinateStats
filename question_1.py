import numpy as np 
import pandas as pd 



def fillEmptyColumns(df):
    null_df = df[dataFrame["daily_vaccinations"].isnull()]

    #extract data frame as replaced daily_vaccinations column with min_values
    minValuesGrouped = df.groupby(["country"])["daily_vaccinations"].min().reset_index()
    minValuesGrouped.columns = ["min_values" if each=="daily_vaccinations" else each for each in minValuesGrouped.columns]
    for index in null_df.index:        

        #extracting country name to get relevant min value for each country
        country = null_df.loc[index,:].tolist()[0]


        #getting row of current country from mimimum value frame
        relevantRow = minValuesGrouped.loc[minValuesGrouped["country"] == country]["min_values"]

        #check if minimum daily_vaccinations is nan or not to determine which value will be assigned to nan valued samples
        relevantValue = None
        if relevantRow.isna().values[0]:
            #no data provided, insert 0
            relevantValue = 0
        else:
            #min value exists, get it
            relevantValue = relevantRow.values[0]


        
        #imputing missing data
        df.loc[index,"daily_vaccinations"] = relevantValue
       
        


#read csv file and create dataFrame
file = pd.read_csv("./country_vaccination_stats.csv",sep=",")
dataFrame = pd.DataFrame(file)



#call relevant function
fillEmptyColumns(dataFrame)


#writing imputed version of dataset
dataFrame.to_csv("./imputed_country_vaccination_stats.csv")
