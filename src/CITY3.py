import tkinter as tk
from PIL import Image, ImageTk

class GridVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Visualization")
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

        self.bg_image = Image.open(r"C:\Users\HOME\Desktop\Building Bridges\city_bg.png")
        self.bg_image = self.bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.building_image = Image.open(r"C:\Users\HOME\Desktop\Building Bridges\blue_building.png")
        self.building_width = 100
        self.building_height = 150  # Adjusted to a fixed height for each building
        self.floor_height = 30
        self.floors = self.building_height // self.floor_height  

        self.space_between_buildings = 5
        self.space_between_rows = 5

        # Define the grid pattern
        self.grid_pattern = [
            ["#", ".", "#", "#", "#"],
            ["#", ".", "#", ".", "#"],
            ["#", "#", "#", ".", "#"]
        ]
        self.building_photos = []
        self.coordinates = self.generate_coordinates_with_offsets()
        self.visualize()

    def generate_coordinates_with_offsets(self):
        rows = len(self.grid_pattern)
        columns = len(self.grid_pattern[0])

        grid_width = columns * (self.building_width + self.space_between_buildings) - self.space_between_buildings
        grid_height = rows * (self.building_height + self.space_between_rows) - self.space_between_rows

        x_offset = (1500 - grid_width) // 2
        y_offset = (750 - grid_height) // 2

        coordinates = []
        for row in range(rows):
            for col in range(columns):
                if self.grid_pattern[row][col] == "#":
                    x = x_offset + col * (self.building_width + self.space_between_buildings)
                    y = y_offset + row * (self.building_height + self.space_between_rows)
                    coordinates.append((x, y))
        return coordinates

    def visualize(self):
        for (x, y) in self.coordinates:
            self.draw_building(x, y)

    def draw_building(self, x, y):
        outline_color = "#333333"
        outline_width = 3

        # Create the rectangle for the building
        self.canvas.create_rectangle(
            x, y, 
            x + self.building_width, 
            y + self.building_height, 
            fill="gray", 
            outline=outline_color, 
            width=outline_width
        )

        # Resize the building image to fit the building dimensions
        resized_building_image = self.building_image.resize((self.building_width, self.building_height), Image.LANCZOS)
        building_photo = ImageTk.PhotoImage(resized_building_image)

        # Create the image for the building
        self.canvas.create_image(
            x + self.building_width // 2, 
            y + self.building_height // 2, 
            image=building_photo
        )
        self.building_photos.append(building_photo)  # Store the reference

if __name__ == "__main__":
    root = tk.Tk()
    app = GridVisualizer(root)
    root.mainloop()
