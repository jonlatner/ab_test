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

df_cr_1 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_cr_wk_1.csv"))
df_cr_2 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_cr_wk_2.csv"))
df_cr_3 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_cr_wk_3.csv"))
df_cr_4 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_cr_wk_4.csv"))

df_revenues_1 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_revenues_wk_1.csv"))
df_revenues_2 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_revenues_wk_2.csv"))
df_revenues_3 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_revenues_wk_3.csv"))
df_revenues_4 = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_revenues_wk_4.csv"))

###########################
# Clean data
###########################

df_cr_1["week"] = "1"
df_cr_2["week"] = "2"
df_cr_3["week"] = "3"
df_cr_4["week"] = "4"

df_cr = pd.concat([df_cr_1,df_cr_2,df_cr_3,df_cr_4])
df_cr
df_cr['treat'] = np.where(df_cr['treat']==" ", ' Difference', df_cr['treat'])
df_cr


df_revenues_1["week"] = "1"
df_revenues_2["week"] = "2"
df_revenues_3["week"] = "3"
df_revenues_4["week"] = "4"

df_revenues = pd.concat([df_revenues_1,df_revenues_2,df_revenues_3,df_revenues_4])
df_revenues
df_revenues['treat'] = np.where(df_revenues['treat']==" ", ' Difference', df_revenues['treat'])
df_revenues

###########################
# Graph data
###########################

graph_cv = (ggplot(df_cr, aes(x = 'week', y='value', fill="treat", label="value"))
+ geom_bar(position = position_dodge(width = 0.9),stat="identity")   
+ geom_errorbar(aes(x = 'week', ymin="ymin", ymax="ymax"), width=.2, position = position_dodge(width = 0.9))
+ geom_text(format_string='{:.3f}', ha="left", va = "bottom", position = position_dodge(width = 0.9))
+ geom_hline(yintercept = 0) # add one horizonal line
+ ylab("Percent")
+ facet_wrap('~type',scales="free")
+ theme(
        legend_title=element_blank(),
        legend_position="bottom",
        axis_title_x = element_blank(),
        subplots_adjust={'wspace':0.25}
        )
)
        
graph_cv
ggsave(plot = graph_cv, filename = "graph_cr_week.pdf", path = os.path.join(main_dir,graphs), width = 10, height = 4)

graph_revenues = (ggplot(df_revenues, aes(x = 'week', y = "value", fill="treat", label = "value"))
+ geom_bar(stat="identity", position = position_dodge(width = 0.9))   
+ geom_text(format_string='{:.2f}', va="bottom", position = position_dodge(width = 0.9))
+ facet_wrap('~type',scales="free")
+ ylab("Revenues (1000s)")
+ xlab("Weeks")
+ theme(
        legend_title=element_blank(),
        # axis_title_x = element_blank(),
        subplots_adjust={'wspace':0.25},
        legend_position = "bottom",
        legend_margin=10
        )
)
   
graph_revenues

ggsave(plot = graph_revenues, filename = "graph_revenues_week.pdf", path = os.path.join(main_dir,graphs), width = 10, height = 4)
