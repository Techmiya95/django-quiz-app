from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile
from django.contrib.auth.decorators import login_required
from quizes.models import QuizSubmission

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    if request.method =='POST':
        email =  request.POST['email']
        username =  request.POST['username']
        password =  request.POST['password']
        password2 =  request.POST['password2']

        if password == password2:
            print('Password Matched')
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect('register')

            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect('register')
            #create user
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log in the user amd redirect to profile
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                
                return redirect('profile', username)
        else:
            messages.info(request, "Password not Matching.")
            return redirect('register')
    context = {}
    return render(request, "register.html", context)


@login_required(login_url='login')
def profile(request, username):
    # Profile user
    user_object2 = User.objects.get(username=username)
    user_profile2, created = Profile.objects.get_or_create(user=user_object2)

    # Request user
    user_object = request.user
    user_profile, created = Profile.objects.get_or_create(user=user_object)

    # Fix: Ensure we use `user_profile2.user` in query
    submission = QuizSubmission.objects.filter(user=user_profile2.user)
    
    context = {"user_profile": user_profile, "user_profile2": user_profile2, "submissions": submission}
    
    return render(request, "profile.html", context)




def login(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)

    if request.method == "POST":
       username = request.POST['username']
       password = request.POST['password']
       user= auth.authenticate(username=username, password=password)
    
       if user is not None:
         auth.login(request, user)
         return redirect('profile', username)
       else:
           messages.info(request,'Credentials Invalid!')
           return redirect('login')

    return render(request, "login.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def editProfile(request):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        if request.FILES.get('profile_img') != None:
            user_profile.profile_img = request.FILES.get('profile_img')
            user_profile.save()


        if request.POST.get('email') != None:
            u = User.objects.filter(email=request.POST.get('email')).first()

            if u == None:
                user_object.email = request.POST.get('email')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request, "Email Already Used, Choose a Different One")
                    return redirect('edit_profile')
                

    #username
        if request.POST.get('username') != None:
            u = User.objects.filter(username=request.POST.get('username')).first()

            if u == None:
                user_object.username = request.POST.get('username')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request, "Username ALready Used, Choose a Different One")
                    return redirect('edit_profile')
                

#first name and lastname
        user_object.first_name = request.POST.get('firstname')
        user_object.last_name = request.POST.get('lastname')
        user_object.save()

#location, bio, gender
        user_profile.location = request.POST.get('location')
        user_profile.gender = request.POST.get('gender')
        user_profile.bio = request.POST.get('bio')
        user_profile.save()

        return redirect('profile', user_object.username)
    
    context = {"user_profile": user_profile}
    return render(request, 'profile-edit.html', context)



        
        

@login_required(login_url='login')
def deleteProfile(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    
    if request.method == "POST":
        user_profile.delete()
        user_object.delete()
        return redirect('logout')


    context = {"user_profile": user_profile}
    return render(request, 'confirm.html', context)

