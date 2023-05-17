from tkinter import Tk, Label, Button, filedialog
from moviepy.editor import VideoFileClip, AudioFileClip

def convert_to_mp3():
    file_path = filedialog.askopenfilename(filetypes=[("Video/Audio files", "*.mp4 *.mkv *.avi *.mov *.mp3 *.wav")])
    if file_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if output_path:
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

def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("Video/Audio files", "*.mp4 *.mkv *.avi *.mov *.mp3 *.wav")])
    if file_path:
        file_label.config(text=file_path)

# Create the main window
window = Tk()
window.title("Video/Audio to MP3 Converter")

# Create and configure the file selection button
browse_button = Button(window, text="Browse", command=browse_files)
browse_button.pack()

# Create a label to display the selected file path
file_label = Label(window, text="")
file_label.pack()

# Create and configure the convert button
convert_button = Button(window, text="Convert", command=convert_to_mp3)
convert_button.pack()

# Create an error label to display conversion errors
error_label = Label(window, text="")
error_label.pack()

# Start the main event loop
window.mainloop()
