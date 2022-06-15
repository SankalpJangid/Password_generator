from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from matplotlib.style import context
from pass_gen.models import UserDetails,UserPasswords
import random

# Machine Learning Packages
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier




def register(request):
    return render(request,'register1.html')

def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone_no = request.POST.get('number')
        date = request.POST.get('date')
        Password1 = request.POST.get('password1')
        Password2 = request.POST.get('password2')
        if Password1 != Password2:
            messages.error(request,"Your password not match")
            return redirect('register')
        myuser = User.objects.create_user(username,email,Password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.phone_no = phone_no
        myuser.save()
        data = UserDetails()
        data.first_name = fname
        data.username = username
        data.last_name = lname
        data.phone_no = phone_no
        data.email = email
        data.date_of_birth = date
        data.user = myuser
        data.save()
        messages.success(request,"user successfully created")
        return redirect('/login')
    else:
        return HttpResponse("404 error")


def login_1(request):
    return render(request,'login1.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('login_n')
        password = request.POST.get('login_p')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"user successfully login")
            return redirect("/")
        else:
            messages.error(request,"Invalid credentials")
            return redirect("/login")
        
    else:
        return HttpResponse("404 error")


@login_required(login_url="login")
def home(request):
    log_user = request.user
    all_data = UserDetails.objects.get(user=log_user)
    name = str(all_data.first_name)
    stored_pass = UserPasswords.objects.filter(username=name)
    print(len(stored_pass))
    context = {'mydict':stored_pass,'length':len(stored_pass)}
    return render(request,'home.html',context)


def logout_user(request):
    logout(request)
    messages.success(request,"user successfully logout")
    return redirect("/")


def generate(request):
    log_user = request.user
    all_data = UserDetails.objects.get(user=log_user)
    symbols = ['!','@','#','$','%','^','&','*','(',')','-','_','+','=','[',']','{','}','|','?','<','>']
    new_pass = ""
    dt = str(all_data.date_of_birth)
    for i in range(2):
        new_pass += random.choice(str(all_data.first_name))
        new_pass += random.choice(str(all_data.last_name))
        new_pass += random.choice(str(all_data.phone_no))
        new_pass += random.choice(str(all_data.email))
        new_pass += random.choice(dt)
        new_pass += random.choice(symbols)

    print(new_pass)
    l = list(new_pass)
    random.shuffle(l)
    result = "".join(l)

    name = str(all_data.first_name)
    stored_pass = UserPasswords.objects.filter(username=name)
    print(len(stored_pass))
    context = {'result':result,'mydict':stored_pass,'length':len(stored_pass)}
    return render(request,'home.html',context)


def save_passwords(request):
    suser = request.user
    all_data = UserDetails.objects.get(user=suser)
    name = str(all_data.first_name)
    if request.method == "POST":
        site_name = request.POST.get('site')
        pass_ = request.POST.get('pass')
        data = UserPasswords()
        data.username = name
        data.password = pass_
        data.for_site = site_name
        data.save()
        return redirect("/")
    return redirect("/")

        

def delete_pass(request,id):
    data = UserPasswords.objects.get(sno=id)
    data.delete()
    return redirect("/")


def update_pass(request,id):
    data = UserPasswords.objects.get(sno=id)
    s = data.for_site
    p = data.password
    context = {'name':s,'pass':p, 'id':id}
    return render(request,"update.html", context)

def change_data(request):
    if request.method == "POST":
        data_id = request.POST.get('data_id')
        data_name = request.POST.get('change_name')
        data_pass = request.POST.get('change_pass')
        data = UserPasswords.objects.get(sno=data_id)
        data.for_site = data_name
        data.password = data_pass
        data.save()
        return redirect("/")
    return redirect("/")




def sample_model(request):
    pswd_data = pd.read_csv("paswword_strenght.csv", error_bad_lines=False)
    pswd = np.array(pswd_data)
    random.shuffle(pswd)
    ylabels  = [s[1] for s in pswd]
    allpasswords = [s[0] for s in pswd]
    def makeTokens(f):
        tokens = []
        for i in f:
            tokens.append(i)
        return tokens
    vectorizer = TfidfVectorizer(tokenizer=makeTokens)
    X = vectorizer.fit_transform(allpasswords)
    X_train, X_test, y_train, y_test = train_test_split(X, ylabels, test_size=0.2)	
    dt = DecisionTreeClassifier()
    dt.fit(X_train,y_train)
    if request.method == "POST":
        print("good")
        site_name = request.POST.get('check_password')
        print(site_name)
        sample_1 = [site_name]
        X_predict11 = vectorizer.transform(sample_1)
        y_Predict11 = dt.predict(X_predict11)
        print(y_Predict11)
        result = ""
        if(y_Predict11[0] == "0"):
            result = "Weak"
        elif(y_Predict11[0] == "1"):
            result = "Medium"
        elif(y_Predict11[0] == "2"):
            result = "Hard"
        context = {'predict':result}
        return render(request,'check.html',context)
    return redirect("/")


def check(request):
    return render(request,'check.html')


def search(request):
    query = request.GET['search']
    
    if len(query) == 0:
        alltask = UserPasswords.objects.none()
    elif len(query) > 70:
        alltask = UserPasswords.objects.none()
    else:
        loginuser = request.user
        all_data = UserDetails.objects.get(user=loginuser)
        name = str(all_data.first_name)
        stored_pass = UserPasswords.objects.filter(username=name)
        allsite = stored_pass.filter(for_site__contains=query)
        allpass = stored_pass.filter(password__contains=query)
        alltask = allsite.union(allpass)
 
    if alltask.count() == 0:
        messages.warning(request,"No result found.Please check The spelling correctly.")

    context = {'alltask':alltask, 'query':query}
    return render(request,'search.html',context)