"""
Unit tests for the Wrangler Script
"""

from wrangler import *


# Test Table Extraction
body = extractTableFromUrl("https://en.wikipedia.org/wiki/Road_safety_in_Europe","wikitable")
data = getRowsNColumns(body)
df = createDataFrame(data[0],data[1])


# Display Statistics
df.describe()


# Create Charts for Header
makeChartsDirectory("charts")

print("info:-----> Creating barplots for each Header Variable")
createVarPlotByCountry(df,'AreaByCountry.png','Area\n(thousands of km2)[24]','blue','bar')
createVarPlotByCountry(df,'PopulationByCountry.png','Population in 2018[25]','pink','bar')
createVarPlotByCountry(df,'GDPByCountry.png','GDP per capita in 2018[26]','orange','bar')
createVarPlotByCountry(df,'VehicleByCountry.png','Vehicle ownership\n(per thousand inhabitants) in 2016[28]','teal','bar')
createVarPlotByCountry(df,'DeathByCountry.png','Total Road Deaths in 2018[30]','sienna','bar')


# Create regression Charts
print("info:-----> Creating Regression Plots to check for Association")
regressionChart(df,'Population in 2018[25]', 'Vehicle ownership\n(per thousand inhabitants) in 2016[28]', 'Population vs Vehicle Ownership','Population vs Vehicle Ownership')
regressionChart(df,'Population in 2018[25]','Road deaths\nper Million Inhabitants in 2018[30]', 'Population vs Death','Population vs Death') 
regressionChart(df,'Vehicle ownership\n(per thousand inhabitants) in 2016[28]','Road deaths\nper Million Inhabitants in 2018[30]', 'Vehicle vs Death','Vehicle vs Death')
regressionChart(df,'GDP per capita in 2018[26]','Road deaths\nper Million Inhabitants in 2018[30]', 'GDP vs Death','GDP vs Death')
regressionChart(df,'Area\n(thousands of km2)[24]', 'Vehicle ownership\n(per thousand inhabitants) in 2016[28]', 'Area vs Vehicle Ownership','Area vs Vehicle Ownership')
regressionChart(df,'Area\n(thousands of km2)[24]', 'Population in 2018[25]', 'Area vs Population','Area vs Population')


# Create Histogram Distributions
print("info:-----> Creating Histogram Distributions")
makeDistribution(df,'Population density\n(inhabitants per km2) in 2017[27]', 'Distribution of Population Density','Distribution of Population Density')
makeDistribution(df,'Total Road Deaths in 2018[30]', 'Distribution of Deaths','Distribution of Deaths')
makeDistribution(df,'GDP per capita in 2018[26]', 'Distribution of GDP','Distribution of GDP')
makeDistribution(df,'Vehicle ownership\n(per thousand inhabitants) in 2016[28]', 'Distribution of Vehicle Ownership','Distribution of Vehicle Ownership')
makeDistribution(df,'Road deaths\nper Million Inhabitants in 2018[30]', 'Distribution of Deaths II','Distribution of Deaths II')


# Create Statistics
print("info:-----> Creating Average Statistics Graph")
makeAverage(df,'Area\n(thousands of km2)[24]','Average Area in different countries','Average Area in different countries')
makeAverage(df,'Total Road Deaths in 2018[30]','Average Death by Country','Average Death by Country')

