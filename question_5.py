import sqlite3
import os
import random


def createDatabase():
    connection=None
    cursor=None

    if not os.path.exists("./databases/hyperLink.db"):
        #create table
        connection = sqlite3.connect("./databases/hyperLink.db")
        cursor = connection.cursor()
        
        query_1 = "CREATE TABLE IF NOT EXISTS {}(Device_Type text,Stats_Access_Link text)".format("deviceLinkInformation") 
        cursor.execute(query_1)
        connection.commit()


        #insert random values
        alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        for i in range(100):
            
            deviceType = "{}{}{}{}".format(alphabet[random.randint(0,25)].upper(),alphabet[random.randint(0,25)].upper(),alphabet[random.randint(0,25)].upper(),random.randint(100,999))
            print(deviceType)
            accessLink = "<url>http{}//{}{}{}{}.{}{}{}.com</url>".format(["s:",":"][random.randint(0,1)],alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],random.randint(0,999),alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],alphabet[random.randint(0,25)])
            print(accessLink)
            insertQuery = "INSERT INTO {} VALUES('{}','{}')".format("deviceLinkInformation",deviceType,accessLink)
            cursor.execute(insertQuery)
            connection.commit()
        connection.close()
    


def readDataAndPurify():
    connection = sqlite3.connect("./databases/hyperLink.db")
    cursor = connection.cursor()


    query = "SELECT * FROM {}".format("deviceLinkInformation")
    cursor.execute(query)
    data = cursor.fetchall()
    


    purifiedDataDict = dict()
    for row in list(data):
        deviceType= row[0]
        fullLink = row[1]
        actualLink = fullLink.split("<url>")[1].split("</url>")[0].split("/")[-1]
        print("Actual Link For {} is : {}".format(deviceType,actualLink))
        purifiedDataDict[deviceType] = actualLink


    connection.close()
    return purifiedDataDict

def addColumnToDatabase(purifiedData):
    connection = sqlite3.connect("./databases/hyperLink.db")
    cursor = connection.cursor()

    #dummy query to acces columns
    cursor.execute("SELECT * FROM deviceLinkInformation")
    
    
    if len(cursor.description)==2:
        query = "ALTER TABLE {} ADD purified_link text".format("deviceLinkInformation")
        cursor.execute(query)
        connection.commit()
    

    


    for deviceType in purifiedData.keys():
        query = "UPDATE deviceLinkInformation SET purified_link='{}' WHERE Device_Type='{}'".format(purifiedData[deviceType],deviceType)
        cursor.execute(query)
        connection.commit()


    connection.close()

createDatabase()
purifiedData = readDataAndPurify()
addColumnToDatabase(purifiedData)
