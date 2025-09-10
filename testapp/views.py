from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from examapp.models import Question
from testapp.models import MyUser


# Create your views here.


def giveMePage1(request):
    return render(request,'testapp/addition.html')


def nextQuestion(request):
    if 'op' in request.GET:
        allanswers = request.session.get('answers', {})
        allanswers[request.GET['qno']] = [
            request.GET['qno'],
            request.GET['qtext'],
            request.GET['answer'],
            request.GET['op']
        ]
        request.session['answers'] = allanswers  # save back to session

    queryset = Question.objects.filter(subject=request.session['subject'])
    allquestions = list(queryset)

    index = request.session.get('questionindex', 0)

    # check if not last question
    if index < len(allquestions) - 1:
        index += 1
        request.session['questionindex'] = index

    question = allquestions[index]

    # Disable Next button if last question
    isdisabled = (index == len(allquestions) - 1)

    return render(request, 'question.html', {
        'question': question,
        'isdisabled': isdisabled,
        'previousanswer': request.session.get('answers', {}).get(str(question.qno), [None, None, None, None])[3],
        'message': ''
    })


# 0  1  2
def previousQuestion(request):
    
    if 'op' in request.GET:

        allanswers=request.session['answers'] # {}

        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]

        print(allanswers)


    #allquestions=Question.objects.all()
    
    queryset=Question.objects.filter(subject=request.session['subject'])
    allquestions=list(queryset)

    if request.session['questionindex']>0:

        request.session['questionindex']=request.session['questionindex'] - 1 

        question=allquestions[request.session['questionindex']]
        
        qno=question.qno

        submitteddetails=request.session['answers']

        print(f"submitted answers are  {submitteddetails}")

        if str(qno) in submitteddetails:
            questiondetails=submitteddetails[str(qno)]
            previousanswer=questiondetails[3]
            print(f"previousanswer is {previousanswer}")
        else:
            previousanswer=''

        return render(request,'question.html',{'question':question,'previousanswer':previousanswer})


    else:
        return render(request,'question.html',{'question':allquestions[0]})



def endexam(request):
            
    if 'answers' in request.session:

        if 'op' in request.GET:

            allanswers=request.session['answers'] # {}

            allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]

            print(f"inside if {allanswers}")

        dictionary=request.session['answers'] 
        
        listoflist=dictionary.values()

        print(listoflist)

        print(f"dictionary in endexam button is {dictionary}")

        for list in listoflist:
            
            if list[2]==list[3]:
                request.session['score']=request.session['score']+1
        
        finalscore=request.session['score']

        username=request.session["username"]

        auth.logout(request) # remove all keys from session dictionary

        return render(request,'score.html',{'username':username,'score': finalscore, 'listoflist':listoflist})
    
    else:
        messages.info(request,"login again")
        return render(request,'login.html')


    #[ [1,'what is 1+1?',2,2] , [2,'what is 2+2?',4,6] , [3,'what is 3+3?',6,3]  ]

    # {1:[1,'what is 1+1?',2,2] , 2:[2,'what is 2+2?',4,6],3:[3,'what is 3+3?',6,3]}

def main_view(request):
    return render(request, 'testapp/main.html')

# localhost:8000/signup
def signup(request):
    if request.method=="GET":
        
        return render(request,'testapp/signup.html')

    photo=request.FILES['photo']
    imagepath='/upload/'+photo.name

    with open('testapp/static/upload/'+photo.name, 'wb+') as destination:  
                for byte in photo.chunks():  
                    destination.write(byte)
   
    MyUser.objects.create_user(username=request.POST["username"] , email=request.POST["email"],password=request.POST["password"],imagepath=imagepath)

    #userobject.save() # save() will save user's details in auth_user table .

    print(connection.queries)

    return render(request,'testapp/login.html',{'message':"registration successful"})
    
    # if request.method=='POST':
    #     fn=request.POST.get('first_name')
    #     ln=request.POST.get('last_name')
    #     un=request.POST.get('username')
    #     email=request.POST.get('email')
    #     pass1=request.POST.get('password1')
    #     pass2=request.POST.get('password2')
    #     if pass1==pass2:
    #         if User.objects.filter(username=un).exists():
    #          messages.error(request,'user name already exists')
    #          return redirect('/signup')
                
    #         else:
    #             if User.objects.filter(email=email).exists():
    #                 messages.error(request,'already have email')
    #                 return redirect('/signup')
    #             else:
    #                 user=User.objects.create_user(username=un,password=pass1,first_name=fn,last_name=ln)
    #                 user.save()
    #                 messages.info(request,'sign up successfully')
    #                 return redirect('/login')
            
        
    #     else:
    #         messages.error(request,'password not match')
    #         return redirect('/signup')

    # return render(request,'testapp/signup.html')

