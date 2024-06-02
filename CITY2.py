import tkinter as tk
from PIL import Image,ImageDraw,ImageTk
root = tk.Tk()

def visualize():
    visualize_window = root
    visualize_window.title("City 2")
    visualize_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    bg_image = Image.open(r"C:\Users\HOME\Desktop\Building Bridges\city_bg.png")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)
    canvas.bg_photo = bg_photo
    
    x1, y1 = 350, 150
    x2, y2 = 455, 150
    x3, y3 = 900, 445

    building_width = 100
    building_height = 150  
    floor_height = 40

    def draw_building_with_floors(x, y, width, height, floor_height, color):
        canvas.create_rectangle(x, y, x + width, y + height, fill=color)
        num_floors = height // floor_height
        for i in range(1, num_floors):
            floor_y = y + i * floor_height
            canvas.create_line(x, floor_y, x + width, floor_y, fill="white")

    draw_building_with_floors(x1, y1, building_width, building_height, floor_height, "black")
    draw_building_with_floors(x2, y2, building_width, building_height, floor_height, "black")
    draw_building_with_floors(x3, y3, building_width, building_height, floor_height, "black")

    building_image = Image.open(r"C:\Users\HOME\Desktop\Building Bridges\blue_building.png")
    building_image = building_image.resize((building_width, building_height), Image.LANCZOS)
    building_photo = ImageTk.PhotoImage(building_image)

    canvas.create_image(x1 + building_width // 2, y1 + building_height // 2, image=building_photo)
    canvas.create_image(x2 + building_width // 2, y2 + building_height // 2, image=building_photo)
    canvas.create_image(x3 + building_width // 2, y3 + building_height // 2, image=building_photo)

    canvas.building_photo = building_photo


visualize()
root.mainloop()
