from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here.

def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        passwd = request.POST['passwd']

        user = auth.authenticate(username = uname, password = passwd)

        if user is not None:
            auth.login(request,user)
            request.session['username'] = uname
            return redirect("/")
        else:
            messages.info(request,"Invalid Username/Password")
            return redirect('login')

    return render(request,'accounts/login.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        passwd = request.POST['password']
        cPasswd = request.POST['cpassword']
        
        if passwd == cPasswd:
            if User.objects.filter(username = email).exists():
                messages.info(request,'Username Already Taken')
                return render(request,'accounts/register.html')
            else:
                user = User.objects.create_user(username = email, email = email, first_name = fname, last_name = lname, password = passwd)
                user.save()
                return redirect("login")
        else:
            messages.info(request,'Password and Confirm Password Does not match')
    return render(request,'accounts/register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')