# request ==> [ POST {username=x  password=y }  , session={username:'x'} ] request object
#   employee ==> [ eid=1 name='sachin' ] Employee object

# def login(request):

#     # if request.method=='POST':

#     #     username=request.POST.get('username')
#     #     password=request.POST["password"]

#     #     print(username,password)

#     #     user=auth.authenticate(username=username,password=password)

#     #     print(connection.queries)

#     #     print(user)

#     #     if user is not None:

#     #         auth.login(request,user)
            
#     #         request.session['questionindex']=0 # add questionindex in session dictionary

#     #         # [questionindex=0] session dictionary

#     #         request.session['answers']={}
#     #         request.session['score']=0
#     #         request.session["username"]=username
        
#     #         messages.success(request,'login successfully')
            
#     #         return render(request,'examapp/subject.html')
#     #     else:
#     #         messages.error(request,'invalid credential')
#     #         return redirect('/testapp/login/')
        
#     # return render (request,'testapp/login.html')
#     if request.method=="GET":
#         return render(request,'testapp/login.html')
    
#     else:

#         userobject=auth.authenticate(username=request.POST["username"] , password=request.POST["password"])

#         if(userobject.username!='admin'):

#             print(connection.queries)

#             print(userobject)

#             print(userobject.id)

#             queryset=MyUser.objects.filter(user_ptr_id=userobject.id)

#             imagepath=queryset[0].imagepath

#             print(queryset[0].imagepath)


#         if userobject==None:
#             return render(request,'testapp/login.html',{'message':"credentials are not correct"})
        
#         else:
            
#             auth.login(request,userobject) # it will start session 

#             queryset=Question.objects.all().values('subject').distinct()

#             #queryset=Question.objects.all()

#             # select distinct subject from question

#             print(f"subjects from db are :- {queryset}")
#             print(connection.queries)
            
#             request.session["username"]=userobject.username
#             request.session["score"]=0
#             request.session["qindex"]=0
#             request.session["answers"]={}

#             if userobject.is_superuser==0:
                
#                 return render(request,'examapp/subject.html',{'listofdictionary':queryset,'imagepath':imagepath})
#             else:
#                 return render(request,'examapp/admindashboard.html')

#https://docs.djangoproject.com/en/5.1/topics/auth/default/
def login(request):
    if request.method == "GET":
        return render(request, 'testapp/login.html')

    else:
        username = request.POST["username"]
        password = request.POST["password"]
        print(f"🔑 Login attempt: {username} / {password}")  
        userobject = auth.authenticate(username=username, password=password)

        if userobject is None:
            print("❌ Invalid credentials")  
            return render(request, 'testapp/login.html', {'message': "credentials are not correct"})

        # ✅ If Admin logs in
        if userobject.is_superuser:
            auth.login(request, userobject)

            request.session["username"] = userobject.username
            request.session["is_admin"] = True
            print("✅ Admin login successful")


            return render(request,'examapp/admindashboard.html')
            # Normal User Login
        else:
                auth.login(request, userobject)

                queryset = Question.objects.all().values('subject').distinct()

                request.session["username"] = userobject.username
                request.session["score"] = 0
                request.session["qindex"] = 0
                request.session["answers"] = {}

                # Fetch user image path
                queryset_user = MyUser.objects.filter(user_ptr_id=userobject.id)
                imagepath = queryset_user[0].imagepath if queryset_user else ''

                return render(request, 'examapp/subject.html',
                            {'listofdictionary': queryset, 'imagepath': imagepath})
@login_required
def admin_verify(request):
    """Extra login verification for admin"""
    if request.method == "GET":
        return render(request, "examapp/admindashboard.html")

    username = request.POST["username"]
    password = request.POST["password"]

    userobject = auth.authenticate(username=username, password=password)

    if userobject and userobject.is_superuser:
        auth.login(request, userobject)
        return render(request, "examapp/admindashboard.html")  # 👉 Create this template
    else:
        messages.error(request, "Invalid admin credentials")
        return render(request, "examapp/admindashboard.html")



def startTest(request):

    subjectname=request.GET["subject"]
    request.session['subject']=subjectname
    
    queryset=Question.objects.filter(subject=subjectname).values()
    questionlist=list(queryset)

    request.session['questionlist']=questionlist

    question=questionlist[0]

    return render(request,"examapp/question.html",{'question':question})


def addition(request,no1,no2):
     
     answer=int(no1) + int(no2)
     
     return HttpResponse(f'{no1} + {no2}= {answer}')


def sum(request):
     
     no1=request.GET["no1"] 
     no2=request.GET["no2"]
     
     answer=int(no1)+int(no2)

     return HttpResponse(f'{no1} + {no2}= {answer}')