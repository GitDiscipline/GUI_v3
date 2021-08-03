import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
##from sklearn.multioutput import MultiOutputRegressor


##for chunk in pd.read_csv("input18800000.csv", chunksize=50000):
##    a=chunk
##    break



a=pd.read_csv("input0.csv")
a.columns=['INDEX', 'Time', 'V-INV', 'V-INT', 'V-ICV', 'V-ICT', 'V-TCV', 'V-TCT',
       'V-MRV', 'V-B1V', 'V-B2V', 'V-B3V', 'V-B5V', 'V-HCV', 'NH_Speed',
       'NL_Speed']
a=a.drop(0)

a=a.reset_index()

a=a.drop(['index', 'INDEX', 'Time'], axis = 1)



from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test= train_test_split(a[['V-INV','V-INT','V-TCV','V-TCT','V-HCV']],a[[ 'V-ICV', 'V-ICT',  
       'V-MRV','V-B1V','V-B2V', 'V-B3V', 'V-B5V']], test_size=0.3, random_state=109)




##from sklearn.svm import SVR
##
##
##svclassifier = SVR(kernel='rbf',C=1e4, gamma=0.1)
##mor = MultiOutputRegressor(svclassifier)
##svm_model= mor.fit(x_train, y_train)
##
##y_pred = mor.predict(x_test)


from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(random_state = 109)
tree_model=regressor.fit(x_train, y_train)
y_pred = tree_model.predict(x_test)


#y_test= y_test.to_numpy()
y_test=np.asfarray(y_test,float)


#x_test= x_test.to_numpy()
x_test=np.asfarray(x_test,float)


#y_pred= y_pred.to_numpy()
y_pred=np.asfarray(y_pred,float)


y_train=np.asfarray(y_train,float)





from sklearn.neural_network import MLPRegressor
regr = MLPRegressor(random_state=1,activation='relu',solver='adam',hidden_layer_sizes=(6,10))
regr.fit(x_train, y_train)
y_pred2 = regr.predict(x_test)


y_pred2=np.asfarray(y_pred2,float)













pickle_out= open("sensor.pkl", "wb")
pickle.dump(tree_model, pickle_out)
pickle_out.close()


pickle_out2= open("sensor2.pkl", "wb")
pickle.dump(regr, pickle_out2)
pickle_out2.close()








