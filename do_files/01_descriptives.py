###########################
# TOP COMMANDS
###########################
# create empty session
globals().clear()

# load libraries
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *

# beginning commands
pd.set_option('display.float_format', str) # drop scientific notation
pd.set_option('display.max_columns', None) # display max columns
plt.clf() # this clears the figure

# file paths - adapt main_dir pathway
main_dir = "/Users/jonathanlatner/GitHub/ab_test/"
data_files = "data_files/"
graphs = "graphs/"
tables = "tables/"

###########################
# LOAD DATA
###########################

df = pd.read_csv(os.path.join(main_dir,data_files,"ga_data_rndm.csv"))

# descriptives
df.columns
df.describe()

# missing values?
df.isnull().sum() 

# one way tabulation of treatment variable
df["ga:dimension13"].value_counts(dropna=False).sort_index() 

###########################
# CLEANING
###########################

# clean variable names by dropping prefix "ga:"
df=df.rename(columns = lambda x: x.strip("ga:"))

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
df = df.drop(['dimension13'], axis=1)

# drop observations where treatment is missing
df = df[df['treat'].notnull()]
df["treat"].value_counts(dropna=False).sort_index()

# Rename values within treatment using dictionary
a = [0, 1]
b = ['Control', 'Treatment']

df['treat'] = df['treat'].map(dict(zip(a, b)))
df["treat"].value_counts(dropna=False)

# drop unnamed variables - what are these?
df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
df.columns

# transform date - all dates occurred in one month (Janurary, 2019)
df['date'] = df['date']-20190100

# this is a fancier way to do dates, but not necessary in this example
# df['date']=pd.to_datetime(df['date'].astype(str), format='%Y-%m-%d')

###########################
# DESCRIPTIVES
###########################

df.describe()
df.columns

###########################
# plot treatment variable
###########################

df["treat"].value_counts(dropna=False).sort_index()

ax = sns.countplot(data=df, x="treat")
for p in ax.patches:
   ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x()+0.25, p.get_height()+0.01))
ax.set_xlabel('')
plt.ylim(0, 500)                        
plt.subplots_adjust(bottom=0.15)
plt.show()

plt.savefig(os.path.join(main_dir,graphs,"plot_treatment.pdf"))
del(ax,p)
plt.clf() # this clears the figure


###########################
# plot treatment per day variable
###########################

df_date = pd.crosstab(df["date"], df["treat"])
df_date["date"] = np.arange(len(df_date))+1 # create date variable as row number + 1
df_date_long = df_date.melt(id_vars='date')
df_date_long

ax=sns.lineplot(data=df_date_long, 
                        y= "value", 
                        x = "date", 
                        hue = "treat")
sns.move_legend(ax, bbox_to_anchor = [.5,-.5], loc = "lower center", ncol=2, title = "")
plt.tight_layout()
plt.ylim(0, 15)
plt.show()

plt.savefig(os.path.join(main_dir,graphs,"plot_treatment_date.pdf"))
del(ax)
plt.clf() # this clears the figure

###########################
# plot categorical variables
###########################

# create df numerical variables (by treat)
df_cat = df.select_dtypes('object')

# convert from wide format to tidy format
df_cat_long = pd.crosstab(df_cat['treat'], df_cat['deviceCategory'], normalize='index')
df_cat_long["treat"] = np.arange(len(df_cat_long)) # create treatment variable as row number
df_cat_long = df_cat_long.melt(id_vars='treat')
df_cat_long

p=sns.catplot(kind='bar', 
                        data=df_cat_long, 
                        hue='treat',
                        x='deviceCategory',
                        y='value', 
                        sharey=False,
                        margin_titles=True,
                        height=2,
                        aspect=1.5
                        )
plt.ylim(0, 1)                        
plt.show()

plt.savefig(os.path.join(main_dir,graphs,"plot_categorical.pdf"))
del(df_cat,df_cat_long,p)
plt.clf() # this clears the figure


###########################
# plot numerical variales
###########################

# create df with categorical variables (by treat)
df_num = df.select_dtypes('number')
df_num.columns

# add treatment variable to categorical variables
df_num["treat"] = df["treat"] 

# convert from wide format to tidy format
df_num_long = df_num.melt(id_vars='treat')

p=sns.catplot(kind='box', 
                        data=df_num_long, 
                        x='treat',
                        y='value', 
                        col='variable',
                        sharey=False,
                        legend=True,
                        margin_titles=True,
                        height=2,
                        aspect=1.5
                        )
                        
p.set_titles(row_template = '{row_name}', col_template = '{col_name}')
p.set(xlabel=None)  # remove the axis label
plt.tight_layout(w_pad=2)
plt.show()
plt.savefig(os.path.join(main_dir,graphs,"plot_numerical.pdf"))

del(df_num,df_num_long,p)
plt.clf() # this clears the figure

###########################
# plot interaction between  numerical and categorical (devices)
###########################

# convert from wide format to tidy format
df_int = df.drop(["date","treat"], axis=1)

