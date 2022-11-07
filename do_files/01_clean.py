###########################
# TOP COMMANDS
###########################
# create empty session
globals().clear()

# load libraries
import os
import pandas as pd
import numpy as np

# beginning commands
# np.set_printoptions(suppress=True) # drop scientific notation
pd.set_option('display.max_columns', None) # display max columns

# file paths - adapt main_dir pathway
main_dir = "/Users/jonathanlatner/GitHub/ab_test/"
data_files = "data_files/"
graphs = "graphs/"
tables = "tables/"

###########################
# LOAD DATA
###########################

df = pd.read_csv(os.path.join(main_dir,data_files,"ga_data_rndm.csv"))

# one way tabulation of treatment variable
df["ga:dimension13"].value_counts(dropna=False).sort_index() 

###########################
# CLEANING
###########################

# clean variable names by dropping prefix "ga:"
df=df.rename(columns = lambda x: x.strip("ga:"))

# drop unnamed variables - what are these?
df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]

# create new treatement variable
# transform df["dimension13"] into integer (0/1)
# drop old treatment variable

df["dimension13"].value_counts(dropna=False).sort_index()
conditions = [
    df["dimension13"].str.contains('Recommendation Slide:0'),
    df["dimension13"].str.contains('Recommendation Slide:1')]
values = [0, 1]
df['treat'] = np.select(conditions, values, default=np.nan)
del(conditions,values)

# df2 = df.query('treat == 0 & deviceCategory == "desktop"').sort_values(by=["date"])
# df2["dimension13"].value_counts(dropna=False).sort_index()

df = df.drop(['dimension13'], axis=1)

# drop observations where treatment is missing
df = df[df['treat'].notnull()]
df["treat"].value_counts(dropna=False).sort_index()

# Rename values within treatment using dictionary
a = [0, 1]
b = ['Control', 'Treatment']

df['treat'] = df['treat'].map(dict(zip(a, b)))
del(a,b)
df["treat"].value_counts(dropna=False)


# rename
df = df.rename(columns={"transactionRevenue":"revenues",
                        "deviceCategory":"device",
                        "uniquePageviews":"uniqueviews"})
                        
# arrange
df = df[["treat","device","date","pageviews","uniqueviews","sessions","revenues","transactions"]]

# in dimension13, treatment/control was subdivided into 4 groups
# In short: In other groups, beside 'Recommendation Slide', we are not interested.
# therefore, aggregate by treatment, device, and date
df = df.groupby(['treat',"device","date"]).sum().reset_index().sort_values(by=["treat","device","date"])

###########################
# Write csv
###########################

df.to_csv(os.path.join(main_dir,data_files,"ab_test.csv"))  

