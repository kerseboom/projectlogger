# main.py
import tkinter as tk
from gui import TimeTrackingApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()
