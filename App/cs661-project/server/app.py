from flask import Flask, request, send_file
from bnwordcloud.bn_wordcloud import generate_wordcloud

app = Flask(__name__)

@app.route('/generate_wordcloud', methods=['GET'])
def generate_word_cloud():
    singer = request.args.get('singer')  # Get the singer name from the query parameters
    if not singer:
        return "Error: Singer name is required.", 400
    
    # Call the generate_wordcloud function from wordcloud.py
    try:
        generate_wordcloud(singer)
        # Assuming the word cloud is saved as "Bengali_word_cloud.png"
        return send_file("Bengali_word_cloud.png", mimetype='image/png')
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
