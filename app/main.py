from flask import Flask, render_template, request
import pickle
import os
app = Flask(__name__, static_folder='./styles')

admitloc = {"EMERGENCY ROOM ADMIT": 0, "PHYS REFERRAL/NORMAL DELI": 1, "TRANSFER FROM HOSP/EXTRAM": 2, "CLINIC REFERRAL/PREMATURE": 3, "HMO REFERRAL/SICK": 4, "TRANSFER FROM OTHER HEALT": 5, "** INFO NOT AVAILABLE **": 6, "TRANSFER FROM SKILLED NUR": 7, "TRSF WITHIN THIS FACILITY": 8}
disloc = {"DISC-TRAN CANCER/CHLDRN H": 0, "HOME HEALTH CARE": 1, "HOME": 2, "REHAB/DISTINCT PART HOSP": 3, "LONG TERM CARE HOSPITAL": 4, "SNF": 5, "SHORT TERM HOSPITAL": 6, "HOME WITH HOME IV PROVIDR": 7, "LEFT AGAINST MEDICAL ADVI": 8, "DISCH-TRAN TO PSYCH HOSP": 9, "HOSPICE-HOME": 10, "HOSPICE-MEDICAL FACILITY": 11, "DISC-TRAN TO FEDERAL HC": 12, "OTHER FACILITY": 13, "ICF": 14}
maritalStatus = {"MARRIED": 0, "SINGLE": 1, "DIVORCED": 2, "WIDOWED": 3, "SEPARATED": 4, "LIFE PARTNER": 5, "UNKNOWN (DEFAULT)": 6}
@app.route("/")
@app.route("/index")
@app.route("/back_to_home", methods=['POST'])
def home():
    return render_template("index.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    result = request.form.to_dict()
    losRange = LOS_predict(result['name'], result['dob'], result['admittime'], result['test1'], result['test2'], result['test3'])
    invAdmit = {v: k for k, v in admitloc.items()}
    invDis = {v: k for k, v in disloc.items()}
    invmarry = {v: k for k, v in maritalStatus.items()}
    result['los1'] = round(losRange[0], 2)
    result['los2'] = round(losRange[1], 2)
    result['name'] = invAdmit[int(result['name'])]
    result['dob'] = invDis[int(result['dob'])]
    result['admittime'] = invmarry[int(result['admittime'])]
    return render_template("result.html",result = result)


def LOS_predict(ADMISSION_LOCATION, DISCHARGE_LOCATION, MARITAL_STATUS, AGE, Service_count, icu_LOS):
    fst_class = 0
    class_breakpoint = 30
    interval = 5
    variance = [3.8, 3.8, 6, 7.5, 8.2, 8.5]

    feature = [ADMISSION_LOCATION, DISCHARGE_LOCATION, MARITAL_STATUS, AGE, Service_count, icu_LOS]
    feature_list = [feature]
    svm_model = pickle.load(open(os.path.join(app.static_folder, 'svm_model'),'rb'))
    svr_model = pickle.load(open(os.path.join(app.static_folder, 'svr_model'),'rb'))
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