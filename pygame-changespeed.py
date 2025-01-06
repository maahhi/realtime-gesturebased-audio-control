"""https://chatgpt.com/share/1f85ffdf-8fa4-4129-9018-3607534ae875"""


import pygame
from pydub import AudioSegment
import io
import tkinter as tk
from tkinter import Scale


class MusicPlayer:
    def __init__(self, root, file_path):
        self.file_path = file_path
        self.sound = AudioSegment.from_file(file_path)
        self.current_speed = 1.0
        self.is_playing = False

        # Initialize pygame mixer
        pygame.mixer.init(frequency=self.sound.frame_rate)
        self.position = 0  # Keep track of current position in ms

        # Tkinter setup
        self.root = root
        self.root.title("Music Speed Changer")

        # Speed control slider
        self.speed_slider = Scale(root, from_=0.5, to=2.0, resolution=0.1, orient='horizontal', label='Speed',
                                  command=self.update_speed)
        self.speed_slider.set(self.current_speed)
        self.speed_slider.pack()

        # Play button
        self.play_button = tk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack()

    def change_speed(self, speed):
        # Change the speed of the sound
        altered_sound = self.sound._spawn(self.sound.raw_data, overrides={
            "frame_rate": int(self.sound.frame_rate * speed)
        })
        altered_sound = altered_sound.set_frame_rate(self.sound.frame_rate)
        return altered_sound

    def play_music(self):
        if not self.is_playing:
            self.is_playing = True
            self._play_chunk()

    def _play_chunk(self):
        if not self.is_playing:
            return

        # Calculate the chunk to play
        chunk_length = 1000  # Length of each chunk in ms
        end_position = min(self.position + chunk_length, len(self.sound))
        chunk = self.change_speed(self.current_speed)[self.position:end_position]

        # Convert chunk to a format pygame can use
        sound_buffer = io.BytesIO()
        chunk.export(sound_buffer, format="wav")
        sound_buffer.seek(0)

        # Play the chunk
        pygame.mixer.music.load(sound_buffer)
        pygame.mixer.music.play()

        # Update position for the next chunk
        self.position = end_position

        # Schedule the next chunk, but start it slightly before the current one ends to smooth transition
        if self.position < len(self.sound):
            overlap = 50  # Milliseconds to overlap
            self.root.after(chunk_length - overlap, self._play_chunk)
        else:
            self.is_playing = False

    def stop_music(self):
        self.is_playing = False
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def update_speed(self, value):
        self.current_speed = float(value)
        if self.is_playing:
            self.stop_music()
            self.play_music()

    def on_close(self):
        self.stop_music()
        pygame.mixer.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    file_path = "music.mp3"  # Replace with your music file path
    player = MusicPlayer(root, file_path)
    root.protocol("WM_DELETE_WINDOW", player.on_close)
    root.mainloop()
