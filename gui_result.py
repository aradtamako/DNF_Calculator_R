import threading
import tkinter
import common


class ResultGUI:
    def __init__(self, parent, image_equipment, image_extra, image_weapon):
        self.colors = common.load_color()  # [dark_main, dark_sub, dark_blue, result_sub]
        self.fonts = common.load_font()  # [guide_font, small_font, mid_font, big_font]
        self.parent = parent
        self.image_equipment = image_equipment
        self.image_extra = image_extra
        self.image_weapon = image_weapon
        self.result_canvas = None
        self.canvas_widget = {}
        self.result_values = None
        self.result_equipments = None
        self.result_tran = None

        # 0: 종합, 1: 그로기, 2: 지딜, 3: 각성기
        self. now_rank_toggle = 0

    def get_result_data(self, result_values_sum, result_equipments_sum, result_tran_sum):
        # 0: 종합, 1: 그로기, 2: 지딜, 3: 각성기
        self.result_values = result_values_sum
        self.result_equipments = result_equipments_sum
        self.result_tran = result_tran_sum

    def start_gui(self):
        self.now_rank_toggle = 0
        self.create_main()
        threading.Thread(target=self.create_ranks_section).start()

    def create_main(self):
        self.result_canvas = tkinter.Canvas(self.parent, width=1000, height=800, bd=0, bg=self.colors[0])
        self.result_canvas.place(x=-2, y=-2)
        self.result_canvas.create_image(0, 0, image=self.image_extra["bg_big_result.png"], anchor='nw')
        tkinter.Button(self.parent, text="닫기", command=self.result_canvas.destroy).place(x=0, y=0)

    def create_ranks_section(self):
        now_result_values = self.result_values[self.now_rank_toggle]
        now_result_equipments = self.result_equipments[self.now_rank_toggle]

        for now_rank in range(len(now_result_values)):
            if now_rank == 9:
                break

            now_damage_value = now_result_values[now_rank]

            for tg, part in enumerate([11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33]):
                for equipment in now_result_equipments[now_rank]:
                    if len(equipment) == 6:  # 무기
                        pass
                    elif equipment[0:2] == str(part):
                        self.result_canvas.create_image(
                            593 + tg * 29, 62 + 78 * now_rank, image=self.image_equipment[equipment + 'n.png']
                        )
            for tg, part in enumerate([41, 55]):
                for equipment in now_result_equipments[now_rank]:
                    if equipment[0:2] == str(part):
                        self.result_canvas.create_image(
                            753 + tg * 29, 32 + 78 * now_rank, image=self.image_equipment[equipment + 'n.png']
                        )



