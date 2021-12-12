from django.shortcuts import redirect, render
from .models import Poke, User
from django.contrib import messages
import bcrypt

# Create your views here.
# Views
def root(request):
    return render(request, 'index.html')

def sign_in(request):
    return render(request, 'sign_in.html')

def user_dash (request):    
    context = {
        'users' : User.objects.all(),
    }
    return render(request, 'user.html', context)

#def user_profile(request, id):
#    user = User.objects.get(id=id)
#    id = user.id
#    context = {
#        'user' : user,
#    }
#    print(user)
#    print(id)
#    return id and render(request, 'user.html', context)

# Functions

def create_new_user(request):
    if request.method  == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_pw']:
            
            user = User(
                name = request.POST['name'],
                alias = request.POST['alias'],
                email = request.POST['email'],
                password = request.POST['password'],
                user_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode(),
                date_of_birth = request.POST['date_of_birth'],
            )
        
        errors = User.objects.sign_up_validator(request.POST)
        if len(errors) > 0:
       
            for key, value in errors.items():
                messages.error(request, value)
        
            return redirect('/')
        else:
            print(user)
            request.session['name'] = request.POST['name']            
            request.session['email'] = request.POST['email']
            request.session['received_pokes'] = 0   
            request.session['id'] = user.id          
            user.save()            
        return redirect('/user')

def login(request):
    if request.method == 'GET':
        return redirect('/sign_in')
    elif request.method == 'POST':
        email = request.POST['log_email']
        log_password = request.POST['log_pw']
        user = User.objects.get(email=email)
        if bcrypt.checkpw(log_password.encode(), user.user_hash.encode()):
            request.session['email'] = email
            request.session['name'] = user.name
            request.session['id'] = user.id 
            return user.id and redirect('/user')
        else:
            log_password != user.password        
            return redirect('/sign_in')

    else:
        return redirect('/sign_in')

def user_verification(request):
    if request.session.get('email') == None:
        return redirect('/sign_in')

    if request.method == 'POST':
        user = User.objects.get(id=request.POST['id'])
        user.delete()

    users = User.objects.all()
    
    context = {
        'users': users,
    }
    return render(request, 'user.html', context=context)

def logout(request):
    request.session.clear()
    return redirect('/')

def make_a_poke(request, id):
    if request.method == 'GET':
        context = {
            'users' : User.objects.all(),
            'pokes' : Poke.objects.all()
        }
        return render(request, 'user.html', context)

    elif request.method == 'POST':
        origin_id = User.objects.get(email=request.session['email'])
        destination_id = User.objects.get(id=id)
    
        poke = Poke.objects.create(origin_user=origin_id, destination_user = destination_id
        )
        poke.save()
        print(poke)
        print(poke.id)
        print(poke.origin_user_id)
        print(poke.destination_user_id)
     
        return redirect('/user')