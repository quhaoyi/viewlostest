from flask import Flask, render_template, request
app = Flask(__name__, static_folder='./styles')

@app.route("/")
@app.route("/index")
@app.route("/back_to_home", methods=['POST'])
def home():
    return render_template("index.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    result = request.form
    return render_template("result.html",result = result)



if __name__ == '__main__':
    app.run()