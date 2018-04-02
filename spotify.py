import numpy as np
import pandas as pd

# dataset from https://www.kaggle.com/edumucelli/spotifys-worldwide-daily-song-ranking/data
def create_region_csv(region):
    with open("./data.csv") as csvfile:
        df = pd.read_csv(csvfile)
        g = df.groupby('Region')
        region_df = g.get_group(region)
        filename = "./%s_data.csv" % region
        with open(filename, "w") as csvtosave:
            region_df.to_csv(csvtosave, index=False, columns=['Position', 'Track Name', 'Artist', 'Streams', 'Date'])

# create_region_csv('us')

# Other data to extract: jumps above and below current spot. 
# http://bl.ocks.org/wpoely86/e285b8e4c7b84710e463
with open ("./us_data.csv") as csvfile:
    df = pd.read_csv(csvfile)

date_list = np.array('2017-01-01', dtype=np.datetime64) + np.arange(365)
print(date_list.to)
# song_dfs = []

# for track_name in df['Track Name'].unique():
#     song_df = df[df['Track Name'] == track_name]
#     df.loc[df['Track Name'] == track_name, 'Position Diff'] = song_df['Position'] - song_df.shift()['Position']