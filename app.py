from flask import Flask, render_template, request
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
        print(request.files['file'])
        f = request.files['file']
        # data_xls = pd.read_excel(f)
        # return data_xls.to_html()
@app.route("/me", methods=['POST'])
def me_api():
    return {
        "username": "username",
        "theme": "username",
        "image": "username",
    }

app.run(debug=True)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
