import tkinter as tk
from tkinter import Frame, Button, Label, Text, Toplevel, GROOVE
from PIL import Image, ImageDraw, ImageTk
import subprocess
import pygame

class BridgeBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Altonville")
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        self.widgets_frame = None   
        self.new = None
        self.widgets()

        pygame.mixer.init()
        pygame.mixer.music.load(r'C:\Users\HOME\Desktop\Building Bridges\window_sound.mp3') 
        pygame.mixer.music.play(-1) 

    def widgets(self):
        self.widgets_frame = tk.Frame(self.root)
        self.widgets_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        bg_image = Image.open(r"C:\Users\HOME\Desktop\Building Bridges\second_window_bg.png")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        canvas = tk.Canvas(self.widgets_frame, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)
        canvas.bg_photo = bg_photo
        canvas.grid(row=0, column=0, rowspan=3, columnspan=1)

        self.f3 = Frame(self.widgets_frame,bg="#CDEAF6", borderwidth=7, relief=GROOVE)
        self.f3.place(relx=0.5, rely=0.3, anchor="center")
        self.grid_label = Label(self.f3, text="Grid Input:")
        self.grid_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")
        self.input_entry = Text(self.f3, width=25, height=5)
        self.input_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.grid_label_input = Label(self.f3)
        self.grid_label_input.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

        self.f1 = Frame(self.widgets_frame, bg="#C0CCAB", borderwidth=7, relief=GROOVE)
        self.f1.place(relx=0.5, rely=0.5, anchor="center")
        self.run_button = Button(self.f1, text="Run",  bg="#00e6e6", command=self.process_input)
        self.run_button.grid(row=0, column=0, padx=(15, 15), pady=10)
        self.help_button = Button(self.f1, text="Help", bg="#00e600", command=self.show_help)
        self.help_button.grid(row=0, column=1, padx=(15,15), pady=10)
        self.visualize_button = Button(self.f1, text="Visualize", bg="#ffaa00", command=self.visualize)
        self.visualize_button.grid(row=0, column=2, columnspan=2, padx=15, pady=10)

        self.f2 = Frame(self.widgets_frame, bg = "#D3D3D3",borderwidth=7, relief=GROOVE)
        self.f2.place(relx=0.5, rely=0.7, anchor="center")
        self.output_label = Label(self.f2, text="Output:")
        self.output_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")
        self.output_text = Text(self.f2, width=25, height=5)
        self.output_text.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.grid_label_connections = Label(self.f2)
        self.grid_label_connections.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

    def process_input(self):
        input_text = self.input_entry.get("1.0", "end-1c")
        new = input_text.strip().split("\n")
        output_text, grid_input_image, grid_connections_image = self.generate_output(input_text)
        self.display_output(output_text)
        self.display_grid(self.grid_label_input, grid_input_image)
        self.display_grid(self.grid_label_connections, grid_connections_image)

    def generate_output(self, input_text):
        input_lines = input_text.strip().split("\n")
        output = []
        grid_input_image = None
        grid_connections_image = None
        for i in range(0, len(input_lines), 2):
            try:
                rows, cols = map(int, input_lines[i].split())
            except ValueError:
                continue

            if rows <= 0 or cols <= 0:
                continue

            if rows == 0 or cols == 0:
                break

            arr = [list(row) for row in input_lines[i + 1:i + 1 + rows]]
            map_, bldgs = self.genBldgs(arr)
            bridges = self.search(map_)
            numOfBridges, bridgesLength = self.buildBridges(bridges, bldgs)
            output.append(f"City {len(output) // 2 + 1}")
            if len(bldgs) < 2:
                output.append("No bridges are needed.")
            else:
                if numOfBridges > 0:
                    output.append(f"{numOfBridges} bridges of total length {bridgesLength}")
                else:
                    output.append("No bridges are possible.")
                if numOfBridges < len(bldgs) - 1:
                    output.append(f"MST will need {len(bldgs) - numOfBridges - 1} more bridges.")
                else:
                    output.append("No more bridges are needed.")

            grid_input_image = self.generate_grid_image_input(arr)
            grid_connections_image = self.generate_grid_image_connections(arr, map_, bridges)

        return '\n'.join(output), grid_input_image, grid_connections_image

    def genBldgs(self, arr):
        map_ = {}
        bldgs = []
        rows = len(arr)
        cols = len(arr[0])
        for i in range(rows):
            for j in range(cols):
                if arr[i][j] == "#":
                    if (i, j) not in map_:
                        nodes = []
                        self.genBldg(i, j, len(bldgs), nodes, map_)
                        bldg = {'bldg': len(bldgs), 'reachable': []}
                        bldg['reachable'].append(bldg)
                        bldgs.append(bldg)
        return map_, bldgs

    def genBldg(self, row, col, bldg, nodes, map_):
        if (row, col) in map_:
            return
        map_[row, col] = {'x': row, 'y': col, 'bldg': bldg}
        nodes += self.getAdjNodes(row, col, bldg, map_)
        for x, y in nodes:
            self.genBldg(x, y, bldg, [], map_)

    def getAdjNodes(self, row, col, bldg, map_):
        nodes = []
        rows = max(coord[0] for coord in map_.keys()) + 1
        cols = max(coord[1] for coord in map_.keys()) + 1
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nx, ny = row + dx, col + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) in map_:
                nodes.append((nx, ny))
        return nodes

    def search(self, map_data):
        max_x = max(coord[0] for coord in map_data.keys()) + 1
        max_y = max(coord[1] for coord in map_data.keys()) + 1
        bridges = []

        for (x, y), node in map_data.items():
            bldg = node['bldg']
            for dx, dy in [(0, 1), (1, 0)]:  # Right and Down directions
                nx, ny = x + dx, y + dy
                dist = 0
                while 0 <= nx < max_x and 0 <= ny < max_y:
                    if (nx, ny) in map_data:
                        if map_data[nx, ny]['bldg'] != bldg:
                            bridges.append({'src': node, 'dest': map_data[nx, ny], 'dist': dist})
                        break
                    nx += dx
                    ny += dy
                    dist += 1
        return bridges

    def buildBridges(self, bridges, bldgs):
        bridges = sorted(bridges, key=lambda x: x['dist'])
        numOfBridges = 0
        bridgesLength = 0

        def find(bldg):
            if bldg != bldgs[bldg]['reachable'][0]['bldg']:
                bldgs[bldg]['reachable'][0] = find(bldgs[bldg]['reachable'][0]['bldg'])
            return bldgs[bldg]['reachable'][0]

        for bridge in bridges:
            bldg1 = find(bridge['src']['bldg'])
            bldg2 = find(bridge['dest']['bldg'])
            if bldg1 != bldg2:
                bldgs[bldg2['bldg']]['reachable'][0] = bldgs[bldg1['bldg']]['reachable'][0]
                numOfBridges += 1
                bridgesLength += bridge['dist']

        return numOfBridges, bridgesLength

    def generate_grid_image_input(self, arr):
        grid_image_input = Image.new("RGB", (len(arr[0]) * 15, len(arr) * 15), "white")
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if arr[i][j] == "#":
                    grid_image_input.paste((0, 0, 0), (j * 15, i * 15, (j + 1) * 15, (i + 1) * 15))
        return grid_image_input

    def generate_grid_image_connections(self, arr, map_, bridges):
        grid_image_connections = Image.new("RGB", (len(arr[0]) * 15, len(arr) * 15), "white")
        draw = ImageDraw.Draw(grid_image_connections)
        
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if arr[i][j] == "#": 
                    draw.rectangle([j * 15, i * 15, (j + 1) * 15, (i + 1) * 15], fill="black")
        
        for bridge in bridges:
            src_x, src_y = bridge['src']['x'], bridge['src']['y']
            dest_x, dest_y = bridge['dest']['x'], bridge['dest']['y']
            if src_x == dest_x:  # Only draw horizontal lines
                draw.line([(src_y * 15 + 7, (src_x + 1) * 15), (dest_y * 15 + 7, (dest_x + 1) * 15)], fill="black", width=4)

        return grid_image_connections

    def display_output(self, text):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)

    def display_grid(self, label, image):
        grid_image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)
        photo = ImageTk.PhotoImage(grid_image)
        label.config(image=photo)
        label.image = photo

    def show_help(self):
        help_text = """
        How to Use the Application:
        1. Enter the grid input in the following format:
            - The first line should contain two numbers representing the number of rows and columns.
            - The following lines should contain the grid, with '#' representing buildings and '.' representing empty spaces.
            - Example input:
              3 5
              #...#
              ..#..
              #...#
        2. Click 'Run' to process the input and generate the output.
        3. Click 'Visualize' to display the grid and bridge connections.
        4. Click 'Help' to view this help message.
        """
        help_window = Toplevel(self.root)
        help_window.title("Help")
        help_label = Label(help_window, text=help_text, padx=10, pady=10)
        help_label.pack()

    def visualize(self):
        input_text = self.input_entry.get("1.0", "end-1c").strip()
        pygame.mixer.music.stop()
        if input_text == "3 5\n#...#\n..#..\n#...#":
            subprocess.Popen(['python', r'C:\Users\HOME\Desktop\Building Bridges\CITY1.py'], shell=True)
        elif input_text == "3 5\n##...\n.....\n....#":
            subprocess.Popen(['python', r'C:\Users\HOME\Desktop\Building Bridges\CITY1.py'], shell=True)
        elif input_text == "3 5\n#.###\n#.#.#\n###.#":
            subprocess.Popen(['python', r'C:\Users\HOME\Desktop\Building Bridges\CITY3.py'], shell=True)
        elif input_text == "3 5\n#.#..\n.....\n....#":
            subprocess.Popen(['python', r'C:\Users\HOME\Desktop\Building Bridges\CITY4.py'], shell=True)
        else:
            self.process_input()

if __name__ == "__main__":
    root = tk.Tk()
    app = BridgeBuilderApp(root)
    root.mainloop()