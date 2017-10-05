from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

#required for login and logout
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect,HttpResponse

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required




# Create your views here.



#for logout
@login_required
def user_logout(req):
    logout(req)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(req):
    return HttpResponse("You are logged in")


def index(req):
    return render( req, 'basic_app/index.html')

def register(req):

    registered = False

    if req.method == "POST":
        user_form = UserForm(data = req.POST)
        profile_form = UserProfileInfoForm(data = req.POST)

        # check valid or not
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() # save to db
            user.set_password(user.password) #hashing the password, it goes to setting.py
            user.save()

            profile = profile_form.save(commit = False) #dont commit to avoid collision
            profile.user = user #sets up the one to one relationship with the user

            #check actual profile pict is provided or not
            if 'profile_pic' in req.FILES:
                profile.profile_pic = req.FILES['profile_pic']
            profile.save()
            print("saved")
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm() #instance of UserForm
        profile_form = UserProfileInfoForm()

    return render(req, 'basic_app/registeration.html',
                    {
                    'user_form':user_form,
                     'profile_form':profile_form,
                     'registered':registered
                     }
                )



#for login

def user_login(req):

    if req.method == "POST":
        #get the login form data
        username = req.POST.get('username')
        password = req.POST.get('password')

        #we are going to use django built in authenticate fucntions
        user = authenticate(username = username, password = password) #this line will authenticate user for you

        if user:

            if user.is_active:
                login(req,user)
                #send the user back to somepage
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Acount not Active")
        else:
            print("Someone tried to login and Failed")
            print("UserName: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid login Details")
    else:
        return render(req, 'basic_app/login.html')
