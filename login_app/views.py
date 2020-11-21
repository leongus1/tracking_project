from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Users
import bcrypt


# Create your views here.
def index(request):
   ## MAYBE ADD SOME AJAX if there is time
    return render(request, 'index.html')

def success(request):
    
    return redirect('/track')

def register(request):
    request.session.flush()
    if request.method == 'POST':
        errors = Users.objects.userValidator(request.POST)
        unique = Users.objects.filter(email=request.POST['email'])
         
        if len(unique)>0:
            errors['duplicate'] = "This email was already used to create an account."
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request, value)
                
            return redirect ('/')
        else: 
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['reg_or_log']="Registration"
            newuser = Users.objects.get(email=request.POST['email'])
            request.session['user_id'] = newuser.id
            request.session['name'] = newuser.first_name
                        
            return redirect('/success')
    else:
        return redirect ('/')

def check_login(request):
    request.session.flush()
    this_user = Users.objects.filter(email=request.POST['email'])
    errors = {}
    if this_user:
        this_user=this_user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
            request.session['user_id']=this_user.id
            request.session['name'] = f"{this_user.first_name} {this_user.last_name}"
            request.session['reg_or_log']="Login"
            return redirect('/success')
        else:
            errors['pass'] = 'Incorrect Password'
    else:
        errors['user'] = 'Invalid Email Address'
    if len(errors)>0:
        request.session['errors'] = errors  
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')
        
def user_details(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        'user' : Users.objects.get(id=user_id),
        'logged_user': Users.objects.get(id=request.session['user_id']),
    }
    return render(request, 'user.html', context)

def user_edit(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.session['user_id'] == user_id:
        context = {
            'user' : Users.objects.get(id=user_id)
        }
        return render(request, 'edit_account.html', context)
    else: 
        return redirect('/success')
    
def update(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    request.session['update'] = ''
    if request.method == "POST":
        logged_user = Users.objects.get(id=user_id)
        errors = Users.objects.userUpdateValidator(request.POST)
        if not logged_user.email == request.POST['email']:
            if Users.objects.filter(email=request.POST['email']):
                errors['duplicate']="There is already an account with this Email Address"
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect (f'/user/{user_id}/edit')
        
        logged_user.first_name = request.POST['first_name']
        logged_user.last_name  = request.POST['last_name']
        logged_user.email = request.POST['email']
        logged_user.save()
        request.session['update'] = 'Successful Updates!'
        return redirect (f'/user/{user_id}/edit')
        
        
    else:
        return redirect (f'/user/{user_id}/edit')

    
    