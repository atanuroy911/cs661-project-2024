from flask import Flask, request, send_file
from bnwordcloud.bn_wordcloud import main
from flask import jsonify
import json
from flask_cors import CORS, cross_origin

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

if __name__ == '__main__':
    app.run(debug=True)
