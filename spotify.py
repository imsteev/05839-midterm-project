import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

class Spotify(object):
    POSITION_SCATTER_LAYOUT = {
        'title': 'Song Position Scatterplot',
        'yaxis': {
            'autotick': False,
            'ticks': '',
            'tick0': 0,
            'dtick': 20,
            'ticklen': 200,
            'tickcolor': '#000',
            'title': 'Position'
        },
        'margin': {
            'l':200
        },
        'shapes' : [
            {
                'type': 'rect',
                'x0': '2017-01-01',
                'y0': 0,
                'x1': '2018-01-01',
                'y1': 50,
                'fillcolor': 'green',
                'opacity': 0.2,
                'line': {
                    'width': 0
                }  
            },
            {
                'type': 'rect',
                'x0': '2017-01-01',
                'y0': 50,
                'x1': '2018-01-01',
                'y1': 100,
                'fillcolor': 'yellow',
                'opacity': 0.2,
                'line': {
                    'width': 0
                }  
            },
            {
                'type': 'rect',
                'x0': '2017-01-01',
                'y0': 100,
                'x1': '2018-01-01',
                'y1': 200,
                'fillcolor': 'red',
                'opacity': 0.2,
                'line': {
                    'width': 0
                }
            }
        ]
    }

    POSITION_DIFF_LAYOUT = {
        'title':'Song Position Differences',
        'yaxis': {
            'autotick': False,
            'ticks': '',
            'tick0': 0,
            'dtick': 20,
            'ticklen': 200,
            'tickcolor': '#000',
            'title': 'Position Difference From Previously Ranked Position'
        },
        'margin': {
            'l':200
        },
        'shapes' : [
            # highlight the region associated with top 10 songs
            {
                'type': 'rect',
                'x0': '2017-01-01',
                'y0': -20,
                'x1': '2018-01-01',
                'y1': +20,
                'fillcolor': 'green',
                'opacity': 0.2,
                'line': {
                    'width': 0
                }  
            },
            {
                'type': 'rect',
                'x0': '2017-01-01',
                'y0': 20,
                'x1': '2018-01-01',
                'y1': 200,
                'fillcolor': 'red',
                'opacity': 0.2,
                'line': {
                    'width': 0
                }  
            },
            {
                'type': 'rect',
                'x0': '2017-01-01',
                'y0': -20,
                'x1': '2018-01-01',
                'y1': -200,
                'fillcolor': 'red',
                'opacity': 0.2,
                'line': {
                    'width': 0
                }  
            }
        ]
    }

    POSITION_HEATMAP_LAYOUT = go.Layout(
        title='Song Position Heatmap',
        xaxis = dict(ticks='', nticks=12),
        yaxis = dict(ticks='' )
    )

    def __init__(self):
        plotly.offline.init_notebook_mode()
        with open ("./us_data_with_diffs.csv") as csvfile:
            self.df = pd.read_csv(csvfile)
        df = self.df
        name_and_artists = df[['Track Name','Artist']].drop_duplicates()
        self.all_songs = list(zip(name_and_artists['Track Name'], name_and_artists['Artist']))
        self.artists = { name : list(group['Track Name'].drop_duplicates()) for name, group in df.groupby('Artist')}

    def load_data(self):
        for song in self.all_songs:
            trackname = song[0]
            artist = song[1]
            song_df = df[(df['Track Name'] == trackname)&(df['Artist'] == artist)]
            position_diffs = song_df['Position'] - song_df.shift()['Position']
            df.loc[(df['Track Name'] == trackname)&(df['Artist']==artist), 'Position Diff'] = position_diffs

    def songs_at_position(self,position):
        df = self.df
        song_df = df[df['Position'] == position]
        song_df = song_df[['Track Name', 'Artist']].drop_duplicates()
        return list(zip(song_df['Track Name'],song_df['Artist']))

    def song_scatter_traces(self, attr, songs, fill='tozeroy', mode='linemode'):
        df = self.df
        traces = []
        for song in songs:
            trackname = song[0]
            artist = song[1]
            track = df[(df['Track Name'] == trackname) & (df['Artist'] == artist)]
            track_x = track['Date']
            track_y = track[attr]
            trace = go.Scatter(
                x = track_x,
                y = track_y,
                mode = mode,
                name = trackname
            )
            traces.append(trace)
        return traces

    def song_box_traces(self, attr, songs):
        df = self.df
        traces = []
        for song in songs:
            trackname = song[0]
            artist = song[1]
            trace = go.Box(
                x = df[(df['Track Name'] == trackname)&(df['Artist'] == artist)][attr],
                name = trackname
            )
            traces.append(trace)
        return traces

    def song_heatmap(self, attr, songs):
        df = self.df
        z = []
        date_list = np.array('2017-01-01', dtype=np.datetime64) + np.arange(365)
        for song in songs:
            trackname = song[0]
            artist = song[1]
            new_row = []
            song_df = df[(df['Track Name'] == trackname) & (df['Artist'] == artist)]
            for date in date_list:
                row = song_df[song_df['Date'] == str(date)]
                if row.empty:
                    new_row.append(None)
                else:
                    new_row.append(int(row[attr]))
            z.append(new_row[:])

        result = go.Heatmap(
                z=z,
                x=date_list,
                y=[song[0] for song in songs],
                colorscale=[ # https://plot.ly/python/colorscales/
                    [0.0, 'rgb(165,0,38)'], 
                    [0.1111111111111111, 'rgb(215,48,39)'], 
                    [0.2222222222222222, 'rgb(244,109,67)'],
                    [0.3333333333333333, 'rgb(253,174,97)'], 
                    [0.4444444444444444, 'rgb(254,224,144)'], 
                    [0.5555555555555556, 'rgb(224,243,248)'],
                    [0.6666666666666666, 'rgb(171,217,233)'],
                    [0.7777777777777778, 'rgb(116,173,209)'], 
                    [0.8888888888888888, 'rgb(69,117,180)'],
                    [1.0, 'rgb(49,54,149)']
                ],
                colorbar = dict(
                    title = 'Song %s' % attr,
                    titleside = 'top',
                    tickvals = [step for step in range(0,211,20)],
                    ticktext = [str(step) for step in range(0,211,20)],
                    ticks = 'outside'
                )
            )
        return result

    def create_scatter(self, attr, songs, layout):
        df = self.df
        data = self.song_scatter_traces(attr, songs)
        fig = go.Figure(data=data, layout=layout)
        plot_div = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def create_heatmap(self,attr,songs,layout):
        df = self.df
        data = [self.song_heatmap(attr, songs)]
        fig = go.Figure(data=data, layout=layout)
        plot_div = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    
    def create_boxplots(self, attr, songs):
        layout = {
            'title':'Song Position Boxplots',
            'yaxis': {
                'autotick': False,
                'ticks': '',
                'tick0': 0,
                'dtick': 20,
                'ticklen': 200,
                'tickcolor': '#000'
            },
            'xaxis': {
                'title': 'Song Position'
            }
        }
        fig = go.Figure(data=self.song_box_traces(attr, songs),layout=layout)
        plot_div = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    
    def count_days_in(self, attr, songs):
        df = self.df
        result = { "%s by %s" %  (trackname,artist) : { (x*20) : 0 for x in range(1,10) } for (trackname,artist) in songs }
        for song in songs:
            trackname = song[0]
            artist = song[1]
            song_df = df[(df['Track Name'] == trackname)&(df['Artist'] == artist)]
            for topX in range(1,10):
                start = (topX-1) * 20
                end = topX * 20
                count_in_range = len(song_df[(song_df['Position'].astype(int)>=start)&(song_df['Position'].astype(int)<end)])
                result["%s by %s" %(trackname,artist)][end] += count_in_range
        return result
    
    def create_barchart(self, attr, songs):
        df = self.df
        topX = self.count_days_in("Position", songs)
        traces = []
        for i in range(1,10):
            trace = go.Bar(
                x = [title for title in topX],
                y = [topX[title][20*i] for title in topX],
                name = "%d-%d" % (20*(i-1),20*i-1)
            )
            traces.append(trace)
        layout = {
            'barmode': 'stack',
            'yaxis': {
                'autotick': False,
                'ticks': '',
                'tick0': 0,
                'dtick': 20,
                'ticklen': 200,
                'tickcolor': '#000',
                'title':'Days in Position'
            }
        }
        fig = go.Figure(data=traces, layout=layout)
        plot_div = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    



