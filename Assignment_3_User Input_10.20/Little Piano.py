import customtkinter as ctk
import pygame
import numpy as np
from PIL import Image, ImageTk 


# Initialize pygame
pygame.mixer.init()


# Set the Sampling Rate and Duration
sampling_rate = 44100  
duration = 0.7  # Duration of Each Note (s)


# Define Note Frequencies (C Major: do, re, mi, fa, so, la, xi, do)
frequencies = {
    'C4': 261.63,  # do
    'D4': 293.66,  # re
    'E4': 329.63,  # mi
    'F4': 349.23,  # fa
    'G4': 392.00,  # so
    'A4': 440.00,  # la
    'B4': 493.88,  # xi
    'C5': 523.25   # do
}


# Define the Notes of Twinkle, Twinkle, Little Star
melody_notes = ['C4', 'C4', 'G4', 'G4', 'A4', 'A4', 'G4', 
                'F4', 'F4', 'E4', 'E4', 'D4', 'D4', 'C4',
                'G4', 'G4', 'F4', 'F4', 'E4', 'E4', 'D4',
                'G4', 'G4', 'F4', 'F4', 'E4', 'E4', 'D4',
                'C4', 'C4', 'G4', 'G4', 'A4', 'A4', 'G4',
                'F4', 'F4', 'E4', 'E4', 'D4', 'D4', 'C4']
# Define the Corresponding keys
key_to_note = {
    'a': 'C4',
    's': 'D4',
    'd': 'E4',
    'f': 'F4',
    'g': 'G4',
    'h': 'A4',
    'j': 'B4',
    'k': 'C5'
}


# Define a Function that Generates a Sine Wave Note
def generate_tone(frequency, duration, sampling_rate=44100):
    t = np.linspace(0, duration, int(sampling_rate * duration), False)  # Generate Time Series
    wave = 0.6 * np.sin(2 * np.pi * frequency * t)  # Generate Sine Wave
    return wave


# Convert Sine Wave to pygame Usable Sound Formats
def generate_sound(frequency):
    wave = generate_tone(frequency, duration)
    sound_array = np.array([wave, wave]).T  # Create Stereo Array
    sound_array = (sound_array * 32767).astype(np.int16) 
    sound_array = np.ascontiguousarray(sound_array)  
    return pygame.sndarray.make_sound(sound_array)  # Generate Sounds with pygame


# Create pygame Sounds for Each Note
sounds = {note: generate_sound(frequency) for note, frequency in frequencies.items()}


# Create a Window with CustomTkinter
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")  
window = ctk.CTk()
background_frame = ctk.CTkFrame(window, width=600, height=491, fg_color="#fffef5") # Set Background Size and Colour
background_frame.place(relx=0.5, rely=0.5, anchor="center")
window.title("🎵 Little Piano 🎵")
window.geometry("600x491")  # Adjust the Window Length and Width


# Define the Font Style
header_label = ctk.CTkLabel(window, text="🎵 Little Piano 🎵", font=("Verdana", 32,  "bold"), fg_color="#fffef5", text_color="#001c41")
header_label.pack(pady=(40, 10))


instructions_label = ctk.CTkLabel(window, text="✨ Follow the Tip to Play A Song! ✨", font=("Verdana", 17, "bold"), fg_color="#fffef5", text_color="#001c41")
instructions_label.pack(pady=(10, 20))


# Create a Start Button
start_button = ctk.CTkButton(window, text="START", font=("Verdana", 16, "bold"), command=lambda: start_game(), width=150, height=50, text_color="white", fg_color="#94bef5", hover_color="#5e96de", border_width=6,   border_color="#001c41" )
start_button.pack(pady=(10, 20))


# Create a Status Label
status_label = ctk.CTkLabel(window, text="", font=("Verdana", 22, "bold"), fg_color="#fffef5")
status_label.pack(pady=(0, 5))


# Load and Display the Image
def load_and_display_image():
    img = Image.open("F:\S1\SD5913 Creative Programming\Git_Code\pfad\Assignment_3_User Input_10.20\img_piano.jpg") # Need Change the Path
    img = img.resize((394, 254), Image.Resampling.LANCZOS)  
    photo = ImageTk.PhotoImage(img)

    image_label = ctk.CTkLabel(window, image=photo, text="")  # Create a Label and Insert the Image
    image_label.image = photo  
    image_label.pack(side="bottom", pady=30)  # Place the Image at the Bottom of the Window


# Initialise Game State
is_started = False  # Marks if the Game has Started
note_index = 0  # Index of Current Note
show_error = False  


note_to_key = {value: key for key, value in key_to_note.items()}


# Functions to Start the Game
def start_game():
    global is_started, note_index, show_error
    is_started = True
    note_index = 0
    show_error = False
    # Immediately Displays the ‘Next Key’ Tip
    status_label.configure(text=f"Next Key: {note_to_key[melody_notes[note_index]]}", text_color="#ff9600")  


def game_loop():
    global note_index, show_error
    window.update()

    if is_started:
        window.bind("<Key>", key_pressed)
    
    window.after(100, game_loop)  


def key_pressed(event):
    global note_index, show_error
    key_pressed = event.char.lower()
    
    # Check that the Correct Key is Pressed
    expected_note = melody_notes[note_index]
    if key_to_note.get(key_pressed) == expected_note:
        sounds[expected_note].play()
        note_index += 1
        show_error = False  # Reset the Error Display
        
        if note_index < len(melody_notes):
            status_label.configure(text=f"Next Key: {note_to_key[melody_notes[note_index]]}", text_color="#ff9600")  # Update the Next Key to be Pressed
        else:
            status_label.configure(text="Congratulations! You Did it！", text_color="#ff9600")
            start_button.configure(text="RESTART",text_color="white", command=lambda: restart_game())  
    else:
        show_error = True  # Display Error when Pressing Wrong Key
        status_label.configure(text=f"Next Key: {note_to_key[melody_notes[note_index]]}", text_color="#f10000")  


# Restart the Game
def restart_game():
    global is_started, note_index, show_error
    is_started = False
    note_index = 0
    show_error = False
    status_label.configure(text="") 
    start_button.configure(text="START", command=start_game)  
    instructions_label.configure(text="Follow the Tip to Play A Song!")  

    
# Load and Display Image
load_and_display_image()

game_loop()

window.mainloop()
