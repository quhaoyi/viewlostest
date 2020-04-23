'''
input: feature = [ADMISSION_LOCATION, DISCHARGE_LOCATION, MARITAL_STATUS, AGE, Service_count, icu_LOS]
the model first classifies the feature as in [0, 30] (class=0) or [30, -] (class=1) by SVM, acc > 97%
then estimate LOS with a SVR model
the model usually under estimates LOS by a variance
output: a predicted range of LOS
usage: LOS_predict(3,6,6,0,1,0.15480)
       => [1.4679578800359927, 5.467957880035993]
'''
import pickle
def LOS_predict(ADMISSION_LOCATION, DISCHARGE_LOCATION, MARITAL_STATUS, AGE, Service_count, icu_LOS):
    fst_class = 0
    class_breakpoint = 30
    interval = 5
    variance = [3.8, 3.8, 6, 7.5, 8.2, 8.5]

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
