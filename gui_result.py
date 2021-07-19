import sys
import threading
import tkinter
import tkinter.ttk
import common

equipment_image_position = {
    "11": [57, 57], "12": [27, 87], "13": [27, 57], "14": [57, 87], "15": [27, 117],
    "21": [189, 87], "22": [219, 87], "23": [219, 117],
    "31": [189, 117], "32": [219, 147], "33": [189, 147],
    "41": [27, 147], "55": [57, 147]
}


class ResultGUI:
    def __init__(self, parent, image_equipment, image_extra, dropdown_list):
        self.colors = common.load_color()  # [dark_main, dark_sub, dark_blue, result_sub]
        self.fonts = common.load_font()  # [guide_font, small_font, mid_font, big_font]
        self.parent = parent
        self.image_equipment = image_equipment
        self.image_extra = image_extra
        self.dropdown_list = dropdown_list
        self.result_canvas = None
        self.canvas_widget = {}
        self.result_values = None
        self.result_equipments = None
        self.result_tran = None
        self.result_stat = None
        self.result_level = None
        self.result_base = None
        self.result_cool = None
        self.result_all = None
        self.result_invert = None

        self.now_creature = "크증18%"

        # 0: 종합, 1: 그로기, 2: 지딜, 3: 각성기
        self.now_rank_toggle = 0
        self.now_rank_selected = 0

        # 그래프용 max_min 지정
        self.tran_max = 0
        self.tran_min = 0

    def get_result_data(
            self, result_values_sum, result_equipments_sum, result_tran_sum,
            result_stat_sum, ranked_result_level_sum, ranked_result_base_sum, ranked_result_cool_sum,
            ranked_result_all_sum, ranked_result_invert_sum
    ):
        self.result_values = result_values_sum  # 순위 최종값
        self.result_equipments = result_equipments_sum  # 장비 리스트
        self.result_tran = result_tran_sum  # tran 시뮬레이션
        self.result_stat = result_stat_sum  # 스탯
        self.result_level = ranked_result_level_sum  # 레벨링
        self.result_base = ranked_result_base_sum  # 순수 데미지
        self.result_cool = ranked_result_cool_sum  # 구간별 쿨감
        # 0: 종합, 1: 그로기, 2: 지딜, 3: 각성기
        self.result_all = ranked_result_all_sum  # 모든 데미지값
        self.result_invert = ranked_result_invert_sum  # 연옥 변환 옵션

    def start_gui(self):
        self.now_rank_toggle = 0
        self.now_rank_selected = 0
        self.create_main()
        self.create_background()
        self.create_base_section()
        self.create_ranks_section()
        self.create_equipment_section()
        self.create_stat_section()
        if self.result_tran[0][0] != [0]:
            self.create_tran_background()
        self.tran_detail_graph()

    def delete_widget_all(self, tag):
        while len(self.result_canvas.find_withtag(tag)) != 0:
            self.result_canvas.delete(tag)

    def rank_select(self, e, rank_num):
        self.now_rank_selected = rank_num
        self.delete_widget_all('rank_select')
        self.create_equipment_section()
        self.create_stat_section()
        self.tran_detail_graph()

    def rank_toggle(self, e, toggle_num):
        self.now_rank_toggle = toggle_num
        for i in range(4):
            if toggle_num == i:
                string_png = f'result_sort_{i + 1}n.png'
            else:
                string_png = f'result_sort_{i + 1}f.png'
            self.result_canvas.itemconfig(
                self.canvas_widget[f'sort{i + 1}'], image=self.image_extra[string_png]
            )
        self.delete_widget_all('rank_toggle')
        self.create_ranks_section()
        self.rank_select(0, 0)

    def create_main(self):
        self.result_canvas = tkinter.Canvas(self.parent, width=1000, height=800, bd=0, bg=self.colors[0])
        self.result_canvas.place(x=-2, y=-2)
        self.result_canvas.create_image(0, 0, image=self.image_extra["bg_big_result.png"], anchor='nw')

        def destroy_result(*e):
            self.result_canvas.destroy()
            try:
                for i in range(3):
                    self.canvas_widget['tran_dropdown' + str(i) + '_rank'].destroy()
                    self.canvas_widget['tran_dropdown' + str(i) + '_type'].destroy()
            except KeyError:
                pass
            self.parent.protocol('WM_DELETE_WINDOW', sys.exit)
        self.parent.protocol('WM_DELETE_WINDOW', destroy_result)
        self.parent.bind('<Escape>', destroy_result)

    def create_ranks_section(self):
        now_result_values = self.result_values[self.now_rank_toggle]
        now_result_equipments = self.result_equipments[self.now_rank_toggle]

        for now_rank in range(len(now_result_values)):
            if now_rank == 8:
                break

            self.canvas_widget["rank_btn_" + str(now_rank)] = self.result_canvas.create_image(
                837, 30 + 78 * now_rank, image=self.image_extra['show_detail2.png'],
                anchor="w", tag="rank_toggle"
            )
            self.result_canvas.tag_bind(self.canvas_widget["rank_btn_" + str(now_rank)],
                                        "<Button-1>", lambda e, rank=now_rank: self.rank_select(e, rank))

            now_damage_value = now_result_values[now_rank]
            if now_damage_value > 10000:
                now_damage_show = str(int(now_damage_value / 1000)) + "K"
            else:
                now_damage_show = str(int(now_damage_value * 100)) + "%"
            self.canvas_widget["rank_value_" + str(now_rank)] = self.result_canvas.create_text(
                620, 30 + 78 * now_rank, text=now_damage_show, font=self.fonts[2], fill='white',
                anchor="w", tag="rank_toggle"
            )
            for equipment in now_result_equipments[now_rank]:
                if len(equipment) == 6:
                    self.canvas_widget["rank_img_" + str(now_rank) + "_weapon"] = self.result_canvas.create_image(
                        738, 31 + 78 * now_rank, image=self.image_equipment[equipment + 'n.png'],
                        tag="rank_toggle"
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
                                tag="rank_toggle")
            for tg, part in enumerate([41, 55]):
                for equipment in now_result_equipments[now_rank]:
                    if equipment[0:2] == str(part):
                        self.canvas_widget["rank_img_" + str(now_rank) + "_" + str(part)] = \
                            self.result_canvas.create_image(
                                767 + tg * 29, 31 + 78 * now_rank, image=self.image_equipment[equipment + 'n.png'],
                                tag="rank_toggle")

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
                        tag="rank_select"
                    )
        for equipment in now_show_equipments:
            if len(equipment) == 6:
                self.canvas_widget["equipment_img_weapon"] = self.result_canvas.create_image(
                    189, 57, image=self.image_equipment[equipment + 'n.png'],
                    tag="rank_select"
                )

    def tran_detail_graph(self):
        now_tran_values = self.result_tran[self.now_rank_toggle][self.now_rank_selected]
        if now_tran_values == [0]:
            print("tran 자료 없음")
            self.result_canvas.create_text(
                270, 565, text="-시간 경과별 계수 그래프 미지원 직업-", fill='white', font=self.fonts[2],
                tag="rank_select"
            )
        else:
            print("tran 그래프 생성 시작")
            self.tran_max = 0
            self.tran_min = 999999999999
            for i in range(len(self.result_tran[self.now_rank_toggle])):
                now_max = max(self.result_tran[self.now_rank_toggle][i])
                now_min = min(self.result_tran[self.now_rank_toggle][i])
                if now_max > self.tran_max:
                    self.tran_max = now_max
                if now_min < self.tran_min:
                    self.tran_min = now_min
            self.tran_min = self.tran_min * 0.7
            start_point = [42, 675]
            for i in range(0, 400):
                now_value = now_tran_values[i * 3]
                now_y = int(start_point[1] - 220 * (now_value - self.tran_min) / (self.tran_max - self.tran_min))
                self.result_canvas.create_line(42 + i, now_y, 42 + i + 1, now_y, fill='white', width=1,
                                               tag="rank_select")

    def create_tran_background(self):
        self.result_canvas.create_polygon(
            42, 675, 42, 455, 442, 455, 442, 675, 42, 675, fill='gray10', outline='gray', width=2
        )
        self.result_canvas.create_polygon(
            108, 674, 108, 456, 143, 456, 143, 674, 108, 674, fill=_from_rgb((40, 10, 10)), width=0
        )
        self.result_canvas.create_polygon(
            143, 674, 143, 456, 175, 456, 175, 674, 143, 674, fill=_from_rgb((10, 40, 10)), width=0
        )
        self.result_canvas.create_polygon(
            375, 674, 375, 456, 441, 456, 441, 674, 375, 674, fill=_from_rgb((10, 10, 40)), width=0
        )
        self.result_canvas.create_line(175, 673, 175, 455, fill='gray', width=1)
        self.result_canvas.create_text(42, 683, text='0', fill='white', font=self.fonts[1])
        self.result_canvas.create_text(108, 683, text='20s', fill='white', font=self.fonts[1])
        self.result_canvas.create_text(142, 683, text='30s', fill='white', font=self.fonts[1])
        self.result_canvas.create_text(175, 683, text='40s', fill='white', font=self.fonts[1])
        self.result_canvas.create_text(375, 683, text='100s', fill='white', font=self.fonts[1])
        self.result_canvas.create_text(442, 683, text='120s', fill='white', font=self.fonts[1])
        self.result_canvas.create_text(242, 433, text='<시간 경과별 데미지 그래프>',
                                       fill='white', font=self.fonts[2])
        self.result_canvas.create_text(503, 454, text='<비교 선택>',
                                       fill='white', font=self.fonts[0])
        rank_num = len(self.result_values[0])
        tran_dropdown_list = ['X']
        tran_dropdown_types = ['종합', '순간', '지속', '각성']
        for i in range(rank_num):
            tran_dropdown_list.append(str(i+1)+'위')

        def create_tran_compare(e, index):
            colors = ['red', 'SteelBlue1', 'green2']
            toggle = tran_dropdown_types.index(self.canvas_widget['tran_dropdown' + str(index) + '_type'].get())
            rank = self.canvas_widget['tran_dropdown' + str(index) + '_rank'].get()[0]
            if rank == 'X':
                self.delete_widget_all('tran_graph_compare_' + colors[index])
                return
            rank_n = int(rank) - 1
            self.delete_widget_all('tran_graph_compare_' + colors[index])
            self.tran_detail_graph_compare(toggle, rank_n, colors[index])

        for i in range(3):
            self.canvas_widget['tran_dropdown'+str(i)+'_type'] = tkinter.ttk.Combobox(
                self.parent, width=4, values=tran_dropdown_types
            )
            self.canvas_widget['tran_dropdown' + str(i) + '_type'].place(x=447, y=490+65*i)
            self.canvas_widget['tran_dropdown' + str(i) + '_type'].set(tran_dropdown_types[self.now_rank_toggle])
            self.canvas_widget['tran_dropdown' + str(i) + '_rank'] = tkinter.ttk.Combobox(
                self.parent, width=4, values=tran_dropdown_list
            )
            self.canvas_widget['tran_dropdown' + str(i) + '_rank'].place(x=502, y=490+65*i)
            self.canvas_widget['tran_dropdown' + str(i) + '_rank'].set('X')
            self.canvas_widget['tran_dropdown' + str(i) + '_type'].bind(
                "<<ComboboxSelected>>", lambda e, index=i: create_tran_compare(e, index))
            self.canvas_widget['tran_dropdown' + str(i) + '_rank'].bind(
                "<<ComboboxSelected>>", lambda e, index=i: create_tran_compare(e, index))
        self.result_canvas.create_line(447, 485, 557, 485, width=2, fill='red')
        self.result_canvas.create_line(447, 550, 557, 550, width=2, fill='SteelBlue1')
        self.result_canvas.create_line(447, 615, 557, 615, width=2, fill='green2')

    def tran_detail_graph_compare(self, compare_toggle, compare_rank, color):
        try:
            now_tran_values = self.result_tran[compare_toggle][compare_rank]
        except IndexError as e:
            print(e)
            return
        if now_tran_values == [0]:
            print("tran 자료 없음")
        else:
            print("tran 비교 그래프 생성 시작")
            start_point = [42, 675]
            for i in range(0, 400):
                now_value = now_tran_values[i * 3]
                now_y = int(start_point[1] - 220 * (now_value - self.tran_min) / (self.tran_max - self.tran_min))
                self.result_canvas.create_line(
                    42 + i, now_y, 42 + i + 1, now_y, fill=color, width=1,
                    tag=("tran_graph_compare_" + color)
                )

    def create_stat_section(self):
        now_equipments = self.result_equipments[self.now_rank_toggle][self.now_rank_selected]
        now_value = self.result_values[self.now_rank_toggle][self.now_rank_selected]
        if now_value > 10000:
            now_value_show = str(int(now_value / 1000)) + "K"
        else:
            now_value_show = str(int(now_value * 100)) + "%"
        now_stat = self.result_stat[self.now_rank_toggle][self.now_rank_selected]
        now_level = self.result_level[self.now_rank_toggle][self.now_rank_selected]
        now_base = self.result_base[self.now_rank_toggle][self.now_rank_selected]
        now_all = self.result_all[self.now_rank_toggle][self.now_rank_selected]
        now_cool = self.result_cool[self.now_rank_toggle][self.now_rank_selected]
        now_convert = self.result_invert[self.now_rank_toggle][self.now_rank_selected]

        # 메인 부분
        if self.now_rank_toggle == 0:
            toggle_text = "종합"
        elif self.now_rank_toggle == 1:
            toggle_text = "순딜"
        elif self.now_rank_toggle == 2:
            toggle_text = "지딜"
        else:
            toggle_text = "각성"
        self.result_canvas.create_text(122, 110, text=toggle_text, font=self.fonts[0], fill='white',
                                       tag="rank_select")
        self.result_canvas.create_text(122, 130, text=now_value_show, font=self.fonts[2], fill='white',
                                       tag="rank_select")

        # 레벨링 부분
        leveling_index = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 48, 50, 60, 70, 75, 80, 85, 95, 100]
        leveling_max = [1, 50, 48, 46, 43, 41, 38, 36, 33, 31, 20, 12, 23, 18, 16, 13, 5, 6, 2]
        leveling_efficiency = [0, 0.05, 0.101443, 0.159328, 0, 0.231886]
        # 사전에 패시브 전용 레벨링 제거
        active_leveling_arr = now_level.copy()
        if self.now_creature == "크증18%" or self.now_creature == "물마독공18%":  # 크리쳐 2각패 레벨링 삭제
            active_leveling_arr[14] -= 1
        if now_equipments.__contains__("111016"):
            active_leveling_arr[5] -= 3
        elif now_equipments.__contains__("111024"):
            active_leveling_arr[3] -= 1
        elif now_equipments.__contains__("111029"):
            active_leveling_arr[14] -= 2
        elif now_equipments.__contains__("111036"):
            active_leveling_arr[10] -= 4
        elif now_equipments.__contains__("111059"):
            active_leveling_arr[5] -= 1.5
        elif now_equipments.__contains__("111060"):
            active_leveling_arr[5] -= 2
            active_leveling_arr[10] -= 2
            active_leveling_arr[14] -= 2
        elif now_equipments.__contains__("111062"):
            active_leveling_arr[10] -= 3
            active_leveling_arr[14] -= 3
        elif now_equipments.__contains__("111069"):
            active_leveling_arr[10] -= 3
            active_leveling_arr[14] -= 3
        elif now_equipments.__contains__("111075"):
            active_leveling_arr[4] -= 4.5
        for i in range(0, 19):
            if i > 10:
                index = i - 1
            elif i == 10:
                continue
            else:
                index = i
            now_leveling = active_leveling_arr[i]
            self.result_canvas.create_text(395, 55 + index * 19, text="+" + str(now_leveling),
                                           font=self.fonts[0], fill='white', anchor="w",
                                           tag="rank_select")
            if leveling_index[i] == 50:
                now_level_damage = now_base * (1 + leveling_efficiency[5] * (11 + now_leveling)) / (
                        1 + leveling_efficiency[5] * 11) * (now_stat[28] / 100 + 1)
            elif leveling_index[i] == 85:
                now_level_damage = now_base * (1 + leveling_efficiency[5] * (4 + now_leveling)) / (
                        1 + leveling_efficiency[5] * 4) * (now_stat[29] / 100 + 1)
            elif leveling_index[i] == 100:
                now_level_damage = now_base * (1 + leveling_efficiency[5] * (1 + now_leveling)) / (
                        1 + leveling_efficiency[5] * 1) * (now_stat[30] / 100 + 1)
            elif i == 0:
                now_level_damage = now_base * (1 + leveling_efficiency[1] * (99 + now_leveling)) / (
                        1 + leveling_efficiency[1] * 99)
            else:
                now_level_damage = now_base * (
                        1 + leveling_efficiency[2] * (leveling_max[i] - 1 + now_leveling)) / (
                                           1 + leveling_efficiency[2] * (leveling_max[i] - 1))
            if now_level_damage > 10000:
                now_level_value_show = str(int(now_level_damage / 1000)) + "K"
            else:
                now_level_value_show = str(int(now_level_damage * 100)) + "%"
            self.result_canvas.create_text(435, 55 + index * 19, text=now_level_value_show,
                                           font=self.fonts[0], fill='white', anchor="w",
                                           tag="rank_select")
            now_cool_down = round((1 - now_cool[index]) * 100, 1)
            self.result_canvas.create_text(540, 55 + index * 19, text="-" + str(now_cool_down) + "%",
                                           font=self.fonts[0], fill='white', anchor="e",
                                           tag="rank_select")

        # 6각 단리 스탯
        max_stat = max([now_stat[2], now_stat[3], now_stat[4], now_stat[6], now_stat[7], now_stat[8]])
        self.result_canvas.create_text(125, 200, anchor='s', text='증뎀\n' + str(round(now_stat[2], 1)) + "%",
                                       fill='white', font=self.fonts[1],
                                       tag="rank_select")
        self.result_canvas.create_text(200, 240, anchor='sw', text='크증\n' + str(round(now_stat[3], 1)) + "%",
                                       fill='white', font=self.fonts[1],
                                       tag="rank_select")
        self.result_canvas.create_text(200, 330, anchor='nw', text='추뎀\n' + str(round(now_stat[4], 1)) + "%",
                                       fill='white', font=self.fonts[1],
                                       tag="rank_select")
        self.result_canvas.create_text(125, 370, anchor='n', text='모공\n' + str(round(now_stat[6], 1)) + "%",
                                       fill='white', font=self.fonts[1],
                                       tag="rank_select")
        self.result_canvas.create_text(50, 330, anchor='ne', text='공%\n' + str(round(now_stat[7], 1)) + "%",
                                       fill='white', font=self.fonts[1],
                                       tag="rank_select")
        self.result_canvas.create_text(50, 240, anchor='se', text='스탯\n' + str(round(now_stat[8], 1)) + "%",
                                       fill='white', font=self.fonts[1],
                                       tag="rank_select")
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
            fill='slate blue', outline='dark slate blue', width=1,
            tag="rank_select")

        # 기타 스탯 옵션
        self.result_canvas.create_text(312, 257, text=str(round(now_stat[0], 0)),
                                       fill='white', font=self.fonts[0],
                                       tag="rank_select")
        self.result_canvas.create_text(312, 277, text=str(round(now_stat[1], 0)),
                                       fill='white', font=self.fonts[0],
                                       tag="rank_select")
        self.result_canvas.create_text(312, 297, text=str(round(now_stat[9], 0)),
                                       fill='white', font=self.fonts[0],
                                       tag="rank_select")
        self.result_canvas.create_text(306, 317, text=str(round(now_stat[10], 1)),
                                       fill='white', font=self.fonts[0],
                                       tag="rank_select")
        self.result_canvas.create_text(306, 337, text=str(round(now_stat[11], 1)),
                                       fill='white', font=self.fonts[0],
                                       tag="rank_select")
        self.result_canvas.create_text(306, 357, text=str(round(now_stat[13], 1)),
                                       fill='white', font=self.fonts[0],
                                       tag="rank_select")
        self.result_canvas.create_text(306, 377, text=str(round(now_stat[14], 1)),
                                       fill='white', font=self.fonts[0],
                                       tag="rank_select")

        # 연옥 변환 옵션
        convert_index = ['-', '', '증뎀', '크증', '추뎀', '', '모공', '공%', '스탯']
        convert_part_index = ['잔향1', '잔향2', '무기', '하의', '반지', '보조']
        for i in range(6):
            convert_string = convert_index[now_convert[i]]
            if i == 2 and now_convert[i] != 0:
                if now_convert[6] is True:
                    convert_string += "(각)"
            self.result_canvas.create_text(264, 56 + i * 20, text=convert_part_index[i],
                                           fill='white', font=self.fonts[0],
                                           tag="rank_select")
            self.result_canvas.create_text(314, 56 + i * 20, text=convert_string,
                                           fill='white', font=self.fonts[0],
                                           tag="rank_select")

    def create_base_section(self):
        self.now_creature = self.dropdown_list["creature"].get()
        now_job = self.dropdown_list["job"].get()
        self.result_canvas.create_text(122, 70, text=now_job, font=self.fonts[0], fill='white')

    def create_background(self):
        # 절대 바뀌지 않는 배경 생성 관련
        self.result_canvas.create_text(122, 50, text="<직업>", font=self.fonts[0], fill='white')

        # 변환 박스
        self.result_canvas.create_polygon(243, 20, 343, 20, 343, 167, 243, 167, 243, 20,
                                          fill='gray25', width=3, outline='black')
        self.result_canvas.create_text(293, 33, text="<변환 옵션>", font=self.fonts[0], fill='white')
        self.result_canvas.create_line(284, 45, 284, 167, width=1, fill='black')
        self.result_canvas.create_line(243, 45, 343, 45, width=1, fill='black')
        self.result_canvas.create_line(243, 65, 343, 65, width=1, fill='black')
        self.result_canvas.create_line(243, 85, 343, 85, width=1, fill='black')
        self.result_canvas.create_line(243, 105, 343, 105, width=1, fill='black')
        self.result_canvas.create_line(243, 125, 343, 125, width=1, fill='black')
        self.result_canvas.create_line(243, 145, 343, 145, width=1, fill='black')

        # 단리 스탯 육각형
        # 6각 단리 스탯
        self.result_canvas.create_polygon(
            125, 200, 200, 240, 200, 330, 125, 370, 50, 330, 50, 240, 125, 200,
            fill='gray21', outline='black', width=2)
        self.result_canvas.create_line(125, 200, 125, 370, fill='gray50', width=1)
        self.result_canvas.create_line(200, 240, 50, 330, fill='gray50', width=1)
        self.result_canvas.create_line(200, 330, 50, 240, fill='gray50', width=1)

        # 기타 스탯 박스
        self.result_canvas.create_polygon(243, 222, 343, 222, 343, 387, 243, 387, 243, 222,
                                          fill='gray25', width=3, outline='black')
        self.result_canvas.create_text(293, 235, text="<기타 스탯>", font=self.fonts[0], fill='white')
        self.result_canvas.create_line(284, 247, 284, 387, width=1, fill='black')
        self.result_canvas.create_line(243, 247, 343, 247, width=1, fill='black')
        self.result_canvas.create_line(243, 267, 343, 267, width=1, fill='black')
        self.result_canvas.create_line(243, 287, 343, 287, width=1, fill='black')
        self.result_canvas.create_line(243, 307, 343, 307, width=1, fill='black')
        self.result_canvas.create_line(243, 327, 343, 327, width=1, fill='black')
        self.result_canvas.create_line(243, 347, 343, 347, width=1, fill='black')
        self.result_canvas.create_line(243, 367, 343, 367, width=1, fill='black')
        self.result_canvas.create_text(248, 257, text="스탯+", fill='white', font=self.fonts[0], anchor='w')
        self.result_canvas.create_text(248, 277, text="공격+", fill='white', font=self.fonts[0], anchor='w')
        self.result_canvas.create_text(248, 297, text="속강", fill='white', font=self.fonts[0], anchor='w')
        self.result_canvas.create_text(251, 317, text="지속          %", fill='white', font=self.fonts[0], anchor='w')
        self.result_canvas.create_text(251, 337, text="스증          %", fill='white', font=self.fonts[0], anchor='w')
        self.result_canvas.create_text(251, 357, text="공속          %", fill='white', font=self.fonts[0], anchor='w')
        self.result_canvas.create_text(251, 377, text="크확          %", fill='white', font=self.fonts[0], anchor='w')

        # 레벨링 박스
        self.result_canvas.create_polygon(355, 20, 545, 20, 545, 388, 355, 388, 355, 20,
                                          fill='gray25', width=3, outline='black')
        self.result_canvas.create_text(450, 33, text="<레벨 구간별 장비%/쿨감>", font=self.fonts[0], fill='white')
        leveling_index = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80, 85, 95, 100]
        for i in range(0, 18):
            self.result_canvas.create_line(355, 45 + i * 19, 545, 45 + i * 19, width=1, fill='black')
            self.result_canvas.create_text(370, 55 + i * 19, text=str(leveling_index[i]),
                                           font=self.fonts[0], fill='white')

        # 정렬 버튼
        self.canvas_widget['sort1'] = self.result_canvas.create_image(
            573, 635, image=self.image_extra['result_sort_1n.png'], anchor='nw')
        self.canvas_widget['sort2'] = self.result_canvas.create_image(
            643, 635, image=self.image_extra['result_sort_2f.png'], anchor='nw')
        self.canvas_widget['sort3'] = self.result_canvas.create_image(
            713, 635, image=self.image_extra['result_sort_3f.png'], anchor='nw')
        self.canvas_widget['sort4'] = self.result_canvas.create_image(
            783, 635, image=self.image_extra['result_sort_4f.png'], anchor='nw')
        self.result_canvas.tag_bind(self.canvas_widget["sort1"],
                                    "<Button-1>", lambda e, toggle=0: self.rank_toggle(e, toggle))
        self.result_canvas.tag_bind(self.canvas_widget["sort2"],
                                    "<Button-1>", lambda e, toggle=1: self.rank_toggle(e, toggle))
        self.result_canvas.tag_bind(self.canvas_widget["sort3"],
                                    "<Button-1>", lambda e, toggle=2: self.rank_toggle(e, toggle))
        self.result_canvas.tag_bind(self.canvas_widget["sort4"],
                                    "<Button-1>", lambda e, toggle=3: self.rank_toggle(e, toggle))


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


