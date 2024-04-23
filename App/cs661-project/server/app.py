from flask import Flask, request, send_file
from bnwordcloud.bn_wordcloud import main
from flask import jsonify
import json
from flask_cors import CORS, cross_origin
import os
from rhymeanalysis.pattern import calculate_entropy, top_author, author_histogram
from pos.pos import run_func

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/generate_wordcloud', methods=['GET'])
@cross_origin()
def generate_word_cloud():
    author = request.args.get('author')  # Get the singer name from the query parameters
    song = request.args.get('song')
    if not author:
        return "Error: Singer name is required.", 400
    
    # Call the generate_wordcloud function from wordcloud.py
    try:
        result = ''
        if song:
            result = main(author, song)
        else:
            result = main(author)
        # Assuming the word cloud is saved as "Bengali_word_cloud.png"
        print(result)
        return send_file(result, mimetype='image/png')
        # return result
    except Exception as e:
        return f"Error: {str(e)}", 500
    
    

@app.route('/data', methods=['GET'])
@cross_origin()
def send_data():
    with open('SongDBL.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/lyrics', methods=['GET'])
@cross_origin()
def send_lyrics():
    author = request.args.get('author')  # Get the singer name from the query parameters
    song = request.args.get('song')  # Get the song name from the query parameters

    with open('SongDB.json', 'r') as file:
        data = json.load(file)

    if not author:
        return "Error: Author name is required.", 400
    if not song:
        return "Error: Song name is required.", 400
    
    if author in data:
        for song_entry in data[author]:
            if song_entry["Song Name"] == song:
                return jsonify({"lyrics": song_entry["Lyrics"]})
        return jsonify({"error": "Song not found for the provided author"}), 404
    else:
        return jsonify({"error": "Author not found"}), 404
    
    
@app.route('/folders', methods=['GET'])
def get_folders():
    try:
        folders = [folder for folder in os.listdir('public') if os.path.isdir(os.path.join('public', folder))]
        return jsonify(folders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files/<folder_name>/<file_name>')
def get_file(folder_name, file_name):
    try:
        file_path = os.path.join('public', folder_name, file_name)
        return send_file(file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/files/<folder_name>', methods=['GET'])
def get_files(folder_name):
    try:
        files = [file for file in os.listdir(os.path.join('public', folder_name)) if os.path.isfile(os.path.join('public', folder_name, file))]
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/rhymepattern', methods=['GET'])
@cross_origin()
def rhyme_pattern():
    n_author = request.args.get('author_num')  # Get the singer name from the query parameters
    if not n_author:
        return "Error: Author Number is required.", 400
    try:
        result = ''
        result = calculate_entropy(n_author)
        return send_file(result, mimetype='image/png')
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/topauthor', methods=['GET'])
@cross_origin()
def call_top_author():
    try:
        result = ''
        result = top_author()
        return send_file(result, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/authorhist', methods=['GET'])
@cross_origin()
def author_hist():
    author = request.args.get('author')  # Get the singer name from the query parameters
    num_rhymes = request.args.get('num_rhymes')  # Get the singer name from the query parameters
    try:
        result = ''
        result = author_histogram(author, int(num_rhymes))
        return send_file(result, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/artistsimilarity', methods=['GET'])
def serve_artist_similarity():
    try:
        file_path = os.path.join('static', 'ArtistSimilarity.html')
        return send_file(file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/pos', methods=['GET'])
@cross_origin()
def call_pos():
    try:
        author = request.args.get('author')  # Get the singer name from the query parameters
        result = ''
        result = run_func(author)
        return send_file(result, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True)
