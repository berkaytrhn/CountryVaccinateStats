import pandas as pd 



def numberOfTotalVaccination(df,date):
    grouped = df.groupby(["date"])["daily_vaccinations"].sum().reset_index()

    grouped.columns = [label if label=="date" else "daily_total_vaccinations" for label in grouped.columns]

    filtering = grouped["date"]==date
    resultFrame = grouped[filtering]
    

    for index,row in enumerate(resultFrame.itertuples()):
        row = list(row)
        print("Number of vaccinations done on {} is {}".format(date,row[2]))





file = pd.read_csv("./imputed_country_vaccination_stats.csv")
dataFrame = pd.DataFrame(file)


numberOfTotalVaccination(dataFrame,"1/6/2021")
