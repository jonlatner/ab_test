###########################
# TOP COMMANDS
###########################
# create empty session
globals().clear()

# load libraries
import pandas as pd
import numpy as np
import os
import statsmodels.formula.api as smf
from pystout import pystout
from statsmodels.iolib import summary2

# beginning commands
pd.set_option('display.float_format', str) # drop scientific notation
pd.set_option('display.max_columns', None) # display max columns

# file paths - adapt main_dir pathway
main_dir = "/Users/jonathanlatner/GitHub/ab_test/"
data_files = "data_files/"
graphs = "graphs/"
tables = "tables/"

###########################
# LOAD DATA
###########################

df_0 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test.csv"))

# create new variables
df_0["conversion"] = df_0["transactions"]/df_0["sessions"]

###########################
# Regressions
###########################

# model 0 baseline - main effect
# model1 = smf.ols(formula=formula='price ~ mpg + displacement + C(foreign)', data=dta).fit()

lm_conversion_0 = smf.ols(formula="conversion ~ treat", data = df_0).fit()
print(lm_conversion_0.summary2())   # Summarize model

lm_conversion_1 = smf.ols(formula="conversion ~ deviceCategory + treat", data = df_0).fit()
print(lm_conversion_1.summary2())   # Summarize model

lm_conversion_2 = smf.ols(formula="conversion ~ deviceCategory*treat", data = df_0).fit()
print(lm_conversion_2.summary2())   # Summarize model

lm_conversion_3 = smf.ols(formula="conversion ~ deviceCategory*treat + date*treat", data = df_0).fit()
print(lm_conversion_3.summary2())   # Summarize model
