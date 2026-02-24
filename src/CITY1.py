import tkinter as tk
from PIL import Image, ImageTk
import pygame

def visualize(root):
    root.title("City 1")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    # Start the sound before starting the bridge animation
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(r'C:\Users\HOME\Desktop\Building Bridges\block sound') 
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Error playing music:", e)
        
    bg_image = Image.open(r"C:\Users\HOME\Desktop\Building Bridges\city_bg.png")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)
    canvas.bg_photo = bg_photo

    x1, y1 = 370, 209
    x2, y2 = 870, 209
    x4, y4 = 370, 449
    x5, y5 = 870, 449
    x3, y3 = 625, 329

    building_width = 100
    building_height = 150  
    floor_height = 30

    def draw_building_with_floors(x, y, width, height, floor_height, color):
        canvas.create_rectangle(x, y, x + width, y + height, fill=color)
        num_floors = height // floor_height
        for i in range(1, num_floors):
            floor_y = y + i * floor_height
            canvas.create_line(x, floor_y, x + width, floor_y, fill="white")

    draw_building_with_floors(x1, y1, building_width, building_height, floor_height, "black")
    draw_building_with_floors(x2, y2, building_width, building_height, floor_height, "black")
    draw_building_with_floors(x4, y4, building_width, building_height, floor_height, "black")
    draw_building_with_floors(x5, y5, building_width, building_height, floor_height, "black")
    draw_building_with_floors(x3, y3, building_width, building_height, floor_height, "black")

    def draw_bridge(canvas, x1, y1, x2, y2):
        canvas.create_rectangle(x1, y1, x2, y2, fill="#8DBFC6")

    def animate_bridge(x1, y1, x2, y2):
        bridge_drawn = False
        def draw():
            nonlocal bridge_drawn
            nonlocal x1
            if not bridge_drawn:
                draw_bridge(canvas, x1, y1, x1 + 10, y2)
                x1 += 10
                if x1 >= x2:
                    bridge_drawn = True
                    pygame.mixer.music.stop()
                else:
                    root.after(150, draw)
        
        draw()

    # Animate bridge from x4,y4 to x3,y3
    animate_bridge(x4 + building_width, y4, x3, y3 + 150)
    # Animate bridge from x3,y3 to x2,y2
    animate_bridge(x3 + building_width, y3, x2, y2 + 150)  
    # Animate bridge from x1,y1 to x3,y3
    animate_bridge(x1 + building_width, y1 + 120, x3, y3 + 30) 
    # Animate bridge from x3,y3 to x5,y5
    animate_bridge(x3 + building_width, y4, x5, y5 + 30)

    # Load images to place on buildings
    building_image = Image.open(r"C:\Users\HOME\Desktop\Building Bridges\blue_building.png")
    building_image = building_image.resize((building_width, building_height), Image.LANCZOS)
    building_photo = ImageTk.PhotoImage(building_image)

    # Place the images on the buildings
    canvas.create_image(x1 + building_width // 2, y1 + building_height // 2, image=building_photo)
    canvas.create_image(x2 + building_width // 2, y2 + building_height // 2, image=building_photo)
    canvas.create_image(x4 + building_width // 2, y4 + building_height // 2, image=building_photo)
    canvas.create_image(x5 + building_width // 2, y5 + building_height // 2, image=building_photo)
    canvas.create_image(x3 + building_width // 2, y3 + building_height // 2, image=building_photo)

    # Keep a reference to the PhotoImage object to prevent it from being garbage collected
    canvas.building_photo = building_photo

root = tk.Tk()
visualize(root)
root.mainloop()
