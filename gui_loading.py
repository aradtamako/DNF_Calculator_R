import tkinter
import common


class LoadingGUI:
    def __init__(self, parent):
        self.colors = common.load_color()  # [dark_main, dark_sub, dark_blue, result_sub]
        self.fonts = common.load_font()  # [guide_font, small_font, mid_font, big_font]
        self.parent = parent
        self.loading_canvas = None

    def start_gui(self):
        self.create_main()

    def create_main(self):
        self.loading_canvas = tkinter.Canvas(self.parent, width=1000, height=800, bd=0, bg=self.colors[0])
        self.loading_canvas.place(x=-2, y=-2)











