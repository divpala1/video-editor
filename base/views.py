from django.core.files import File
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm
import webvtt
from webvtt import WebVTT, Caption
import os

def home(request):
    videos = Video.objects.all()
    
    context = {'videos':videos}
    return render(request, 'base/index.html', context=context)

def editVideo(request, pk):
    if request.method == 'POST':
        subFileName = request.POST.get("subFile")
        startList = request.POST.getlist("startTime")
        endList = request.POST.getlist("endTime")
        subList = request.POST.getlist("subs")

        vtt = WebVTT()

        for i in range(len(startList)):
            # creating a caption with a list of lines
            print(startList[i], ' : ', endList[i], ' : ', subList[i].split('\n'))
            
            if startList[i] and endList[i] and subList[i]:
                caption = Caption(
                    startList[i],
                    endList[i],
                    subList[i].replace('\r', '').split('\n')
                )

                # adding a caption
                vtt.captions.append(caption)
                
            else:
                messages.error(request, 'One of the fields was empty for a subtitle entry and hence that was skipped.')

        os.remove(f'media/subtitles/{subFileName}')
        vtt.save(f'media/subtitles/{subFileName}')
        
        return redirect('edit', pk)
    
    video = Video.objects.get(id=pk)
    sub_file_path = f'media/subtitles/{video.name}.vtt'
    subtitles = webvtt.read(sub_file_path)
    
    context = {'video':video, 'subtitles':subtitles, 'sub_file_path':sub_file_path}
    
    return render(request, 'base/edit_video.html', context)

def uploadVideo(request):
    form = VideoForm()
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            new_vid = form.save(commit=False)
            
            if Video.objects.filter(name=new_vid.name).exists():
                messages.error(request, 'The name is already taken. Try a different name.')
                
                return redirect('home')
                
            else:
                # Creating subtitles file
                file_path = f'media/subtitles/{new_vid.name}.vtt'
                with open(file_path, 'w') as fp:
                    fp.write('WEBVTT')

                # Add the file to the caption_file field
                with open(file_path, 'rb') as fp:
                    new_vid.caption_file.save(f'{new_vid.name}.vtt', File(fp), save=False)

                # Save the model instance
                new_vid.save()

                # Deleting the new file created by Django in the media folder due to the FileField in caption_file.
                os.remove(f'media/{new_vid.name}.vtt')
                
                return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/upload.html', context)

def deleteVideo(request, pk):
    video = Video.objects.get(id=pk)
    
    try:
        os.remove(f'media/{video.video}')
    except FileNotFoundError:
        print('Video file not found while deleting.')

    try:
        os.remove(f'media/subtitles/{video.name}.vtt')
    except FileNotFoundError:
        print('Subtitle file not found while deleting.')
    
    video.delete()
    
    return redirect('home')
