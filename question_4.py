import sqlite3
import pandas as pd 
import numpy as np 
import os

class Database:
    connection=None
    cursor=None
    df=None
    dfArray=None
    tableName="country_vaccination_stats"
    
    def __init__(self,dataFrame,rowArray):
        self.connection = sqlite3.connect("./databases/dailyVaccinations.db")
        self.cursor = self.connection.cursor()
        self.df=dataFrame
        self.dfArray=rowArray
        
    def closeConnection(self):
        self.connection.close()
    
    def addRow(self,rowArray):
        #parsing
        for i in rowArray:
            i = list(i)
            country = i[1]
            date = i[2]
            dailyVaccination = i[3]
            vaccines = i[4]
            
            numericValue = np.fromstring("{},{}".format(i[3],i[3]),dtype=float,sep=",")

            if np.isnan(numericValue[0]):
                dailyVaccination=None

            query = "INSERT INTO {} VALUES('{}','{}','{}','{}')".format(self.tableName,country,date,dailyVaccination,vaccines)
            self.cursor.execute(query)
            self.connection.commit()
            

    def createTable(self,name):
        query = "CREATE TABLE IF NOT EXISTS {}(country text,date text,vaccine_number integer,vaccines text)".format(name)
        self.cursor.execute(query)
        self.connection.commit()
        self.tableName=name

    def displayAllTables(self):
        print("----Table {}----".format(self.tableName))
        query = "SELECT * FROM {}".format(self.tableName)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        for row in data:
            print(row)

    def updateMissingData(self):
        #execute sql file and fetch data
        sql_median_file = open("./queries/country_vaccinations_median.sql")
        sql_string = sql_median_file.read()
        self.cursor.execute(sql_string)
        data = self.cursor.fetchall()


        #create dataframe from fetched data
        df = pd.DataFrame(data)
        
        #updating columns
        df.columns = ["country" if index==0 else "median_value" for index in range(len(df.columns))]

        #updating nan values
        for row in df.itertuples():
            rowList = list(row)
            countryName = rowList[1]
            medianValue = int(rowList[2])
            query = "UPDATE {} SET vaccine_number={} WHERE country='{}' AND vaccine_number='None'".format(self.tableName,medianValue,countryName)
            self.cursor.execute(query)
            self.connection.commit()


        
def main():
    file = pd.read_csv("./country_vaccination_stats.csv",sep=",")
    df = pd.DataFrame(file)

    rowArray = np.array([row for row in df.itertuples()])



    
    
    if os.path.exists("./databases/dailyVaccinations.db"):
        os.remove("./databases/dailyVaccinations.db")
    
    
    
    
    database = Database(df,rowArray)
    database.createTable("country_vaccination_stats")
    database.addRow(database.dfArray)
    database.updateMissingData()

    database.closeConnection()




main()
