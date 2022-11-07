###########################
# TOP COMMANDS
###########################
# create empty session
globals().clear()

# load libraries
import os
import pandas as pd
import numpy as np
from plotnine import *
from scipy.stats import ttest_ind_from_stats

# beginning commands
# np.set_printoptions(suppress=True) # drop scientific notation
pd.set_option('display.max_columns', None) # display max columns

# file paths - adapt main_dir pathway
main_dir = "/Users/jonathanlatner/GitHub/ab_test/"
data_files = "data_files/"
graphs = "graphs/"
tables = "tables/"

# https://linuxtut.com/en/1a81ea350b2efbbd1979/
#Set the desired parameter to None
#alternative is"one_sided" "two_sided"Select either
#Returns each obtained parameter as a dictionary type
def power_prop_test(n=None, p1=None, p2=None, sig_level=0.05, power=None,
                    alternative="one_sided", strict=False,
                    tol=2.220446049250313e-16**0.25):
    
    from math import sqrt
    from scipy.stats import norm
    from scipy.optimize import brentq
    
    missing_params = [arg for arg in [n, p1, p2, sig_level, power] if not arg]
    num_none = len(missing_params)
    
    if num_none != 1:
        raise ValueError("exactly one of 'n', 'p1', 'p2', 'power' and 'sig.level'must be None")
        
    if sig_level is not None:
        if sig_level < 0 or sig_level > 1:
            raise ValueError("\"sig_level\" must be between 0 and 1")

    if power is not None:
        if power < 0 or power > 1:
            raise ValueError("\"power\" must be between 0 and 1")
        
    if alternative not in ["two_sided", "one_sided"]:
        raise ValueError("alternative must be \"two_sided\" or \"one_sided\"")
    t_side_dict = {"two_sided":2, "one_sided":1}
    t_side = t_side_dict[alternative]
        
    # compute power 
    def p_body(p1=p1, p2=p2, sig_level=sig_level, n=n, t_side=t_side, strict=strict):
        if strict and t_side==2:
            qu = norm.ppf(1-sig_level/t_side)
            d = abs(p1-p2)
            q1 = 1-p1
            q2 = 1-p2
            pbar = (p1 + p2) / 2
            qbar = 1 - pbar
            v1 = p1 * q1
            v2 = p2 * q2
            vbar = pbar * qbar
            power_value = (norm.cdf((sqrt(n) * d - qu * sqrt(2 * vbar))/sqrt(v1 + v2))
                    + norm.cdf(-(sqrt(n) * d + qu * sqrt(2 * vbar))/sqrt(v1 + v2)))
            return power_value
                
        else:
            power_value = norm.cdf((sqrt(n) * abs(p1 - p2) - (-norm.ppf(sig_level / t_side)
                        * sqrt((p1 + p2) * (1 - (p1 + p2)/2)))) / sqrt(p1 * 
                        (1 - p1) + p2 * (1 - p2)))
            return power_value
    
    if power is None:
        power = p_body()

    # solve the equation for the None value argument 
    elif n is None:
        def n_solver(x, power=power):
            return p_body(n=x) - power
        n = brentq(f=n_solver, a=1, b=1e+07, rtol=tol, maxiter=1000000)

    elif p1 is None:
        def p1_solver(x, power=power):
            return p_body(p1=x) - power
        try:
            p1 = brentq(f=p1_solver, a=0, b=p2, rtol=tol, maxiter=1000000)
        except:
            ValueError("No p1 in [0, p2] can be found to achive the desired power")
        
    elif p2 is None:
        def p2_solver(x, power=power):
            return p_body(p2=x) - power
        try:
            p2 = brentq(f=p2_solver, a=p1, b=1, rtol=tol, maxiter=1000000)
        except:
            VealueError("No p2 in [p1, 1] can be found to achive the desired power")

    elif sig_level is None:
        def sig_level_solver(x, power=power):
            return p_body(sig_level=x) - power
        try:
            sig_level = brentq(f=sig_level_solver, a=1e-10, b=1-1e-10, rtol=tol, maxiter=1000000)
        except:
            ValueError("No significance level [0,1] can be found to achieve the desired power")
            
    print("""
    Sample size: n = {0}
    Probability: p1 = {1}, p2 = {2}
    sig_level = {3},
    power = {4},
    alternative = {5}
    
    NOTE: n is number in "each" group
    """.format(n, p1, p2, sig_level, power, alternative))
    #Each parameter is returned in a dictionary with argument names as keys
    params_dict = {"n":n, "p1":p1, "p2":p2,
                   "sig_level":sig_level, "power":power, "alternative":alternative}
    
    return params_dict


###########################
# LOAD DATA
###########################

df = pd.read_csv(os.path.join(main_dir,data_files,"ab_test.csv"))

###########################
# DESCRIPTIVES
###########################

df.describe()
df.columns

df["treat"].value_counts(dropna=False).sort_index()
df['sessions'].sum()


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

graph_revenues = (ggplot(df_revenues, aes(x = 'treat', y = "value", label = "value"))
+ geom_bar(stat="identity")   
+ geom_text(nudge_y=-0.5, format_string='{:.2f}', va="bottom")
+ facet_wrap('~type',scales="free")
+ ylab("Revenues (1000s)")
+ theme(
        axis_title_x = element_blank(),
        subplots_adjust={'wspace':0.25}
        )
)

graph_revenues
ggsave(plot = graph_revenues, filename = "graph_revenues.pdf", path = os.path.join(main_dir,graphs), width = 10, height = 4)

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

graph_cv = (ggplot(df_graph, aes(x = 'treat', y='value', label="value"))
+ geom_bar(stat="identity")   
+ geom_errorbar(aes(x = 'treat', ymin="ymin", ymax="ymax"), width=.2)
+ geom_hline(yintercept = 0) # add one horizonal line
+ geom_text(nudge_x=0.1, format_string='{:.3f}', ha="left", va="bottom", position = position_dodge(width = 0.9))
+ ylab("Percent")
+ facet_wrap('~type',scales="free")
+ theme(
        # legend_title=element_blank(),
        axis_title_x = element_blank(),
        subplots_adjust={'wspace':0.25}
        )
)
        
graph_cv
ggsave(plot = graph_cv, filename = "graph_cr.pdf", path = os.path.join(main_dir,graphs), width = 10, height = 4)


# power = power_prop_test(n=None, p1=.0059, p2=.0060, sig_level=0.05, power=.8, alternative="two_sided")
# power["n"]/df_converted["sessions"][0]
