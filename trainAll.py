import pandas as pd
df=pd.read_csv("kidney_disease.csv")

#null remove
print(df.isnull().sum())
df=df.dropna()
print(df.isnull().sum())

#drop colum
df=df.drop(['id'],axis=1)

#Label encoding
category_colums=['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane']
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
df[category_colums] = df[category_colums].apply(encoder.fit_transform)

#data type
print(df.dtypes)
df.pcv=df.pcv.astype('float')
df.wc=df.wc.astype('float')
df.rc=df.rc.astype('float')
print(df.dtypes)

#data label 
X=df.iloc[:,:24]
y=df.iloc[:,24]

#array convert
X=X.to_numpy()
y=y.to_numpy()

#split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

import warnings
warnings.filterwarnings("ignore")
names = ["K-Nearest Neighbors", "SVM",
         "Decision Tree", "Random Forest",
         "Naive Bayes","ExtraTreesClassifier","VotingClassifier"]

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import VotingClassifier

classifiers = [
    KNeighborsClassifier(),
    LinearSVC(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    GaussianNB(),
    ExtraTreesClassifier(),
    VotingClassifier(estimators=[('DT', DecisionTreeClassifier()), ('rf', RandomForestClassifier()), ('et', ExtraTreesClassifier())], voting='hard')]

clfF=[]
for name, clf in zip(names, classifiers):
    clf.fit(X_train, y_train)
    y_pred=clf.predict(X_test)
    print(name)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print('--------------------------------------------------------------')
    clfF.append(clf)

import pickle
pickle.dump(clfF, open("model.pkl",'wb'))
pickle.dump(encoder, open("encoder.pkl",'wb'))    
    
    
    
    
    
    
    
    
    
    
    