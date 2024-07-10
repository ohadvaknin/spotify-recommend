from flask import Flask, render_template, request
from artist_recommender import get_recommendations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommended_artists = []
    if request.method == 'POST':
        artist1 = request.form['artist1']
        artist2 = request.form['artist2']
        artist3 = request.form['artist3']
        
        recommended_artists = get_recommendations(artist1, artist2, artist3)
    
    return render_template('index.html', recommended_artists=recommended_artists)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
