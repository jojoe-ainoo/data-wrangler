"""
@author: Emmanuel Jojoe Ainoo
@brief:  This program extracts a table summary of European Union Road Safety Facts and Figures
from a wikipedia webpage
"""

# -------> DEPENDENCIES
# python3,requests pandas, BeautifulSoup, re, matplotlib, numpy, os, sys


# -------> IMPORTS
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# -------> FUNCTIONS
"""
@brief: This function extracts a specific table from the url using BeautifulSoup
@param url: string - wikipedia url to extract data from
@param tagclass: string - class tag of specific table to extract
@returns body: list - table extracted
"""
def extractTableFromUrl(url, tagclass):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")

    all_tables = soup.find_all("table", attrs={"class":tagclass}) # Extract all table tag data with specific class
    wikitable = all_tables[0] # select wikitable from array of tables since its the first table on the page
    body = wikitable.find_all("tr") # select all rows from table
    print("info:-----> Wikitable Found & Extracted from Page")
    
    return body

"""
@brief: This function cleans the data, and organizes the rows and columns
@param body: list - body of exracted table
@returns list - headers and rows
"""

def getRowsNColumns(body):
    header = body[0] # first item in body is header row
    rows = body[1:] # rest of items are body data of table

    headers = [] # store list of headers(column names)
    for each in header.find_all("th"): # loop through table headers
        each = (each.text).rstrip("\n") # convert elements to texts and remove newline char
        headers.append(each) # append each header to headers list
    print("info:-----> Headers for Table have been Created")

    all_rows = [] # store rows of table
    for i in range(len(rows)): # loop through all row entries clean, and store in list
        row = []
        for j in rows[i].find_all("td"): # find table data - rows
            entry = re.sub("(\xa0)|(\n)|(†a)|,","",j.text) # remove newline character, ',', unwanted characters
            row.append(entry)  # append one row entry
        all_rows.append(row) # append one row to all rows
    print("info:-----> Data rows have been Cleaned & Stored")
    return [headers,all_rows] # return a list of headers and all rows

"""
@brief: This function creates a pandas dataframe with the headers and rows retrieved
@param headers: list - a list of headers (column names)
@param all_rows: list - a list of table rows
@return df: a pandas dataframe of the table extracted
"""
def createDataFrame(headers,all_rows):
    df = pd.DataFrame(data=all_rows,columns=headers) # create dataframe
    # select only relevant columns
    df = df.drop(['Road Network Length\n(in km) in 2013[29]', 'Number of People Killed\nper Billion km[30]', 'Number of Seriously Injured in 2017/2018[30]'], axis=1) 
    df['Year'] = 2018  #create year column
    df = df[['Country','Year','Area\n(thousands of km2)[24]','Population in 2018[25]','GDP per capita in 2018[26]','Population density\n(inhabitants per km2) in 2017[27]','Vehicle ownership\n(per thousand inhabitants) in 2016[28]','Total Road Deaths in 2018[30]','Road deaths\nper Million Inhabitants in 2018[30]']]
    print("info:-----> Dataframe with rows and headers have been Created with the Relevant Columns") 
    print(df)

    #sort values by column
    df = df.sort_values(by=['Road deaths\nper Million Inhabitants in 2018[30]'])
    print("info:-----> Dataframe sorted by Road Deaths Column")
    df.head()

    #save dataframe as csv
    df.to_csv('road_safety.csv', index=False)
    print("info:-----> Dataframe is saved as a CSV fle")

    return df


# -------> CHART FUNCTIONS
"""
@brief: This function creates a directory for charts
@param directory_name: string - directory name
@returns void
"""
def makeChartsDirectory(directory_name):
    try: 
        os.mkdir(directory_name) 
    except OSError as error: 
        print(error)  

"""
@brief: This function creates a bar chart for each variable header(column name) of a pandas dataframe
@param df: object - pandas dataframe
@param filename: string - filename to save chart generated
@param var: string - variable header to create bar plot for
@color: string - specify color of plot
@charttype: string - specify plot type (bar,line)
@returns void
"""
def createVarPlotByCountry(df, filename, var, color,charttype):
    data = df.drop(labels=28, axis=0)
    chart = pd.DataFrame(data, columns=['Country',var])
    chart[var] = chart[var].astype(float)
    chart.plot(x ='Country', y=var, color=color, kind =charttype)
    filename = os.path.join('charts/',filename)
    plt.savefig(filename,dpi=300, bbox_inches='tight')

"""
@brief: This function plots a regression chart between two variables
@param df: object - pandas dataframe
@param var1: string - variable header 1
@param var2: string - variable header 2
@param filename: string - filename to save chart generate
@returns void
"""

def regressionChart(df, var1, var2, title, filename):
    data = df.drop(labels=28, axis=0)
    data = data.apply(pd.to_numeric,errors='ignore')
    data.plot(x=var1, y=var2, kind='scatter',
        figsize=(10,6),
        title=title)
    filename = os.path.join('charts/',filename)
    plt.savefig(filename,dpi=300, bbox_inches='tight')

"""
@brief This function creates a distribution with the frequencies for columns
@param df: object - pandas dataframe
@param title: string - title of chart
@param filename: string - filename to save chart generate
@returns void
"""

def makeDistribution(df,column_name,title,filename):
    data = df.drop(labels=28, axis=0)
    data = data.apply(pd.to_numeric,errors='ignore')
    data[column_name].plot(kind='hist', figsize=(10,6), title='title')
    filename = os.path.join('charts/',filename)
    plt.savefig(filename,dpi=300, bbox_inches='tight')

"""
@brief: This function creates a plot with the averages of coloumns
@param df: object - pandas dataframe
@param column_name: string - column name
@param title: string - title of chart
@returns void
"""
def makeAverage(df,column_name,title, filename):
    data = df.drop(labels=28, axis=0)
    data = data.apply(pd.to_numeric,errors='ignore')
    data[['Country',column_name]].groupby('Country').mean().plot.bar(figsize=(10,6), rot=45, title=title)
    filename = os.path.join('charts/',filename)
    plt.savefig(filename,dpi=300, bbox_inches='tight')


