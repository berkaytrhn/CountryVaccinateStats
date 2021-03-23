import pandas as pd 

def topThreeCountryFinder(df):
    #create median frame"
    medianFrame = df.groupby(["country"])["daily_vaccinations"].median().reset_index()

    #renaming median column
    medianFrame.columns = [label if label=="country" else "median" for label in medianFrame.columns]

    
    #sorting dataframe
    medianFrame.sort_values(by="median",ascending=False,kind="mergesort",inplace=True)

    #printing top-3 countries with highest median daily vaccination
    print("-----Top-3 Countreis With Highest Median Daily Vaccination-----")
    for index,data in enumerate(medianFrame.head(3).itertuples()):
        
        #converting pandas.core.frame object to python list
        data = list(data)

        print("{} -> {}, median value : {}".format(index+1,data[1],data[2]))







file = pd.read_csv("./imputed_country_vaccination_stats.csv",sep=",")
dataFrame = pd.DataFrame(file)


topThreeCountryFinder(dataFrame)
