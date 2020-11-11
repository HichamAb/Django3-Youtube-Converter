from __future__ import unicode_literals
from django.shortcuts import render,redirect
import youtube_dl
from youtube_dl import YoutubeDL
from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import datetime



# Create your views here.

def home(request) :
    global video
    if request.method == "POST" :
        try :  
            video_url = request.POST['videourl']
            ydl =YoutubeDL()
            video= ydl.extract_info(video_url,download=False)
            print(video['format'])
            return redirect('video_info')
        except Exception as e : 

            return render(request,'youtube_downloader/home.html',{'error':f'An Error occured please check link you typed and try again !\n {e} '}) 

    else : 
        return render(request,'youtube_downloader/home.html')

def video_info(request,*args,**kwargs) : 
    try : 
        video_streams = []
        audio_streams = []
        #loop through the video parameters 
        '''
        for d in  video['formats'] : 
            for k,v in d.items() : 
                print(f'{k} :')    '''          
        for v in video['formats'] :
            
            #Check if the object has size
            filesize = v['filesize']
            if filesize is not None : 
                #convert size to "mb"
                filesize = f"{round(int(filesize)/1000000,2)}mb"
            
             
                
            if v['format_note'] =='tiny' : 
                audio_streams.append({
                    'britate' : v['abr'] , 
                    'filesize' : filesize , 
                    'format':v['format_id'],

                })
            else :
                #add object resolution
                resolution = f"{v['height']}x{v['width']}" 
                video_streams.append({
                    'video_quality' : v['format_note'],
                    'resolution' : resolution,
                    'filesize' : filesize , 
                    'format':v['format_id'],

                })
            #Just for test 
            '''try :
                for a,b in v.items() : 
                    print(f'{a} : {b}')
                print(v['format_note'],'----',v['format'],filesize)
            except : print("error")

            video_streams.append({ 
                'resolution':resolution , 
                'filesize':filesize ,
                'video_url':f['url'],
                'ext': f['ext'] ,
                'format' : f['format_id'] ,
                'download_url':f['url']+"&title="+video['title'] ,
                'quality' : quality ,
            }) 
            '''
        duration = datetime.timedelta(seconds=video["duration"])
        context = {
                'title':video['title'],
                'uploader':video['uploader'],
                'uploaded':video['upload_date'],
                'duration':duration,
                'viewcount':video['view_count'],
                'id' : video['id'],
                'thumbnail':video['thumbnail'],
                'video_streams': video_streams , 
                'audio_streams' : audio_streams,
                "media_url":settings.MEDIA_URL,
                'web_url':video['webpage_url'] ,
                'category':video['categories'][0]
        }
        
        return render(request,'youtube_downloader/video_info.html',context)
    except NameError : 
        return redirect('home')
def download(request,id,format,vtype) :
    title = video['title']
    url = id 
    if 'p' in vtype : 
        ydl_opts_VIDEO = {
        'format': format,
        'download_archive ':'download_archive.txt',
        'outtmpl': 'media/downloaded/%(title)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' :True ,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4' ,
            }],
        }
        try : 
            with youtube_dl.YoutubeDL(ydl_opts_VIDEO) as ydl:
                ydl.download([url])
                #print(type(title),title)
                filename=title +'.mp4'
                context = {
                'media_url':settings.MEDIA_URL ,
                'filename' : filename ,
                }

                return render(request,'youtube_downloader/download.html',context)
        except Exception as e :
            return render(request,'youtube_downloader/download.html',{"Error":e})
    
    else :
        ydl_opts_AUDIO =  {
            'format': format,
            'outtmpl': 'media/downloaded/%(title)s.%(ext)s',
            'writethumbnail': True,
            'noplaylist' :True ,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': 'best',
                
                
                
                }],
            }
     
        try : 
            with youtube_dl.YoutubeDL(ydl_opts_AUDIO) as ydl:
                ydl.download([url])
                #print(type(title),title)
                filename=title +'.opus'
                context = {
                'media_url':settings.MEDIA_URL ,
                'filename' : filename ,
                }

                return render(request,'youtube_downloader/download.html',context)
        except Exception as e :
            return render(request,'youtube_downloader/download.html',{"Error":e})

        
    print(ydl_opts_VIDEO['postprocessors']['key'])
    
    
    

    
    
    
        