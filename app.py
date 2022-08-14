import re
import os
from flask import Flask, render_template, url_for, request
from textgrab.textgrab import word_count_dict

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    # return 'hello world'
    if request.method == 'POST':
        print(os.getcwd())
        url = request.form['content']
        status, word_agg = word_count_dict(url)
        return render_template('index.html', url=url, status=status, word_agg=word_agg)
    else:
        status = True
        url = None
    return render_template('index.html', status=status, url=url)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, port=port, host="0.0.0.0")