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


###########################
# Regressions
###########################

# model 0 baseline - main effect
lm_sessions_0 = smf.ols(formula="sessions ~ deviceCategory + treat", data = df_0).fit()
lm_pageviews_0 = smf.ols(formula="pageviews ~ deviceCategory + treat", data = df_0).fit()
lm_unique_0 = smf.ols(formula="uniquePageviews ~ deviceCategory + treat", data = df_0).fit()
lm_transactions_0 = smf.ols(formula="transactions ~ deviceCategory + treat", data = df_0).fit()
lm_revenue_0 = smf.ols(formula="transactionRevenue ~ deviceCategory + treat", data = df_0).fit()
lm_rev_per_trns_0 = smf.ols(formula="avg_rev_per_trns ~ deviceCategory + treat", data = df_0).fit()

# model 1 - baseline + interaction between device and treatment
lm_sessions_1 = smf.ols(formula="sessions ~ deviceCategory*treat", data = df_0).fit()
lm_pageviews_1 = smf.ols(formula="pageviews ~ deviceCategory*treat", data = df_0).fit()
lm_unique_1 = smf.ols(formula="uniquePageviews ~ deviceCategory*treat", data = df_0).fit()
lm_transactions_1 = smf.ols(formula="transactions ~ deviceCategory*treat", data = df_0).fit()
lm_revenue_1 = smf.ols(formula="transactionRevenue ~ deviceCategory*treat", data = df_0).fit()
lm_rev_per_trns_1 = smf.ols(formula="avg_rev_per_trns ~ deviceCategory*treat", data = df_0).fit()

# model 2 - baseline + date
lm_sessions_2 = smf.ols(formula="sessions ~ deviceCategory + treat + date", data = df_0).fit()
lm_pageviews_2 = smf.ols(formula="pageviews ~ deviceCategory + treat + date", data = df_0).fit()
lm_unique_2 = smf.ols(formula="uniquePageviews ~ deviceCategory + treat + date", data = df_0).fit()
lm_transactions_2 = smf.ols(formula="transactions ~ deviceCategory + treat + date", data = df_0).fit()
lm_revenue_2 = smf.ols(formula="transactionRevenue ~ deviceCategory + treat + date", data = df_0).fit()
lm_rev_per_trns_2 = smf.ols(formula="avg_rev_per_trns ~ deviceCategory + treat + date", data = df_0).fit()

# model 3 - interaction with date
lm_sessions_3 = smf.ols(formula="sessions ~ deviceCategory*treat + deviceCategory*date + treat*date", data = df_0).fit()
lm_pageviews_3 = smf.ols(formula="pageviews ~ deviceCategory*treat + deviceCategory*date + treat*date", data = df_0).fit()
lm_unique_3 = smf.ols(formula="uniquePageviews ~ deviceCategory*treat + deviceCategory*date + treat*date", data = df_0).fit()
lm_transactions_3 = smf.ols(formula="transactions ~ deviceCategory*treat + deviceCategory*date + treat*date", data = df_0).fit()
lm_revenue_3 = smf.ols(formula="transactionRevenue ~ deviceCategory*treat + deviceCategory*date + treat*date", data = df_0).fit()
lm_rev_per_trns_3 = smf.ols(formula="avg_rev_per_trns ~ deviceCategory*treat + deviceCategory*date + treat*date", data = df_0).fit()

###########################
# Tables
###########################
print(lm_sessions_0.summary())   # Summarize model
print(lm_sessions_1.summary())   # Summarize model

pystout(models=[lm_sessions_0,lm_sessions_1,
                lm_pageviews_0,lm_pageviews_1,
                lm_unique_0,lm_unique_1,
                lm_transactions_0,lm_transactions_1,
                lm_revenue_0,lm_revenue_1,
                lm_rev_per_trns_0,lm_rev_per_trns_1],
        endog_names=['0','1',
                        '0','1',
                        '0','1',
                        '0','1',
                        '0','1',
                        '0','1'],
        file=os.path.join(main_dir,tables,"table_regression.tex"),
        digits=2,
        mgroups={'Sessions':[1,2],
                                    "Pageviews": [3,4],
                            "Unique views": [5,6],
                            "Transactions": [7,8],
                            "Revenue": [9,10],
                            "Avg. Rev per Trns": [11,12]
},
        modstat={'nobs':'Obs','rsquared_adj':'Adj. R\sym{2}'}
        )


pystout(models=[lm_sessions_2,lm_sessions_3,
            lm_pageviews_2,lm_pageviews_3,
            lm_unique_2,lm_unique_3,
            lm_transactions_2,lm_transactions_3,
            lm_revenue_2,lm_revenue_3,
            lm_rev_per_trns_2,lm_rev_per_trns_3],
        endog_names=['2','3',
                        '2','3',
                        '2','3',
                        '2','3',
                        '2','3',
                        '2','3'],
        file=os.path.join(main_dir,tables,"table_regression_date.tex"),
        digits=2,
        mgroups={'Sessions':[1,2],
                                    "Pageviews": [3,4],
                            "Unique views": [5,6],
                            "Transactions": [7,8],
                            "Revenue": [9,10],
                            "Avg. Rev per Trns": [11,12]
},
        modstat={'nobs':'Obs','rsquared_adj':'Adj. R\sym{2}'}
        )
