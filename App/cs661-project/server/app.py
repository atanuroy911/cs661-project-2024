from flask import Flask, request, send_file
from bnwordcloud.bn_wordcloud import main

app = Flask(__name__)

@app.route('/generate_wordcloud', methods=['GET'])
def generate_word_cloud():
    singer = request.args.get('singer')  # Get the singer name from the query parameters
    if not singer:
        return "Error: Singer name is required.", 400
    
    # Call the generate_wordcloud function from wordcloud.py
    try:
        result = main(singer)
        # Assuming the word cloud is saved as "Bengali_word_cloud.png"
        print(result)
        return send_file(result, mimetype='image/png')
        # return result
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
