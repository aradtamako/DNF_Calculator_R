import gui_main
import tkinter as tk
import data.dataload as dataload

if __name__ == "__main__":
    data_loaded = dataload.DataLoad()

    root = tk.Tk()
    mainGUI = gui_main.MainGUI(root)
    mainGUI.mainloop()
