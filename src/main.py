import tkinter as tk
from tkinter import ttk
from gui import TimeTrackingAppGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingAppGUI(root)
    root.mainloop()