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

df_cr_d = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_cr_device_d.csv"))
df_cr_m = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_cr_device_m.csv"))
df_cr_t = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_cr_device_t.csv"))

df_revenues_d = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_revenues_device_d.csv"))
df_revenues_m = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_revenues_device_m.csv"))
df_revenues_t = pd.read_csv(os.path.join(main_dir,data_files,"ab_test_revenues_device_t.csv"))

###########################
# Clean data
###########################

df_cr_d["device"] = "D"
df_cr_m["device"] = "M"
df_cr_t["device"] = "T"

df_cr = pd.concat([df_cr_d,df_cr_m,df_cr_t])
df_cr
df_cr['treat'] = np.where(df_cr['treat']==" ", ' Difference', df_cr['treat'])
df_cr

df_revenues_d["device"] = "D"
df_revenues_m["device"] = "M"
df_revenues_t["device"] = "T"

df_revenues = pd.concat([df_revenues_d,df_revenues_m,df_revenues_t])
df_revenues
df_revenues['treat'] = np.where(df_revenues['treat']==" ", ' Difference', df_revenues['treat'])
df_revenues

###########################
# Graph data
###########################

graph_device = (ggplot(df_cr, aes(x = 'device', y='value', fill="treat", label="value"))
+ geom_bar(position = position_dodge(width = 0.9),stat="identity")   
+ geom_errorbar(aes(x = 'device', ymin="ymin", ymax="ymax"), width=.2, position = position_dodge(width = 0.9))
+ geom_text(format_string='{:.3f}', ha="left", position = position_dodge(width = 0.9))
+ geom_hline(yintercept = 0) # add one horizonal line
+ ylab("Percent")
+ facet_wrap('~type',scales="free")
+ theme(
        legend_title=element_blank(),
        legend_position="bottom",
        axis_title_x = element_blank(),
        subplots_adjust={'wspace':0.25},
        legend_margin=20
        )
)
        
graph_device
ggsave(plot = graph_device, filename = "graph_device_week.pdf", path = os.path.join(main_dir,graphs), width = 10, height = 4)


graph_revenues = (ggplot(df_revenues, aes(x = 'device', y = "value", fill="treat", label = "value"))
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

ggsave(plot = graph_revenues, filename = "graph_revenues_device.pdf", path = os.path.join(main_dir,graphs), width = 10, height = 4)
