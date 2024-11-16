import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For handling the background image
from network.path import PathFinder
from tube.map import TubeMap


def get_tubemap():
    """Return an initialized TubeMap object"""
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    return tubemap


def find_shortest_path():
    """Callback function to find the shortest path and display it"""
    start_station = entry_start.get().strip()
    end_station = entry_end.get().strip()

    if not start_station or not end_station:
        result_label.config(text="Please enter both stations.")
        return

    try:
        stations = path_finder.get_shortest_path(start_station, end_station)
        station_names = [station.name for station in stations]
        result_label.config(text=" -> ".join(station_names))
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")


# Initialize the TubeMap and PathFinder
tubemap = get_tubemap()
path_finder = PathFinder(tubemap)

# Create the GUI
root = tk.Tk()
root.title("Tube Shortest Path Finder")
root.geometry("600x400")

# Add a background image
background_image = Image.open("images/background_img.jpg")  # Replace with your image path
background_image = background_image.resize((600, 400))
bg_image = ImageTk.PhotoImage(background_image)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Add input fields
label_start = ttk.Label(root, text="Start Station:", background="#ffffff")
label_start.place(x=150, y=100)

entry_start = ttk.Entry(root, width=30)
entry_start.place(x=250, y=100)

label_end = ttk.Label(root, text="End Station:", background="#ffffff")
label_end.place(x=150, y=150)

entry_end = ttk.Entry(root, width=30)
entry_end.place(x=250, y=150)

# Add a button
find_button = ttk.Button(root, text="Find Shortest Path", command=find_shortest_path)
find_button.place(x=250, y=200)

# Add a result label
result_label = ttk.Label(root, text="", wraplength=500, background="#ffffff")
result_label.place(x=50, y=250)

# Run the main loop
root.mainloop()
