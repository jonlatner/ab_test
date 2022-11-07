df_sessions = df.groupby(['treat'])[["sessions"]].sum().reset_index()
df_sessions["sessions"]=df_sessions["sessions"]/1000
df_sessions["type"]=" sessions (1000s)"
df_sessions = df_sessions.rename(columns={"sessions":"value"})
df_sessions

data = {"treat":[" "],
        'value': df_sessions["value"][1]-df_sessions["value"][0],
        'type': ["Difference (T-C)"]
}

df_diff = pd.DataFrame(data)
df_diff
df_sessions = pd.concat([df_sessions,df_diff])
df_sessions
df_sessions["type"].value_counts(dropna=False).sort_index()

graph_sessions = (ggplot(df_sessions, aes(x = 'treat', y = "value", label = "value"))
                  + geom_bar(stat="identity")   
                  # + ylim(0,4000)
                  + geom_text(nudge_y=-0.5, 
                              format_string='{:.2f}', va="bottom")   
                  + facet_wrap('~type',scales="free")
                  + ylab("sessions (1000s)")
                  + theme(
                          axis_title_x = element_blank(),
                          subplots_adjust={'wspace':0.25}
                  )
)

graph_sessions
