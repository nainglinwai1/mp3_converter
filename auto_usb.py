import os
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
from pydub.playback import play
import psutil

def convert_to_mp3(file_path, output_folder):
    try:
        clip = None
        if file_path.endswith(('.mp4', '.mkv', '.avi', '.mov')):
            clip = VideoFileClip(file_path)
        elif file_path.endswith(('.mp3', '.wav')):
            clip = AudioFileClip(file_path)
        else:
            error_label.config(text="Unsupported file format. Only video and audio files are supported.")
            return
        
        output_file_name = os.path.splitext(os.path.basename(file_path))[0] + ".mp3"
        output_file_path = os.path.join(output_folder, output_file_name)
        
        clip.audio.write_audiofile(output_file_path, codec='mp3')
        error_label.config(text="Conversion completed successfully.")
        
    except Exception as e:
        error_label.config(text="An error occurred during conversion: " + str(e))


import os
import psutil

def get_usb_drive_path():
    usb_devices = []
    
    # Iterate over all partitions
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts and partition.mountpoint.startswith('/media/'):
            usb_devices.append(partition.mountpoint)
    
    if usb_devices:
        # Sort the USB devices based on the available space
        usb_devices.sort(key=lambda path: psutil.disk_usage(path).free, reverse=True)
        return usb_devices[0]
    
    return None


def choose_output_folder():
    output_folder = filedialog.askdirectory()
    output_label.config(text=output_folder)

def convert_files():
    usb_path = get_usb_drive_path()
    output_folder = output_label["text"]

    # Check if both USB location and output folder are selected
    if usb_path and output_folder:
        # Iterate over all files in the USB directory
        for root, dirs, files in os.walk(usb_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Convert the file to MP3
                convert_to_mp3(file_path, output_folder)
    else:
        error_label.config(text="Please select an output folder.")

def play_mp3(file_path):
    sound = AudioSegment.from_file(file_path, format="mp3")
    play(sound)

# Create the main window
window = tk.Tk()
window.title("USB to MP3 Converter")
window.geometry("400x280")

# Create and configure the USB location selection button
usb_label = tk.Label(window, text="USB Path:")
usb_label.place(x=20, y=20)

# Get USB path
usb_path = get_usb_drive_path()
if usb_path:
    usb_path_label = tk.Label(window, text=usb_path)
    usb_path_label.place(x=120, y=20)
else:
    usb_path_label = tk.Label(window, text="No USB drive detected.")
    usb_path_label.place(x=120, y=20)

# Create and configure the output folder selection button
output_button = tk.Button(window, text="Select Output Folder", command=choose_output_folder)
output_button.place(x=20, y=60)

output_label = tk.Label(window, text="")
# Create a label to display the selected output folder
output_label.place(x=20, y=100)

# Create and configure the convert button
convert_button = tk.Button(window, text="Convert Files", command=convert_files)
convert_button.place(x=20, y=140)

# Create an error label to display conversion errors
error_label = tk.Label(window, text="", fg="red")
error_label.place(x=20, y=180)

# Create and configure the play button
play_button = tk.Button(window, text="Play MP3", command=lambda: play_mp3(output_label["text"]))
play_button.place(x=20, y=220)

# Start the main event loop
window.mainloop()
