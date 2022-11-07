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

df = pd.read_csv(os.path.join(main_dir,data_files,"ab_test.csv"))

###########################
# DESCRIPTIVES
###########################

df.describe()
df.columns

df["date"].value_counts(dropna=False).sort_index()
df['sessions'].sum()

#Use Filter Function
df=df[(df["date"] >= 20190122)&(df["date"] <= 20190131)]

df["date"].value_counts(dropna=False).sort_index()

###########################
# Find the difference in revenues
###########################

df_revenues = df.groupby(['treat'])[["revenues"]].sum().reset_index()
df_revenues["revenues"]=df_revenues["revenues"]/1000
df_revenues["type"]=" Revenues (1000s)"
df_revenues = df_revenues.rename(columns={"revenues":"value"})
df_revenues

data = {"treat":[" "],
        'value': df_revenues["value"][1]-df_revenues["value"][0],
        'type': ["Difference (T-C)"]
        }

df_diff = pd.DataFrame(data)
df_diff
df_revenues = pd.concat([df_revenues,df_diff])
df_revenues
df_revenues["type"].value_counts(dropna=False).sort_index()

# Write csv
df_revenues.to_csv(os.path.join(main_dir,data_files,"ab_test_revenues_wk_4.csv"))  

###########################
# Find the difference, mean, sem outcome by treatment
# KPI = Converted (CR)
###########################

df_converted = df.groupby(['treat'])[['sessions',"transactions"]].sum().reset_index()
df_converted["cr"] = df_converted["transactions"]/df_converted["sessions"]
df_converted["variance"] = df_converted["cr"] * (1-df_converted["cr"])
df_converted["cr_se"] = np.sqrt(df_converted["cr"] * 
                                        (1-df_converted["cr"]) / 
                                        df_converted["sessions"])
                                        
df_converted

# Difference
diff = (df_converted["cr"][1]-df_converted["cr"][0])
diff_se = np.sqrt(df_converted["cr_se"][0]**2+df_converted["cr_se"][1]**2)
pvalue = ttest_ind_from_stats(mean1=df_converted["cr"][0], std1=np.sqrt(df_converted["variance"][0]), nobs1=df_converted["sessions"][0],
                                mean2=df_converted["cr"][1], std2=np.sqrt(df_converted["variance"][1]), nobs2=df_converted["sessions"][1])[1]
                     
data = {'type': ["Difference (T-C)"],
        "treat":[" "],
        'value': [diff],
        "value_se": [diff_se]}

df_diff = pd.DataFrame(data)
del(diff,diff_se,pvalue,data)

# Prepare data for graph
# Mean
df_mean = df_converted[["cr","treat"]]
df_mean = df_mean.melt(id_vars=["treat"],value_name='value') # reshape long
del df_mean['variable']

# Standard error
df_mean_se = df_converted[["cr_se","treat"]]
df_mean_se = df_mean_se.melt(id_vars=["treat"],value_name='value_se') # reshape long
del df_mean_se['variable']

# Merge mean
df_graph = df_mean.merge(df_mean_se)
df_graph["type"] = "Conversion rate"
del(df_mean,df_mean_se)

# Add difference
df_graph = pd.concat([df_graph,df_diff])

# Standard error
df_graph["value"] = df_graph["value"]*100
df_graph["value_se"] = df_graph["value_se"]*100
df_graph["ymin"] = df_graph["value"]-1.96*df_graph["value_se"]
df_graph["ymax"] = df_graph["value"]+1.96*df_graph["value_se"]

# Write csv
df_graph.to_csv(os.path.join(main_dir,data_files,"ab_test_cr_wk_4.csv"))  
