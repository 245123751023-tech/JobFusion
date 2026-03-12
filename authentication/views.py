from django.shortcuts import render,redirect
from home import views,urls
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import Profile


# Create your views here.


def page1_view(request):    # page -1
    user_id = request.session.get("user_id")
    username = None
    if user_id:
        user = User.objects.get(id=user_id)
        username = user.username

    if (request.method=='POST'):
        fullname = request.POST.get('fullname')
        phno = request.POST.get('phno')
        location = request.POST.get('location')


        user_id = request.session.get("user_id")
        print(user_id,request.session.get("user_id"))

        if user_id:
            user = User.objects.get(id=user_id)
            profile_object,created = Profile.objects.get_or_create(user=user)
            profile_object.full_name = fullname
            profile_object.phone = phno
            profile_object.location = location
            profile_object.save()
            
            return redirect('rolespage')

    return render(request,"page1.html",{'username':username})


def rolespage(request):     # page -2
    if(request.method=='POST'):
        role = request.POST.get('choice')
        print(role)
        user_id = request.session.get("user_id")
        print(user_id,request.session.get("user_id"))
        if user_id:
            user = User.objects.get(id=user_id)
            profile_object,created = Profile.objects.get_or_create(user=user)
            profile_object.Role = role
            profile_object.save()
            #del request.session["user_id"]
            return redirect('page3')
    return render(request,'rolespage.html',{})

def page3_view(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    profile_object,k = Profile.objects.get_or_create(user=user)
    if(request.method=='POST'):
        skills = request.POST.getlist('skills')
        user_id = request.session.get('user_id')
        skills = ",".join(skills)
        print(skills)

        otherskills = request.POST.get('otherskills')
        print("=============Other skills:=============",otherskills)
        exp = request.POST.get('exp')
        gclg = request.POST.get("gclg")
        gstartingyear = request.POST.get('gstartingyear')
        gendingyear = request.POST.get('gendingyear')
        gbranch = request.POST.get('gbranch')
        #liurl = request.POST.get('liurl')
        gcgpa = request.POST.get('gcgpa')
        gclgadd = request.POST.get('gclgadd')
        iclg = request.POST.get('iclg')
        istartingyear = request.POST.get('istartingyear')
        iendingyear = request.POST.get('iendingyear')
        ibranch = request.POST.get('ibranch')
        imarks = request.POST.get('imarks')
        schoolname = request.POST.get('schoolname')
        sscyear = request.POST.get('sscyear')
        cname = request.POST.get('cname')
        industry = request.POST.get('industry')
        cadd = request.POST.get('cadd')
        hiringneeds = request.POST.get('hiringneeds')
        cemail = request.POST.get('cemail')

        if user_id:
            user = User.objects.get(id=user_id)
            profile_object,k = Profile.objects.get_or_create(user=user)
            if profile_object.Role not in ['Manager','HR','Recruiter']:
                profile_object.skills = skills
                profile_object.otherskills = otherskills
                profile_object.exp = exp
                #profile_object.liurl = liurl
                profile_object.gclg = gclg
                profile_object.gstartingyear = gstartingyear
                profile_object.gendingyear = gendingyear
                profile_object.gbranch = gbranch
                profile_object.gcgpa = gcgpa
                profile_object.gclgadd = gclgadd
                profile_object.iclg = iclg
                profile_object.istartingyear = istartingyear
                profile_object.iendingyear = iendingyear
                profile_object.ibranch = ibranch
                profile_object.imarks = imarks
                profile_object.otherskills = otherskills
                profile_object.schoolname = schoolname
                profile_object.sscyear =sscyear
            else: # user may be hr or manager or recruiter
                profile_object.cname = cname
                profile_object.cadd = cadd
                profile_object.cemail=cemail
                profile_object.hiringneeds = hiringneeds
            

            profile_object.save()

            return redirect('page4')

    return render(request,'page3.html',{'profile':profile_object})

def page4_view(request):
    if(request.method=='POST'):
        profilepic = request.FILES.get('profilepic')
        user_id = request.session.get('user_id')
        liurl = request.POST.get('liurl')
        if user_id:
            user = User.objects.get(id=user_id)
            profileobj,k = Profile.objects.get_or_create(user=user)
            profileobj.liurl = liurl
            profileobj.profile_pic = profilepic
            profileobj.save()
        return redirect('login')
    return render(request,"page4.html",{})

def login_view(request):
    user_id = request.session.get("user_id")
    pwd = request.session.get("raw_pwd")
    username = None
    pwd = None
    if user_id:
        username = User.objects.get(id=user_id)
    print(pwd)
    if(request.method=='POST'):
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        print(uname,pwd)
        user = authenticate(request,username=uname,password=pwd)
        
        if user is not None:
            z = login(request,user)
            print(z)
            #messages.success(request,f"Welcome Back,{user.username}"!)
            return redirect('home')
        messages.error(request,'Invalid Username or password!')
    return render(request,"login.html",{'username':username})

def logout_view(request):
    logout(request)
    messages.success(request,"You Have been Logged out.")
    return redirect("login")


def signup_view(request):
    if(request.method=='POST'):
        uname = request.POST.get('username')
        Email = request.POST.get("Email")
        pwd = request.POST.get('password')
        #phno = request.POST.get('phno')

        print(uname,pwd)
        
        if(User.objects.filter(username=uname).exists()):
            messages.error(request,"Username already exists!")
            return redirect('login')
        
        user = User.objects.create_user(username=uname,password=pwd,email=Email)
        user.save()
        request.session["user_id"] = user.id
        request.session["raw_pwd"] = pwd
        messages.success(request,"Signup Successfull!,Please Continue.")
        return redirect("page1")
        #return redirect("login")
    return render(request,"signup.html",{})


def learnmore_view(request):
    return render(request,'learnmore.html',{})

