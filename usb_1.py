import os
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, AudioFileClip

def convert_to_mp3(file_path, output_path):
    try:
        clip = None
        if file_path.endswith(('.mp4', '.mkv', '.avi', '.mov')):
            clip = VideoFileClip(file_path)
        elif file_path.endswith(('.mp3', '.wav')):
            clip = AudioFileClip(file_path)
        else:
            error_label.config(text="Unsupported file format. Only video and audio files are supported.")
            return
        
        clip.audio.write_audiofile(output_path, codec='mp3')
        error_label.config(text="Conversion completed successfully.")
        
    except Exception as e:
        error_label.config(text="An error occurred during conversion: " + str(e))

def choose_usb_location():
    usb_path = filedialog.askdirectory()
    usb_label.config(text=usb_path)

def convert_files():
    usb_path = usb_label["text"]

    # Check if a USB location is selected
    if usb_path:
        # Iterate over all files in the USB directory
        for root, dirs, files in os.walk(usb_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                output_path = os.path.splitext(file_path)[0] + ".mp3"

                # Convert the file to MP3
                convert_to_mp3(file_path, output_path)
    else:
        error_label.config(text="Please select a USB location.")

# Create the main window
window = tk.Tk()
window.title("USB to MP3 Converter")
window.geometry("400x200")

# Create and configure the USB location selection button
usb_button = tk.Button(window, text="Select USB Location", command=choose_usb_location)
usb_button.place(x=20, y=20)

# Create a label to display the selected USB location
usb_label = tk.Label(window, text="")
usb_label.place(x=20, y=60)

# Create and configure the convert button
convert_button = tk.Button(window, text="Convert Files", command=convert_files)
convert_button.place(x=20, y=100)

# Create an error label to display conversion errors
error_label = tk.Label(window, text="", fg="red")
error_label.place(x=20, y=140)

# Start the main event loop
window.mainloop()
