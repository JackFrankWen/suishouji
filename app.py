from flask import Flask, render_template, request, redirect, url_for
import os
from flask_cors import CORS


app = Flask(__name__,
            static_folder = 'web/static',
            template_folder = 'web/templates'
    )
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/transaction')
def flow():
     return render_template('transaction.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file:
            filename = 'abc.csv'
            print(request.files['file'])
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded successfully'
    return 'sssssssssss'
@app.route("/me", methods=['POST'])
def me_api():
    return {
        "username": "username",
        "theme": "username",
        "image": "username",
    }

app.run(debug=True)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
