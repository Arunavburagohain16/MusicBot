import speech_recognition as sr
import re
import urllib.request
from bs4 import BeautifulSoup
import pafy
from selenium import webdriver
import requests
import os
from gtts import gTTS

#Get audio from the microphone
r = sr.Recognizer()
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

language='en'
p=0
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)
    print("Say:")
    audio = r.listen(source)

try:
    said=r.recognize_google(audio)
    print("You said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))

try:
    said_list=re.split(r'\s',said)
    print(said_list)

    for i in range(len(said_list)):
        if said_list[i]=="play":
            p=1
            print("you are ready to proceed")
            print(said_list[i+1:])
            music_list=said_list[i+1:]
    if p==1:
        music=(" ".join(music_list))
        print(music)
#Text to Speech part
        mytext="You asked to play "+music
        print(mytext)
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("sound.mp3")
        os.system("sound.mp3")

#Search for the song in youtube
        Search = music
        query = urllib.parse.quote(Search)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        c=0
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            print('https://www.youtube.com' + vid['href'])
            if c==0:
                video_url='https://www.youtube.com' + vid['href']
            c+=1
        print("Video link:",video_url)

#Play the youtube link
        video=pafy.new(video_url)
        best=video.getbest()
        playurl = best.url
        print(video.title)
        print(video.description)
        browser = webdriver.Chrome()
        browser.get(playurl)
    else:
        print("Use the command play to play songs")
        mytext="Didnot get the play command in your speech"
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("sound.mp3")
        os.system("sound.mp3")


except NameError:
    print("Error Occured")
    mytext="Error Occured"
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("sound.mp3")
    os.system("sound.mp3")
