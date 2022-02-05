#Music Player

#import libraries
from tkinter import *
from tkinter import filedialog as fd
from pygame import mixer
import os
from PIL import Image, ImageTk

#intializing music player
mixer.init()
theFont = "@ Yu Gothic UI Semibold"
mixer.music.set_volume(0.7)

#Creating the GUI
window = Tk()
window.title("SimplyMusic")
#WidthxHeight
window.geometry("460x350")
window.configure(background = "black")

#Opening the file and adding songs to list
directory = fd.askdirectory()
os.chdir(directory)
songs = []
for music in os.listdir(directory):
    if music.endswith(".mp3"):
        songs.append(music)
songNumber = 0
    
#Title of App
playing = Label(text = "SimplyMusic", font = (theFont, 12))
playing.place(x = 130, y = 20, width = 200, height = 25)
playing["bg"] = "black"
playing["fg"] = "white"
playing["relief"] = "sunken"

#Title of the Song
title = Label(text = "Not Playing", font = (theFont, 14))
title.place(x = 80, y = 260, width = 300, height = 25)
title["bg"] = "black"
title["fg"] = "white"

#Cover art of the song
def placeImage():
    global directory
    for images in os.listdir(directory):
        if images.endswith(".png"):
            image = Image.open(images)
            resize_image = image.resize((200,200), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(resize_image)
            label1 = Label(image=img)
            label1.image = img
            label1.pack()
            label1.place(x = 130, y = 50)
placeImage()

#SongList
def loadSongs():
    global songs
    global songNumber
    songNumber = 0
    mixer.music.load(songs[songNumber])
loadSongs()

#Actual Player
def StartOrPlayOrPause():
    if mixer.music.get_busy() == True:
        mixer.music.pause()
    else:
        mixer.music.unpause()
        if mixer.music.get_busy() == False:
            mixer.music.play()
            #Changes song title
            global title
            title.config(text = songs[songNumber].removesuffix(".mp3"))

#Restarts song
def restart():
    mixer.music.rewind()

#Plays last song
def lastSong():
    #Previous song
    global songNumber
    #Prevents reversal
    if songNumber != 0:
        songNumber -= 1
        mixer.music.load(songs[songNumber])
        mixer.music.play()
        global title
        title.config(text = songs[songNumber].removesuffix(".mp3"))
        
#Change volume based on slider
def volume(x):
    new = volume_sli.get()*0.01
    mixer.music.set_volume(new)
    
#Slider
volume_sli = Scale(from_= 100, to=0,orient="vertical", command = volume)
volume_sli.place(x = 350, y = 50, width = 100, height = 204)
volume_sli.set(100)

#Skips song
def skip():
    #Loads next song in array
    global songNumber
    #Can't have it breaking out
    if songNumber != len(songs)-1:
        songNumber += 1
        mixer.music.load(songs[songNumber])
        mixer.music.play()
        #Changes song title
        global title
        title.config(text = songs[songNumber].removesuffix(".mp3"))

#Open New Album
def newAlbum():
    #imports all variables needed as globals
    global songs
    global songNumber
    global title
    global directory
    songs = []
    directory = fd.askdirectory()
    os.chdir(directory)
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            songs.append(files)
    songNumber = 0
    placeImage()
    loadSongs()
    temp = songs[songNumber]
    temp.removesuffix(".mp3")
    title.config(text = temp)
    songList.delete(0, END)
    for song in songs:
        songList.insert(END,song.removesuffix(".mp3"))
    StartOrPlayOrPause()

#Switches song
def onselect(event):
    global songNumber
    w = event.widget
    i = int(w.curselection()[0])
    songNumber = i
    title.config(text = songs[songNumber].removesuffix(".mp3"))
    mixer.music.load(songs[songNumber])
    mixer.music.play()
   
#Functional Buttons
playButton = Button(text = "Play", command = StartOrPlayOrPause)
playButton.place(x = 180, y = 290, width = 100, height = 25)

lastSongButton = Button(text = "Previous Song", command = lastSong)
lastSongButton.place(x = 80, y = 290, width = 100, height = 25)

newSongButton = Button(text = "Next Song", command = skip)
newSongButton.place(x = 280, y = 290, width = 100, height = 25)

restartButton = Button(text = "Restart", command = restart)
restartButton.place(x = 20, y = 20, width = 100, height = 25)

volumeTitle = Label(text = "Volume")
volumeTitle.place(x = 350, y = 20, width = 100, height = 25)

changeButton = Button(text = "Change Album", command = newAlbum)
changeButton.place(x = 180, y = 315, width = 100, height = 25)

songList = Listbox(window)
songList.place(x = 20, y = 50, width = 100, height = 204)
for song in songs:
    songList.insert(END,song.removesuffix(".mp3"))

songList.bind('<<ListboxSelect>>',onselect)

window.mainloop()