df_int["deviceCategory"].value_counts(dropna=False).sort_index()

# Rename values within deviceCategory using dictionary
dict = {"desktop" : 'D', 
        "mobile" : 'M', 
        "tablet": 'T'}
df_int=df_int.replace({"deviceCategory": dict})

df_int_long = df_int.melt(id_vars=["deviceCategory"])
df_int_long

p=sns.catplot(kind='box', 
                        data=df_int_long, 
                        x='deviceCategory',
                        y='value', 
                        col='variable',
                        sharey=False,
                        legend=True,
                        margin_titles=True,
                        height=2,
                        aspect=1.5
                        )
                        
p.set_titles(row_template = '{row_name}', col_template = '{col_name}')
p.tight_layout(w_pad = 5)
plt.show()

plt.savefig(os.path.join(main_dir,graphs,"plot_interaction.pdf"))
del(df_int,df_int_long,p)
plt.clf() # this clears the figure

###########################
# plot two-way interaction between numerical and (categorical and treat)
###########################

# convert from wide format to tidy format
df_int = df

# Rename values within deviceCategory using dictionary
df_int=df_int.replace({"deviceCategory": dict})

df_int_long = df_int.melt(id_vars=["deviceCategory","treat"])
df_int_long

p=sns.catplot(kind='box', 
                        data=df_int_long, 
                        hue='treat',
                        x='deviceCategory',
                        y='value', 
                        col='variable',
                        sharey=False,
                        margin_titles=True,
                        height=2,
                        aspect=1.5
                        )
                        
p.set_titles(row_template = '{row_name}', col_template = '{col_name}')
sns.move_legend(p, loc = "lower center", ncol=2, title = "")
p.tight_layout(w_pad=5)
plt.show()

plt.savefig(os.path.join(main_dir,graphs,"plot_interaction_twoway.pdf"))
del(df_int,df_int_long,p)
plt.clf() # this clears the figure


###########################
# plot new numerical variales - average revenue per transaction
###########################

# create new df with categorical variables (by treat)
df_new = df[["transactionRevenue","transactions","treat","deviceCategory"]] 
df_new["avg_rev_per_trns"] = df_new["transactionRevenue"]/df_new["transactions"]
df_new = df_new.drop(["transactionRevenue","transactions",], axis=1)
df_new.columns

# Rename values within deviceCategory using dictionary
df_new=df_new.replace({"deviceCategory": dict})

# create new variables
df_new["avg_rev_per_trns"] = df_new["transactionRevenue"]/df_new["transactions"]

# convert from wide format to tidy format
df_new_long = df_new.melt(id_vars=['treat',"deviceCategory"])

p=sns.catplot(kind='box', 
              data=df_new_long,
              hue="treat",
              x='deviceCategory',
              y='value', 
              height=3,
              aspect=1.5
)

p.set_titles(row_template = '{row_name}', col_template = '{col_name}')
sns.move_legend(p, loc = "lower center", ncol=2, title = "")
plt.subplots_adjust(bottom=.3) # or whatever
plt.show()

plt.savefig(os.path.join(main_dir,graphs,"plot_new.pdf"))

del(df_new,df_new_long,p)
plt.clf() # this clears the figure

###########################
# plot time trend
###########################

df_time_trend = df

# create new variables
df_time_trend["avg_rev_per_trns"] = df_time_trend["transactionRevenue"]/df_time_trend["transactions"]

# convert from wide format to tidy format
df_time_trend_long = df_time_trend.melt(id_vars=["deviceCategory","treat","date"])

# Rename values within deviceCategory using dictionary
df_time_trend_long["variable"].value_counts(dropna=False).sort_index() 
dict = {"avg_rev_per_trns" : 'Avg. revenues \n per transaction', 
        "pageviews" : 'pageviews', 
        "sessions": 'sessions',
        "transactionRevenue": 'revenue',
        "transactions": 'transactions',
        "uniquePageviews": 'unique \n pageviews',
        }
df_time_trend_long=df_time_trend_long.replace({"variable": dict})
df_time_trend_long["variable"].value_counts(dropna=False).sort_index() 

p = (ggplot(df_time_trend_long, aes('date', 'value', color='treat'))
+ facet_wrap('~deviceCategory+variable',scales="free", ncol = 6)
+ geom_line()
+ theme(
        text = element_text(size = 6),
        # strip_text_x = element_text(size = 6),
        # strip_text_y = element_text(size = 6),
        legend_title=element_blank(),
        subplots_adjust={'wspace':0.75,'hspace':0.5},
        legend_position=(.5, -0.025)))
 
ggsave(plot = p, filename = "plot_time_trend.pdf", path = os.path.join(main_dir,graphs), width = 10, height = 4)

###########################
# Write csv
###########################

df["avg_rev_per_trns"] = df["transactionRevenue"]/df["transactions"]

df.to_csv(os.path.join(main_dir,data_files,"ab_test.csv"))  
