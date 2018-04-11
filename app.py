from flask import Flask, render_template, url_for, request, redirect, Markup
from datetime import datetime
from spotify import Spotify

app = Flask(__name__, static_url_path='/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
S = Spotify()
selected_songs = []

@app.route('/')
def homepage():
    position_scatter = False
    position_heatmap = False
    position_boxplots = False
    position_diff_scatter = False
    position_bar = False
    if len(selected_songs) > 0:
        position_scatter = Markup(S.create_scatter("Position", selected_songs, Spotify.POSITION_SCATTER_LAYOUT))
        position_diff_scatter = Markup(S.create_scatter("Position Diff", selected_songs, Spotify.POSITION_DIFF_LAYOUT))
        position_heatmap = Markup(S.create_heatmap("Position", selected_songs, Spotify.POSITION_HEATMAP_LAYOUT))
        position_boxplots = Markup(S.create_boxplots("Position", selected_songs))
        position_bar = Markup(S.create_barchart("Position", selected_songs))

    print(selected_songs)
    return render_template("index.html", 
                            all_songs=S.all_songs, 
                            artists=S.artists,
                            selected_songs=selected_songs, 
                            pos_scatter=position_scatter, 
                            diff_scatter=position_diff_scatter,
                            bar=position_bar,
                            heatmap=position_heatmap,
                            boxplot=position_boxplots)

@app.route('/loaddata')
def load_data():
    S.load_data()
    return redirect(url_for('homepage'))

@app.route('/selectsongs', methods=['POST'])
def select_songs():
    global selected_songs
    new_songs = []
    for key in request.form:
        song = request.form[key]
        trackname = song.split("---")[0]
        artist = song.split("---")[1]
        new_songs.append(tuple((trackname, artist)))
    selected_songs = new_songs
    return redirect(url_for('homepage'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(use_reloader=True)  