from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login,authenticate,logout
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .forms import  DownloadTaskforms ,fileCreationforms, processdownloadforms
from django.contrib.auth.forms import  AuthenticationForm
from .models import DownloadTask,fileCreation,processdownload
import os, threading, queue, uuid
from youtubeconverter import YouCon
download_queue = queue.Queue()
import logging
logger=logging.getLogger(__name__)

def register(request):
    form = DownloadTask(request.POST)
    if form.is_valid():
        user = form.save()
        username=form.cleaned.data.get('username')
        password=form.cleaned.data.get('password1')
        user=authenticate(username=username,password=password)
        auth_login(request, user)
        return redirect('index')  # Redirect to home after registration
    if user is not None:
        auth_login(request, user)
        return redirect('index')
    else:
        form=DownloadTask
        return render(request,'youtube/register.html',{'form':form})
    
def UserCrea(request):
    if request.method == 'POST':
        form = fileCreationforms(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)
            username=user,username
            messages.error(request,'kullanicinin adi veya parolasi hatali')

        else:
            form=AuthenticationForm()
            form.add_error(None, "Invalid username/email or password.")
    else:
        form = fileCreationforms()
    return render(request, 'registration/login.html', {'form': form})


def processdownload():
    while True:
        task = download_queue.get()
        if task is None: 
            break
        link, path, task_id = task
        try:
            task_obj = DownloadTask.objects.get(task_id=task_id)
            task_obj.status = "In Progress"
            task_obj.save()

            youtubeconverter_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'no-mtime': True
            }
            with YouCon (youtubeconverter_opts) as YouCon:
                info_dict = YouCon.extract_info(link, download=False)
                title = info_dict.get('title', None)
                ext = info_dict.get('ext', None)
                original_file = os.path.join(path, f"{title}.{ext}")
                mp3_file = os.path.join(path, f"{title}.mp3")

                if os.path.exists(mp3_file):
                    task_obj.status = "File already exists"
                    task_obj.file_path = path
                    task_obj.title = title
                else:
                    YouCon.download([link])
                    if os.path.exists(original_file):
                        os.rename(original_file, mp3_file)
                    task_obj.title = title
                    task_obj.status = "Completed"
                    task_obj.file_path = mp3_file
            task_obj.save()
        except Exception as e:
            task_obj.status = "Error"
            task_obj.error_message = str(e)
            task_obj.save()
        finally:
            download_queue.task_done()
@login_required
def status(request):
    tasks = DownloadTask.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'status.html', {"tasks": tasks})

@login_required
def get_task_status(request):
    tasks = DownloadTask.objects.filter(user=request.user).order_by('-created_at').values(
        'title', 'link', 'status', 'error_message', 'created_at', 'updated_at', 'file_path'
    )
    return JsonResponse(list(tasks), safe=False)

@login_required 
def index(request):
    if request.method == "POST":
        form = fileCreation(request.POST)
        if form.is_valid():
            link = form.cleaned_data["link"]
            validator = URLValidator()
            try:
                validator(link)
                path = os.path.join(os.path.expanduser('~'), 'downloads')
                task_id = str(uuid.uuid4())
            
                DownloadTask.objects.create(
                    task_id=task_id,
                    link=link,
                    status="Queued",
                    user=request.user  
                )
                download_queue.put((link, path, task_id))
                messages.info(request, f"Your download request has been added to the queue. Task ID: {task_id}")
                return redirect("status")
            except ValidationError:
                messages.error(request, "Invalid URL. Please provide a valid YouTube link.")
                return redirect("index")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect("index")

    form = fileCreation()
    return render(request, 'index.html', {"form": form})

threading.Thread(target=processdownload, daemon=True).start()
