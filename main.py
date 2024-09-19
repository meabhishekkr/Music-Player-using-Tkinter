import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import pygame.mixer as mixer
import audio_metadata
import os
import time



# Function to play the selected songs from the list or directory.
def play_song(song_name: StringVar, song_list: Listbox, status: StringVar):
    # Set the name of the current played song on the window.
    name = song_list.get(ACTIVE)
    if len(name) > 40:
        name = (name[:35] + '.mp3')
    song_name.set(name)

    # Load the selected song and start the mixer/play the song.
    mixer.music.load(song_list.get(ACTIVE))
    mixer.music.play()

    # Extract the total song duration from the metadata of the song.
    global duration, metadata
    metadata = audio_metadata.load(song_list.get(ACTIVE))
    song_len = metadata.streaminfo['duration']
    duration = time.strftime('%M:%S', time.gmtime(song_len))

    # Call the play_time function when the song is played.
    play_time()

    # Set the status of the player to Playing.
    status.set("Now Playing..")

    # Active the disabled resume button.
    if resume_btn['state'] == DISABLED:
        resume_btn['state'] = NORMAL


# Function to stop the current song and set the status of the player to 'stop'.
def stop_song(status: StringVar):
    mixer.music.stop()
    status.set("Stopped Playing!!")

    # Disable the resume button when the song is stopped.
    resume_btn['state'] = DISABLED


# Function to pause the current song and set the status of the player to 'pause'.
def pause_song(status: StringVar):
    mixer.music.pause()
    status.set("Paused!")


# Function to resume the paused song and set the status of the player to 'resume'.
def resume_song(status: StringVar):
    mixer.music.unpause()
    if status.get() == "<Not Available>":
        status.set("Please Select a song!")
    else:
        status.set("Song Playing..")



# Function to load all the songs from the specified directory.
def load(listbox):
    # Request the user to input the path of the directory and os will change to that directory.
    os.chdir(filedialog.askdirectory(title="Open a song Directory"))

    # List all the songs present in the specified directory.
    tracks = os.listdir()

    # Takes all the songs from the directory and store in listbox.
    for track in tracks:
        listbox.insert(END, track)


# Function to change the sound volume.
def volume(x):
    value = volume_slider.get()
    mixer.music.set_volume(value / 100)


def play_time():
    # Fetch the song's current time position,
    current_time = mixer.music.get_pos() / 1000

    # Convert the time into minute and second format.
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # show the time on the duration frame and reset the timer when the song is stopped.
    song_duration = duration
    if song_status.get() != 'Song Stopped!!':
        duration_frame.config(text=f"Time Elapsed: {converted_current_time} / {song_duration}")
    else:
        duration_frame.config(text=f"Time Elapsed: 00:00 / {song_duration}")

    duration_frame.after(1000, play_time)


# Starting the mixer.
mixer.init()


# Create the main window
root = tk.Tk()

root.title("Music Player")
root.geometry("400x500")
logo = ImageTk.PhotoImage(file = "logo.png")
root.iconphoto(False, logo)

# It helps to stop the change of the window size.
root.resizable(False, False)

# Creating Frames
song_frame = LabelFrame(root, text="", bg='dark grey', width=400, height=300)
song_frame.place(x=0, y=0)
cover_image = Image.open('cover.jpg')
resized_image = cover_image.resize((400, 300))
cover_image = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(song_frame, image=cover_image)
image_label.pack()


button_frame = LabelFrame(root, text="", bg='light grey', width=400, height=90)
button_frame.place(x = 0,y = 301)

listbox_frame = LabelFrame(root, text='Playlist', bg="grey")
listbox_frame.place(x=0, y=391, height=90, width=400)

volume_frame = LabelFrame(song_frame, text="", bg="light grey")
volume_frame.place(x=290, y=245, height = 50,width = 100)

duration_frame = Label(root, bg='pink', text='Time Elapsed: 00:00 / 00:00', bd=2, relief=GROOVE, width=28, height=2,
                       font=('Helvetica', 10, 'bold'))
duration_frame.place(x=5, y=245)

# StringVar is used to manipulate text in entry, labels.
current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')


# Playlist Listbox.
playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='light grey')


# Make the scroll bar to scroll the playlist.
scroll_bar = Scrollbar(listbox_frame, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=BOTH)
scroll_bar.config(command=playlist.yview)

playlist.config(yscrollcommand=scroll_bar.set)
playlist.pack(fill=BOTH, padx=5, pady=5)


# SongFrame labels.
Label(song_frame, text="CURRENTLY PLAYING:", font=('Times', 10, '')).place(x=5, y=5)

song_lbl = Label(song_frame, textvariable=current_song, font=('Times', 10), bg='light grey')
song_lbl.place(x=145, y=5)

# Control Buttons


play_button = Button(button_frame, text="Play", bg='light blue', font=("Helvetica", 13), width=7,command=lambda: play_song(current_song, playlist, song_status))
play_button.place(x=200, y=5)

resume_btn = Button(button_frame, text='Resume', bg="light blue", font=("Helvetica", 13), width=7,command=lambda: resume_song(song_status))
resume_btn.place(x=290, y=5)

pause_btn = Button(button_frame, text="Pause", bg='light blue', font=('Helvetica', 13), width=7,command=lambda: pause_song(song_status))
pause_btn.place(x=10, y=5)

stop_btn = Button(button_frame, text="Stop", bg='light blue', font=("Helvetica", 13), width=7,command=lambda: stop_song(song_status))
stop_btn.place(x=105, y=5)

dir_btn = Button(button_frame, text="Load Directory", bg='light blue', font=("Helvetica", 13), width=38, command=lambda: load(playlist))
dir_btn.place(x=10, y=45)

# Control the volume of the song.
volume_slider = Scale(volume_frame, from_=0, to=100, orient=HORIZONTAL, command=volume, length=100, bg='grey', cursor='hand2')
volume_slider.set(30)
volume_slider.pack()

Label(root, textvariable=song_status, bg='sky blue', font=('Times', 8), justify=LEFT).pack(side=BOTTOM, fill=X)


root.mainloop()
