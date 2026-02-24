import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import pygame

def play_click_sound():
    click_sound = pygame.mixer.Sound(r'C:\Users\HOME\Desktop\Building Bridges\button.mp3')
    click_sound.play()

def fore(root):
    fore_frame = tk.Frame(root)
    fore_frame.pack()
    
    pygame.mixer.init()
    pygame.mixer.music.load(r'C:\Users\HOME\Desktop\Building Bridges\window_sound.mp3') 
    pygame.mixer.music.play(-1) 

    bg_image = Image.open(r"C:\Users\HOME\Desktop\Building Bridges\new alontville.png")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(fore_frame, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack()
    
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)
    canvas.bg_photo = bg_photo

    def on_ok_click():
        play_click_sound()
        widgets(root)

    ok_button = tk.Button(fore_frame, text="OK", command=on_ok_click, width=10, height=2)
    ok_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def widgets(root):
    subprocess.Popen(['python', r'C:\Users\HOME\Desktop\Building Bridges\main.py'], shell=True)
    root.destroy()

root = tk.Tk()
fore(root)
root.mainloop()
