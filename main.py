import gui_main
import tkinter as tk
import data.dataload as dataload
import multiprocessing as mp

"""
pyinstaller -w --onefile --icon="./ext_img/icon.ico" main.py
"""

if __name__ == '__main__':
    mp.freeze_support()
    data_loaded = dataload.DataLoad()

    root = tk.Tk()
    mainGUI = gui_main.MainGUI(root)
    mainGUI.mainloop()
