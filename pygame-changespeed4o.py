import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import pygame
import io

# Initialize Pygame mixer
pygame.mixer.init()

global current_position_ms

# Load audio file into memory
def load_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    return audio


# Function to play the audio at the given speed from a specific position
def play_audio(audio, speed, start_pos_ms):
    pygame.mixer.music.stop()  # Stop any currently playing music

    # Adjust the speed
    new_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * speed)})
    new_audio = new_audio.set_frame_rate(audio.frame_rate)

    # Convert to bytes and play using pygame
    audio_io = io.BytesIO()
    new_audio.export(audio_io, format="wav")
    audio_io.seek(0)
    pygame.mixer.music.load(audio_io)

    # Calculate the position to start from in terms of frames
    start_pos_frames = int(start_pos_ms * (new_audio.frame_rate / 1000.0))
    pygame.mixer.music.play(start=round(start_pos_frames / new_audio.frame_rate))


# Function to handle the slider change
def on_slider_change(val):

    speed = float(val)
    # Get the current position in milliseconds
    current_position_ms = pygame.mixer.music.get_pos()
    print(current_position_ms)
    # Play the audio from the last position with the new speed
    play_audio(loaded_audio, speed, current_position_ms)


# Function to load a file
def load_file():
    global loaded_audio, current_position_ms
    file_path = filedialog.askopenfilename()
    loaded_audio = load_audio(file_path)
    current_position_ms = 0  # Start from the beginning
    play_audio(loaded_audio, 1.0, current_position_ms)  # Play at normal speed initially


# Create the GUI
root = tk.Tk()
root.title("Audio Speed Controller")

# Add a load button
load_button = tk.Button(root, text="Load Audio", command=load_file)
load_button.pack()

# Add a slider to control speed
speed_slider = tk.Scale(root, from_=0.5, to=2.0, resolution=0.01, orient="horizontal", label="Playback Speed",
                        command=on_slider_change)
speed_slider.set(1.0)
speed_slider.pack()

# Start the GUI loop
root.mainloop()
