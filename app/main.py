from flask import Flask, render_template, request
from LOSpredict import LOS_predict
app = Flask(__name__, static_folder='./styles')

@app.route("/")
@app.route("/index")
@app.route("/back_to_home", methods=['POST'])
def home():
    return render_template("index.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    result = request.form.to_dict()
    losRange = LOS_predict(result['name'], result['dob'], result['admittime'], result['test1'], result['test2'], result['test3'])
    result['los1'] = round(losRange[0], 2)
    result['los2'] = round(losRange[1], 2)
    return render_template("result.html",result = result)



if __name__ == '__main__':
    app.run()