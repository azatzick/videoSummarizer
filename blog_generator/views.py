from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
import json

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            #converts into python dict
            data = json.loads(request.body)
            yt_link = data['link']
            return JsonResponse({'content':yt_link })
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'invalid data sent',}, status=400)
        
        # get title of the video 
        # get the transcript 
        # use openAI to generate the blog 
        # save blog article to DB 
        # return blog article as a response 
        
    else:
        return JsonResponse({'error': 'invalid request method',}, status=405)
    pass
        
    
    
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            # Handle successful signup logic here (e.g., create user)
            try:
                user = User.objects.create_user(username=username,password=password, email=email)
                user.save()
                login(request,user)
                return redirect('/')  # Redirect to the homepage page after signup
            except:
                error_message = "error creating account"
                return render(request, 'signup.html', {'error_message': error_message})
        else: 
            error_message = "Passwords do not match"
            return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    return redirect('/')

