import pandas as pd
import numpy as np

dataframe   = ({
        'id':[1, 1, 1, 1,
              2, 2, 2, 2,
              3, 3, 3, 3,
              4, 4, 4, 4],
        'month' :[1, 2, 3, 4,
                  1, 2, 3, 4,
                  1, 2, 3, 4,
                  1, 2, 3, 4],
        'income':[100, 110, 120, 130,
                  200, 210, 220, 230,
                  90, 100, 110, 120,
                  180, 190, 200, 210]
})

df = pd.DataFrame(dataframe, columns=['id','month','income'])
df = df.sort_values(by=['id',"month"])
df

# within group, subtract lagged value 
df["diff"] = df.groupby(['id'])['income'].transform(pd.Series.diff)
df
