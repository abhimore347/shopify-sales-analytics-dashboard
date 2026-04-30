import tkinter as tk
from gui import App

root = tk.Tk()
root.title("Sales Dashboard")
root.state('zoomed')

app = App(root)
root.mainloop()