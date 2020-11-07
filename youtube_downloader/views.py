from django.shortcuts import render,redirect
import youtube_dl
from youtube_dl import YoutubeDL
# Create your views here.

def home(request) :
    global info
    if request.method == "POST" :
        try :  
            video_url = request.POST['videourl']
            ydl =YoutubeDL()
            info= ydl.extract_info(video_url,download=False)
            return redirect('video_info')
        except Exception : 

            return render(request,'youtube_downloader/home.html',{'error':'An Error occured please check link you typed and try again ! '}) 

    else : 
        return render(request,'youtube_downloader/home.html')

def video_info(request,*args,**kwargs) : 
    video_streams = []
    for f in info['formats'] : 
        
        
        filesize = f['filesize']
        if filesize is not None : 
            filesize = f"{round(int(filesize)/1000000,2)}mb"
        resolution = 'audio' 
        if f['height'] is not None : 
            resolution = f"{f['height']}x{f['width']}"
        
        format=f['format_id'].split('-',1)[0]
        
     
        video_streams.append({ 
            'resolution':resolution , 
            'filesize':filesize ,
            'video_url':f['url'],
            'ext': f['ext'] ,
            'format' : format ,
            
            
        })   
        
    context = {
            'title':info['title'],
            'id' : info['id'],
          
            'thumbnail':info['thumbnail'],
            'streams': video_streams , 
    }
    
    return render(request,'youtube_downloader/video_info.html',context)
def download(request,id,format) :
    url = 'https://www.youtube.com/watch?v=' + id
    print(url,format)
    ydl_opts =  {
        'format' : format
    }
    try : 
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e :
        print(Exception)
    


    return render(request,'youtube_downloader/download.html',{})
