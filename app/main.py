from flask import Flask, render_template, request
import pickle
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


def LOS_predict(ADMISSION_LOCATION, DISCHARGE_LOCATION, MARITAL_STATUS, AGE, Service_count, icu_LOS):
    fst_class = 0
    class_breakpoint = 30
    interval = 5
    variance = [4, 4, 4, 4, 7, 7]

    feature = [ADMISSION_LOCATION, DISCHARGE_LOCATION, MARITAL_STATUS, AGE, Service_count, icu_LOS]
    feature_list = [feature]
    svm_model = pickle.load(open("model/svm_model",'rb'))
    svr_model = pickle.load(open("model/svr_model",'rb'))
    class_pred = svm_model.predict(feature_list)
    if class_pred[0] == fst_class:
        value_pred_lst = svr_model.predict(feature_list)
    else:
        return [class_breakpoint, 200]
    value_pred = value_pred_lst[0]
    count = 0
    for i in range(0, class_breakpoint, interval):
        if value_pred >= i and value_pred <= i+interval:
            return [value_pred, value_pred+variance[count]]
        count += 1


if __name__ == '__main__':
    app.run()