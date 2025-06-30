import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
import json
from pytubefix import YouTube 
import assemblyai as aai
import openai

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
            #return JsonResponse({'content':yt_link })
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'invalid data sent',}, status=400)
        
        # get title of the video 
        title = yt_title(yt_link)
        
        # get the transcript 
        transcription = get_transcript(yt_link)
        if not transcription:
            return JsonResponse({'error': 'failed to transcribe video'}, status = 500)
            
        # use openAI to generate the blog 
        content = generate_blog_response(transcription)
        if not content:
            return JsonResponse({'error': 'failed to generate response from openAI'}, status = 500)
        
        # save blog article to DB
         
        # return blog article as a response
        return JsonResponse({'content' : content}) 
        
    else:
        return JsonResponse({'error': 'invalid request method',}, status=405)
        
def yt_title(link):
    yt= YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base,ext= os.path.splitext(out_file)
    new_file = base + '.mp3' 
    os.rename(out_file, new_file)
    return new_file

def get_transcript(link):
    audio_file = download_audio(link)
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")  # Ensure you have set your AssemblyAI API key in your environment variables
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text
    
def generate_blog_response(transcription):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you have set your OpenAI API key in your environment variables
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes blog articles."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=1
    )
    return response.choices[0].message.content.strip()
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

