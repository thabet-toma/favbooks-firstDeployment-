from ast import Return
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
import  bcrypt
def logandRegs(request):
    return render(request,'LogAndRegs.html')
def regs(request):
    errors = Users.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
    
        hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        Users.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],email=request.POST['email'],password=hash)
        request.session['user']=Users.objects.last().first_name
        request.session['state']='registered'
        return redirect('/success1')
def success1(request):
    if 'user' in request.session:
        context={'last':Users.objects.last()}
        return render(request,'success.html',context)
    else:
        return redirect('/') 
def login(request):
    
    # see if the username provided exists in the database
    user = Users.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0] 
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            # if we get True after checking the password, we may put the user id in session
            request.session['user'] = logged_user.first_name
            request.session['state']='logged in'
            request.session['Uid']=logged_user.id
            # never render on a post, always redirect!
            return redirect('/books')
        else:
            messages.error(request, 'invalid email or password')
            return redirect("/")

    # if we didn't find anything in the database by searching by username or if the passwords don't match, 
    # redirect back to a safe route
    return redirect("/")
def logout(request):
    del request.session['user']
    del request.session['Uid']
    return redirect('/')
def book(request):
    if 'Uid' in request.session:
        context={
            'user':Users.objects.get(id=request.session['Uid']),
            'allBooks':Books.objects.all()
        }
        
        return render(request,'books.html',context)
    else:
        return redirect('/')
def addbook(request):
    errors = Books.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/books')
    else:
        user=Users.objects.get(id=request.session['Uid'])
        Books.objects.create(title=request.POST['title'],desc=request.POST['desc'],Uploadby=user)
        Books.objects.get(title=request.POST['title']).users.add(user)
        return redirect('/books')
def bookDe(request,id):
    context={'book':Books.objects.get(id=id),
    'user':Users.objects.get(id=request.session['Uid'])
    }
    return render(request,'bookDe.html',context)
def addfav(request,id):
    user=Users.objects.get(id=request.session['Uid'])
    Books.objects.get(id=id).users.add(user)
    return redirect('/books/'+str(id))
def delfav(request,id):
    user=Users.objects.get(id=request.session['Uid'])
    Books.objects.get(id=id).users.remove(user)
    return redirect('/books/'+str(id))
def edit(request):
    if request.POST['edit']=='update':
        x=Books.objects.get(id=request.POST['id'])
        x.title=request.POST['title']
        x.desc=request.POST['desc']

        x.save()
        return redirect('/books/'+request.POST['id'])
    else:
        Books.objects.get(id=request.POST['id']).delete()
        return redirect('/books')


    




    
        
# Create your views here
