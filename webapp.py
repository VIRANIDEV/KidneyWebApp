import streamlit as st
import re
import sqlite3 
import pickle
import pandas as pd


conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()


menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.subheader("Welcome To Chronic kidney disease (CKD) Prediction System")
    st.image('Home.jpg')
    
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            if Email=='a@a.com' and Password=='123':
                st.success("Logged In as {}".format("Admin"))
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
            else:
                result = login_user(Email,Password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["K-Nearest Neighbors", "SVM",
                             "Decision Tree", "Random Forest",
                             "Naive Bayes","ExtraTreesClassifier","VotingClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)

                    age=float(st.slider('age Value', 0, 90))
                    bp=float(st.slider('BP Value', 50, 110))
                    sg=float(st.slider('SG Value', 1.0, 1.5))
                    al=float(st.slider('al Value', 0.0, 4.0))
                    su=float(st.slider('su Value', 0.0, 5.0))
                    rbc1 = ["normal", "abnormal"]
                    rbc=st.selectbox("Select rbc",rbc1)
                    pc1 = ["normal", "abnormal"]
                    pc=st.selectbox("Select pc",pc1)
                    pcc1 = ["present", "notpresent"]
                    pcc=st.selectbox("Select pcc",pcc1)
                    ba1 = ["present", "notpresent"]
                    ba=st.selectbox("Select ba",ba1)
                    bgr=float(st.slider('bgr Value', 70.0, 490.0))
                    bu=float(st.slider('bu Value', 10.0, 309.0))
                    sc=float(st.slider('sc Value', 0.4, 15.2))
                    sod=float(st.slider('sod Value', 111.0, 115.0))
                    pot=float(st.slider('pot Value', 2.5, 47.0))
                    hemo=float(st.slider('hemo Value', 3.1, 17.8))
                    pcv=float(st.slider('pcv Value', 9.0, 54.0))
                    wc=float(st.slider('wc Value', 3800.0, 26400.0))
                    rc=float(st.slider('rc Value', 2.1, 8.0))
                    htn1 = ["yes", "no"]
                    htn=st.selectbox("Select htn",htn1)
                    dm1 = ["yes", "no"]
                    dm=st.selectbox("Select dm",dm1)
                    cad1 = ["yes", "no"]
                    cad=st.selectbox("Select cad",cad1)
                    appet1= ["poor", "good"]
                    appet=st.selectbox("Select appet",appet1)
                    pe1 = ["yes", "no"]
                    pe=st.selectbox("Select pe",pe1)
                    ane1 = ["yes", "no"]
                    ane=st.selectbox("Select ane",ane1)
                    my_array=[age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu,
                           sc, sod, pot, hemo, pcv, wc, rc, htn, dm, cad,
                           appet, pe, ane] 
                    
                    b2=st.button("Predict")
                    model=pickle.load(open("model.pkl",'rb'))
                                           
                    if b2:                        
                        df = pd.DataFrame([my_array], 
                                          columns=['age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr', 'bu',
                                                 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 'htn', 'dm', 'cad',
                                                 'appet', 'pe', 'ane'])
                        category_colums=['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane']
                        encoder=pickle.load(open("encoder.pkl",'rb'))
                        df[category_colums] = df[category_colums].apply(encoder.fit_transform)
                        tdata=df.to_numpy()
                        #st.write(tdata)
                        if choice2=="K-Nearest Neighbors":
                            test_prediction = model[0].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="SVM":
                            test_prediction = model[1].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)                 
                        if choice2=="Decision Tree":
                            test_prediction = model[2].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="Random Forest":
                            test_prediction = model[3].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="Naive Bayes":
                            test_prediction = model[4].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="ExtraTreesClassifier":
                            test_prediction = model[5].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="VotingClassifier":
                            test_prediction = model[6].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                            
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
                
           
if choice=="SignUp":
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password",type="password")
    CPassword = st.text_input("Confirm Password",type="password")
    b2=st.button("SignUp")
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==CPassword:
            if (pattern.match(Mname)):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
            
        

    