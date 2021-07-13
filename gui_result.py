import threading
import tkinter
import common

equipment_image_position = {
    "11": [57, 57], "12": [27, 87], "13": [27, 57], "14": [57, 87], "15": [27, 117],
    "21": [189, 87], "22": [219, 87], "23": [219, 117],
    "31": [189, 117], "32": [219, 147], "33": [189, 147],
    "41": [27, 147], "55": [57, 147]
}


class ResultGUI:
    def __init__(self, parent, image_equipment, image_extra):
        self.colors = common.load_color()  # [dark_main, dark_sub, dark_blue, result_sub]
        self.fonts = common.load_font()  # [guide_font, small_font, mid_font, big_font]
        self.parent = parent
        self.image_equipment = image_equipment
        self.image_extra = image_extra
        self.result_canvas = None
        self.canvas_widget = {}
        self.result_values = None
        self.result_equipments = None
        self.result_tran = None
        self.result_stat = None
        self.result_level = None

        # 0: 종합, 1: 그로기, 2: 지딜, 3: 각성기
        self.now_rank_toggle = 0
        self.now_rank_selected = 0

        # 그래프용 max_min 지정
        self.tran_max = 0
        self.tran_min = 0

    def get_result_data(
            self, result_values_sum, result_equipments_sum, result_tran_sum,
            result_stat_sum, ranked_result_level_sum
    ):
        # 0: 종합, 1: 그로기, 2: 지딜, 3: 각성기
        self.result_values = result_values_sum
        self.result_equipments = result_equipments_sum
        self.result_tran = result_tran_sum
        self.result_stat = result_stat_sum
        self.result_level = ranked_result_level_sum

    def start_gui(self):
        self.now_rank_toggle = 0
        self.now_rank_selected = 0
        self.create_main()
        threading.Thread(target=self.create_ranks_section).start()
        threading.Thread(target=self.create_equipment_section).start()
        threading.Thread(target=self.create_stat_section).start()
        self.tran_detail_graph()
        self.tran_detail_graph_compare(1, 1)
        # threading.Thread(target=self.tran_detail_graph).start()
        # threading.Thread(target=self.tran_detail_graph2).start()

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
            if now_damage_value > 10000:
                now_damage_show = str(int(now_damage_value / 1000)) + "K"
            else:
                now_damage_show = str(int(now_damage_value * 100)) + "%"
            self.canvas_widget["rank_value_" + str(now_rank)] = self.result_canvas.create_text(
                620, 30 + 78 * now_rank, text=now_damage_show, font=self.fonts[2], fill='white',
                anchor="w", tag="rank"
            )
            for equipment in now_result_equipments[now_rank]:
                if len(equipment) == 6:
                    self.canvas_widget["rank_img_" + str(now_rank) + "_weapon"] = self.result_canvas.create_image(
                        767, 31 + 78 * now_rank, image=self.image_equipment[equipment + 'n.png'],
                        tag="rank"
                    )

            for tg, part in enumerate([11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33]):
                for equipment in now_result_equipments[now_rank]:
                    if len(equipment) == 6:  # 무기
                        continue
                    elif len(equipment) == 4:  # 세트
                        continue
                    elif equipment[0:2] == str(part):
                        self.canvas_widget["rank_img_" + str(now_rank) + "_" + str(part)] = \
                            self.result_canvas.create_image(
                                593 + tg * 29, 62 + 78 * now_rank, image=self.image_equipment[equipment + 'n.png'],
                                tag="rank")
            for tg, part in enumerate([41, 55]):
                for equipment in now_result_equipments[now_rank]:
                    if equipment[0:2] == str(part):
                        self.canvas_widget["rank_img_" + str(now_rank) + "_" + str(part)] = \
                            self.result_canvas.create_image(
                                796 + tg * 29, 31 + 78 * now_rank, image=self.image_equipment[equipment + 'n.png'],
                                tag="rank")

    def create_equipment_section(self):
        now_show_equipments = self.result_equipments[self.now_rank_toggle][self.now_rank_selected]
        for tg, part in enumerate([11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33, 41, 55]):
            for equipment in now_show_equipments:
                if len(equipment) == 6:  # 무기
                    continue
                elif len(equipment) == 4:  # 세트
                    continue
                elif equipment[0:2] == str(part):
                    position = equipment_image_position[str(part)]
                    self.canvas_widget["equipment_img_" + str(part)] = self.result_canvas.create_image(
                        position[0], position[1], image=self.image_equipment[equipment + 'n.png'],
                        tag="equipment"
                    )
        for equipment in now_show_equipments:
            if len(equipment) == 6:
                self.canvas_widget["equipment_img_weapon"] = self.result_canvas.create_image(
                    189, 57, image=self.image_equipment[equipment + 'n.png'],
                    tag="equipment"
                )

    def tran_detail_graph(self):
        now_tran_values = self.result_tran[self.now_rank_toggle][self.now_rank_selected]
        if now_tran_values == [0]:
            print("tran 자료 없음")
        else:
            print("tran 그래프 생성 시작")
            self.tran_max = 0
            for i in range(len(self.result_tran[self.now_rank_toggle])):
                now_max = max(self.result_tran[self.now_rank_toggle][i])
                if now_max > self.tran_max:
                    self.tran_max = now_max
            start_point = [42, 675]
            for i in range(0, 400):
                now_value = now_tran_values[i * 3]
                now_y = int(start_point[1] - 220 * (now_value / self.tran_max))
                self.result_canvas.create_line(42 + i, now_y, 42 + i + 1, now_y, fill='white', width=1)
            self.result_canvas.create_line(
                42, 675, 42, 455, 442, 455, 442, 675, 42, 675, fill='gray', width=2,
                tag="tran_graph_now"
            )

    def tran_detail_graph_compare(self, compare_rank, toggle):
        try:
            now_tran_values = self.result_tran[self.now_rank_toggle][compare_rank]
        except IndexError:
            return
        if now_tran_values == [0]:
            print("tran 자료 없음")
        else:
            print("tran 그래프 생성 시작")
            start_point = [42, 675]
            for i in range(0, 400):
                now_value = now_tran_values[i * 3]
                now_y = int(start_point[1] - 220 * (now_value / self.tran_max))
                self.result_canvas.create_line(
                    42 + i, now_y, 42 + i + 1, now_y, fill='red', width=1,
                    tag="tran_graph_compare_" + str(toggle)
                )

    def create_stat_section(self):
        now_stat = self.result_stat[self.now_rank_toggle][self.now_rank_selected]
        now_level = self.result_level[self.now_rank_toggle][self.now_rank_selected]
        print(now_stat)
        print(now_level)
        max_stat = max([now_stat[2], now_stat[3], now_stat[4], now_stat[6], now_stat[7], now_stat[8]])

        self.result_canvas.create_polygon(
            125, 200, 200, 240, 200, 330, 125, 370, 50, 330, 50, 240, 125, 200,
            fill='gray21', outline='black', width=2)
        self.result_canvas.create_text(125, 200, anchor='s', text='증뎀\n' + str(round(now_stat[2], 1)) + "%"
                                       , fill='white', font=self.fonts[1])
        self.result_canvas.create_text(200, 240, anchor='sw', text='크증\n' + str(round(now_stat[3], 1)) + "%"
                                       , fill='white', font=self.fonts[1])
        self.result_canvas.create_text(200, 330, anchor='nw', text='추뎀\n' + str(round(now_stat[4], 1)) + "%"
                                       , fill='white', font=self.fonts[1])
        self.result_canvas.create_text(125, 370, anchor='n', text='모공\n' + str(round(now_stat[6], 1)) + "%"
                                       , fill='white', font=self.fonts[1])
        self.result_canvas.create_text(50, 330, anchor='ne', text='공%\n' + str(round(now_stat[7], 1)) + "%"
                                       , fill='white', font=self.fonts[1])
        self.result_canvas.create_text(50, 240, anchor='se', text='스탯\n' + str(round(now_stat[8], 1)) + "%"
                                       , fill='white', font=self.fonts[1])
        point = [[], [], [], [], [], []]
        # 중간 지점 좌표 = (125, 285)
        point[0] = [125, int(285 - 85 * now_stat[2] / max_stat)]
        point[1] = [int(125 + 75 * now_stat[3] / max_stat), int(285 - 45 * now_stat[3] / max_stat)]
        point[2] = [int(125 + 75 * now_stat[4] / max_stat), int(285 + 45 * now_stat[4] / max_stat)]
        point[3] = [125, int(285 + 85 * now_stat[6] / max_stat)]
        point[4] = [int(125 - 75 * now_stat[7] / max_stat), int(285 + 45 * now_stat[7] / max_stat)]
        point[5] = [int(125 - 75 * now_stat[8] / max_stat), int(285 - 45 * now_stat[8] / max_stat)]
        self.result_canvas.create_polygon(
            point[0][0], point[0][1],
            point[1][0], point[1][1],
            point[2][0], point[2][1],
            point[3][0], point[3][1],
            point[4][0], point[4][1],
            point[5][0], point[5][1],
            point[0][0], point[0][1],
            fill='slate blue', outline='dark slate blue', width=1)
        self.result_canvas.create_line(125, 200, 125, 370, fill='gray50', width=1)
        self.result_canvas.create_line(200, 240, 50, 330, fill='gray50', width=1)
        self.result_canvas.create_line(200, 330, 50, 240, fill='gray50', width=1)









