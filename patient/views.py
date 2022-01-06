from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import pandas as pd


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from .models import DiabetesData


def home(request):
    return render(request,"index.html")

def login(request):
    if request.method == 'POST':
        #v = DoctorReg.objects.all()
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'data.html')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request,'login.html')
    else:
        return render(request, 'login.html')

def register(request):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is already exist')
                    return render(request, 'register.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email is already exist')
                    return render(request, 'register.html')
                else:

                    # save data in db
                    user = User.objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save();
                    print('user created')
                    return redirect('login')

            else:
                messages.info(request, 'Invalid Credentials')
                return render(request, 'register.html')
            return redirect('/')
        else:
            return render(request, 'register.html')

def predict(request):
        if (request.method == 'POST'):
            pregnancies = request.POST['pregnancies']
            glucose = request.POST['glucose']
            bloodpressure = request.POST['bloodpressure']
            skinthickness = request.POST['skinthickness']
            insulin = request.POST['insulin']
            bmi = request.POST['bmi']
            diabetespedigreefunction = request.POST['diabetespedigreefunction']
            age = request.POST['age']



            df = pd.read_csv(r"static/dataset/diabetes (1).csv")
            df.dropna(inplace=True)
            df.isnull().sum()
            X_train = df[['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']]
            y_train = df[['Outcome']]
            n = RandomForestClassifier()
            n.fit(X_train, y_train)
            prediction = n.predict(
                [[pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi,diabetespedigreefunction,age]])
            Diabetes = DiabetesData.objects.create(Pregnancies=pregnancies, Glucose=glucose, BloodPressure=bloodpressure, SkinThickness=skinthickness, Insulin=insulin, BMI=bmi, DiabetesPedigreeFunction=diabetespedigreefunction, Age=age)
            Diabetes.save()
            print("Predicted Value of Stock Prediction: ", prediction)

            return render(request, 'predict.html',
                          {"data": prediction, 'pregnancies': pregnancies, 'glucose': glucose,
                           'bloodpressure': bloodpressure, 'skinthickness': skinthickness, "insulin": insulin, 'bmi': bmi,
                           'diabetespedigreefunction': diabetespedigreefunction, 'age': age})


        else:
            return render(request, 'predict.html')

# Cre
