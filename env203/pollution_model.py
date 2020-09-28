# ENVSCI 203 Urban Pollution Model
# Created for assignment 4
#
# Created by Samuel Kolston
# Created on: 280920
# Last edited: 280920

# constants
import pandas as pd

# read excel data and save as pandas dataframe
df = pd.read_excel("sitedata_python.xlsx")
# print(df.head())

print(df["Time"].head())

# calculates denoted X variable
def getX(windspeed, trafficflow, vehiclespeed):
    return (trafficflow * vehiclespeed ** (-0.75)) / (windspeed + 0.5)


print(getX(0.36, 1200, 6.2))
