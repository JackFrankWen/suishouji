from flask import Flask,render_template

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

app.run(debug=True)
