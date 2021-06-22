import tkinter
import tkinter.ttk
import tkinter.font
import tkinter.messagebox
import threading

import data.weapon as weapon
import data.job as job
import common
import calculate.terminal as terminal


class MainGUI(tkinter.Frame):
    font_list = []  # [guide_font, small_font, mid_font, big_font]
    color_list = []  # [dark_main, dark_sub, dark_blue, result_sub]
    image_weapon = {}
    image_equipment = []
    image_extra = {}
    btn_list = {}
    dropdown_list = {}
    label_list = {}
    select_weapon_list = []
    equipment_toggle = {}
    main_window = None

    def __init__(self, master):
        super(MainGUI, self).__init__(master)
        self.main_window = master
        self.font_list = common.load_font()
        self.color_list = common.load_color()
        self.image_equipment = common.load_equipment_image()
        self.image_extra = common.load_extra_image()
        self.image_weapon = common.load_weapon_image()
        self.create_main()
        self.set_btn_equipment()
        self.set_function_button()
        self.set_function_weapon()
        self.set_function_job()
        self.set_function_scent()
        self.set_function_purgatory()
        self.set_function_extra()
        self.set_extra()

    def create_main(self):
        self.main_window.geometry("909x720+0+0")
        self.main_window.resizable(False, False)
        self.main_window.title('에픽 조합 계산기')
        self.main_window.iconbitmap('ext_img/icon.ico')
        tkinter.Label(self.main_window, image=self.image_extra['bg_img.png']).place(x=-2, y=0)
        self.main_window.configure(bg=self.color_list[0])

    def set_btn_equipment(self):
        def create_btn_set(range_x, range_y, start_x, start_y, myth_index, *no_set):
            x_stack = 0
            for i in range_x:
                y_stack = 0
                for j in range_y:
                    if x_stack == 0 and not no_set:
                        self.create_btn_set(str(j), start_x - 71, start_y + 30 * y_stack)
                    code = str(i) + str(j)[1:] + '0'
                    self.create_btn_equipment(code, start_x + x_stack * 30, start_y + 30 * y_stack)
                    y_stack += 1
                x_stack += 1
                if i == myth_index:
                    y_stack = 0
                    for j in range_y:
                        code = str(i) + str(j)[1:] + '1'
                        self.create_btn_equipment(code, start_x + x_stack * 30, start_y + 30 * y_stack)
                        y_stack += 1
                    x_stack += 1

        # 533 방어구
        create_btn_set(
            [11, 12, 13, 14, 15],
            [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            100, 105, 11
        )
        # 533 악세사리
        create_btn_set(
            [21, 22, 23],
            [116, 117, 118, 119],
            358, 105, 21
        )
        # 533 특수장비
        create_btn_set(
            [31, 32, 33],
            [120, 121, 122, 123],
            554, 105, 33
        )
        # 3332 상목보
        create_btn_set(
            [11, 22, 31],
            [128, 129, 130, 131],
            100, 570, 11
        )
        # 3332 하팔법
        create_btn_set(
            [12, 21, 32],
            [124, 125, 126, 127],
            296, 570, 21
        )
        # 3332 신반귀
        create_btn_set(
            [15, 23, 33],
            [132, 133, 134, 135],
            492, 570, 33
        )
        # 시로코
        create_btn_set(
            [41],
            [151, 152, 153, 154, 155],
            770, 465, 99, True
        )
        # 오즈마
        create_btn_set(
            [55],
            [156, 157, 158, 159, 160],
            855, 465, 99, True
        )

    def create_btn_equipment(self, code, place_x, place_y):
        self.equipment_toggle[code] = False
        now_btn = tkinter.Button(self.main_window, relief='flat', bd=0, activebackground=self.color_list[0],
                                 bg=self.color_list[0], image=self.image_equipment[code + 'f.png'],
                                 command=lambda: self.click_equipment(code))
        now_btn.place(x=place_x, y=place_y)
        self.btn_list[code] = now_btn

    def create_btn_set(self, code, place_x, place_y):
        self.equipment_toggle[code] = False
        now_btn = tkinter.Button(self.main_window, relief='flat', borderwidth=0, activebackground=self.color_list[0],
                                 bg=self.color_list[0], image=self.image_equipment[code + 'f.png'],
                                 command=lambda: self.click_set(code))
        now_btn.place(x=place_x, y=place_y)
        self.btn_list[code] = now_btn

    def click_equipment(self, code):
        if self.equipment_toggle[code]:
            self.btn_list[code]['image'] = self.image_equipment[code + 'f.png']
            self.equipment_toggle[code] = False
        else:
            self.btn_list[code]['image'] = self.image_equipment[code + 'n.png']
            self.equipment_toggle[code] = True

    def click_set(self, code):
        part_tag = []
        if 115 >= int(code) >= 101:
            part_tag = ['11', '12', '13', '14', '15']
        elif 119 >= int(code) >= 116:
            part_tag = ['21', '22', '23']
        elif 123 >= int(code) >= 120:
            part_tag = ['31', '32', '33']
        elif 127 >= int(code) >= 124:
            part_tag = ['12', '21', '32']
        elif 131 >= int(code) >= 128:
            part_tag = ['11', '22', '31']
        elif 135 >= int(code) >= 132:
            part_tag = ['15', '23', '33']
        elif 155 >= int(code) >= 151:
            part_tag = ['41', '42', '43']
        on_stack = 0
        set_equipments = []
        for part in part_tag:
            now_code = part + code[1:] + '0'
            set_equipments.append(now_code)
            if self.equipment_toggle[now_code]:
                on_stack += 1
        if on_stack == len(part_tag):
            for now_code in set_equipments:
                self.click_equipment(now_code)
        else:
            for now_code in set_equipments:
                if not self.equipment_toggle[now_code]:
                    self.click_equipment(now_code)

    def set_function_extra(self):
        # 계산모드 설정
        self.create_dropdown('mode', 15, [
            '풀셋모드', '메타몽풀셋모드', '단품제외', '단품포함', '세트필터↓'
        ], 750, 11)
        # 칭호/크리쳐/쿨감보정
        self.create_dropdown('title', 13, ['증뎀15%', '속강32', '증뎀10%', '추뎀10%', '크증10%', '기타(직접비교)'], 373, 302)
        self.create_dropdown('creature', 13, ['크증18%', '모공15%', '물마독공18%', '기타(직접비교)'], 373, 332)
        self.create_dropdown('cool_down', 13, ['X(지속딜만)', 'O(그로기포함)'], 373, 362)

    def set_function_job(self):
        def job_type_select(event):
            now_list = list(job.job_list[self.dropdown_list['job_type'].get()])
            self.dropdown_list['job']["values"] = now_list
            self.dropdown_list['job'].set(now_list[0])

        self.create_dropdown('job_type', 13, list(job.job_list.keys()), 373, 242)
        self.create_dropdown('job', 13, job.job_list['귀검사(남)'], 373, 272)
        self.dropdown_list['job_type'].bind("<<ComboboxSelected>>", job_type_select)

    def set_function_weapon(self):
        tkinter.Label(self.main_window, image=self.image_extra['wep.png'], bd=0,
                      activebackground=self.color_list[0], bg=self.color_list[0]).place(x=29, y=10)

        def wep_job_selected(event):
            changing_dict = weapon.wep_list[str(self.dropdown_list['weapon_job'].get())]
            changing_list = list(changing_dict.keys())
            self.dropdown_list['weapon_type']["values"] = changing_list
            self.dropdown_list['weapon_type'].set(changing_list[0])
            wep_type_selected(0)

        def wep_type_selected(event):
            changing_dict = weapon.wep_list[str(self.dropdown_list['weapon_job'].get())]
            changing_list = list(changing_dict[str(self.dropdown_list['weapon_type'].get())])
            self.dropdown_list['weapon']["values"] = changing_list
            self.dropdown_list['weapon'].set(changing_list[0])

        def wep_selected():
            now_selected = str(self.dropdown_list['weapon'].get())
            if self.select_weapon_list.__contains__(now_selected) or len(self.select_weapon_list) == 10:
                tkinter.messagebox.showerror('에러', "중복된 무기 선택 또는 한도 초과")
                return
            self.select_weapon_list.append(now_selected)
            wep_img_list_refresh()

        def wep_reset():
            self.select_weapon_list = []
            wep_img_list_refresh()

        def wep_img_list_refresh():
            for i in range(0, 10):
                if len(self.select_weapon_list) > i:
                    now_image = self.image_weapon[weapon.wep_filename_image[self.select_weapon_list[i]] + '.png']
                else:
                    now_image = self.image_extra['00000.png']
                self.label_list['weapon_select_image'][i].configure(image=now_image)

        self.create_dropdown('weapon_job', 12, list(weapon.wep_list.keys()), 110, 10)
        self.dropdown_list['weapon_job'].bind("<<ComboboxSelected>>", wep_job_selected)
        self.create_dropdown('weapon_type', 12, list(weapon.wep_list['귀검/나이트'].keys()), 236, 10)
        self.dropdown_list['weapon_type'].bind("<<ComboboxSelected>>", wep_type_selected)
        self.create_dropdown('weapon', 30, weapon.wep_list['귀검/나이트']['광검'], 110, 38)
        self.btn_list['weapon_select'] = tkinter.Button(self.main_window, image=self.image_extra['wep_select.png'],
                                                        bd=0, activebackground=self.color_list[0],
                                                        command=wep_selected, bg=self.color_list[0])
        self.btn_list['weapon_select'].place(x=350, y=10)
        self.btn_list['weapon_reset'] = tkinter.Button(self.main_window, image=self.image_extra['wep_reset.png'], bd=0,
                                                       activebackground=self.color_list[0],
                                                       command=wep_reset, bg=self.color_list[0])
        self.btn_list['weapon_reset'].place(x=440, y=10)
        self.label_list['weapon_select_image'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 10):
            self.label_list['weapon_select_image'][i] = tkinter.Label(self.main_window, bg=self.color_list[1], bd=0,
                                                                      image=self.image_extra['00000.png'])
            self.label_list['weapon_select_image'][i].place(x=32 + 31 * i, y=68)

    def set_function_scent(self):
        def select_scent_mode(event):
            now_mode = str(self.dropdown_list['scent_mode'].get())
            if now_mode == '미부여' or now_mode == '최적부여':
                self.dropdown_list['scent1_option']['state'] = 'disabled'
                self.dropdown_list['scent2_option']['state'] = 'disabled'
                self.dropdown_list['scent1_value']['state'] = 'disabled'
                self.dropdown_list['scent2_value']['state'] = 'disabled'
                pass
            else:
                self.dropdown_list['scent1_option']['state'] = 'normal'
                self.dropdown_list['scent2_option']['state'] = 'normal'
                self.dropdown_list['scent1_value']['state'] = 'normal'
                self.dropdown_list['scent2_value']['state'] = 'normal'
                pass

        self.create_dropdown('scent_mode', 11, ["미부여", "선택부여", "최적부여"], 785, 285)
        self.dropdown_list['scent_mode'].bind("<<ComboboxSelected>>", select_scent_mode)

        scent1_option_list = [
            "증뎀 축탯%/각+", "크증 축탯%/각%", "추뎀 축공%/각+", "모공 축공%/각%", "공% 축공%/각렙", "스탯 스탯+"
        ]
        scent2_option_list = [
            "증뎀 축탯%/각+", "크증 축탯%/각%", "추뎀 축공%/각+", "모공 축공%/각%", "공% 축렙/각+", "스탯 스탯+"
        ]
        self.create_dropdown('scent1_option', 14, scent1_option_list, 764, 315)
        self.create_dropdown('scent1_value', 14, ['상(노랑)', '중(보라)', '하(파랑)'], 764, 315 + 27)
        self.create_dropdown('scent2_option', 14, scent2_option_list, 764, 315 + 27 + 28)
        self.create_dropdown('scent2_value', 14, ['상(노랑)', '중(보라)', '하(파랑)'], 764, 315 + 27 + 28 + 27)
        self.dropdown_list['scent1_option']['state'] = 'disabled'
        self.dropdown_list['scent2_option']['state'] = 'disabled'
        self.dropdown_list['scent1_value']['state'] = 'disabled'
        self.dropdown_list['scent2_value']['state'] = 'disabled'

    def set_function_purgatory(self):
        def set_purgatory_option(event, drop_down, drop_down_sub):
            if drop_down.get() == "미변환" or drop_down.get() == "최적변환":
                drop_down_sub['state'] = 'disabled'
            else:
                drop_down_sub['state'] = 'normal'

        purgatory_weapon_option = ["미변환", "최적변환",
                                   "증뎀 축탯%/각+", "크증 축탯%/각%", "추뎀 축공%/각+", "모공 축공%/각%", "공% 축탯%/각렙",
                                   "스탯 스탯+", "증뎀 각성+2", "크증 각성+2", "추뎀 각성+2",
                                   "모공 각성+2", "공% 각성+2", "스탯 각성+2"]
        purgatory_extra_option = ["미변환", "최적변환",
                                  "증뎀 축탯%/각+", "크증 축탯%/각%", "추뎀 축공%/각+",
                                  "모공 축공%/각%", "공% 축렙/각+", "스탯 스탯+"]
        self.create_dropdown('purgatory1_option', 13, purgatory_weapon_option, 510, 404)
        self.create_dropdown('purgatory1_value', 4, ['+16', '+12', '+8', '+4'], 632, 404)
        self.dropdown_list['purgatory1_option'].bind(
            "<<ComboboxSelected>>",
            lambda event:
            set_purgatory_option(event, self.dropdown_list['purgatory1_option'], self.dropdown_list['purgatory1_value'])
        )
        self.create_dropdown('purgatory2_option', 13, purgatory_extra_option, 510, 430)
        self.create_dropdown('purgatory2_value', 4, ['+8', '+6', '+4', '+2'], 632, 430)
        self.dropdown_list['purgatory2_option'].bind(
            "<<ComboboxSelected>>",
            lambda event:
            set_purgatory_option(event, self.dropdown_list['purgatory2_option'], self.dropdown_list['purgatory2_value'])
        )
        self.create_dropdown('purgatory3_option', 13, purgatory_extra_option, 510, 456)
        self.create_dropdown('purgatory3_value', 4, ['+8', '+6', '+4', '+2'], 632, 456)
        self.dropdown_list['purgatory3_option'].bind(
            "<<ComboboxSelected>>",
            lambda event:
            set_purgatory_option(event, self.dropdown_list['purgatory3_option'], self.dropdown_list['purgatory3_value'])
        )
        self.create_dropdown('purgatory4_option', 13, purgatory_extra_option, 510, 482)
        self.create_dropdown('purgatory4_value', 4, ['+8', '+6', '+4', '+2'], 632, 482)
        self.dropdown_list['purgatory4_option'].bind(
            "<<ComboboxSelected>>",
            lambda event:
            set_purgatory_option(event, self.dropdown_list['purgatory4_option'], self.dropdown_list['purgatory4_value'])
        )

        tkinter.Label(self.main_window, text='최적변환 각성 강제 여부', font=self.font_list[1],
                      fg="white", bg=self.color_list[1]).place(x=312, y=462)
        self.create_dropdown('purgatory_ult_mode', 15, ['태생유지', '각성강제', '각성해제'], 315, 482)

        self.dropdown_list['purgatory1_value']['state'] = 'disabled'
        self.dropdown_list['purgatory2_value']['state'] = 'disabled'
        self.dropdown_list['purgatory3_value']['state'] = 'disabled'
        self.dropdown_list['purgatory4_value']['state'] = 'disabled'

    def create_dropdown(self, tag, width, values, place_x, place_y):
        now_dropdown = tkinter.ttk.Combobox(self.main_window, width=width, values=values)
        now_dropdown.set(values[0])
        now_dropdown.place(x=place_x, y=place_y)
        self.dropdown_list[tag] = now_dropdown

    def set_function_button(self):
        def start_calc_thread():
            threading.Thread(target=terminal.Terminal, args=(self.dropdown_list, self.select_weapon_list,
                                                             self.equipment_toggle), daemon=True).start()

        self.btn_list["calculate"] = tkinter.Button(self.main_window, relief='flat', bd=0,
                                                    activebackground=self.color_list[0],
                                                    bg=self.color_list[0], image=self.image_extra['calc.png'])
        self.btn_list["calculate"]['command'] = start_calc_thread  # 테스트
        self.btn_list["calculate"].place(x=505, y=7)
        pass

    def set_extra(self):
        def guide_speed():
            tkinter.messagebox.showinfo("정확도 선택",
                                        "매우빠름=세트옵션7개 풀적용 경우의 수만 계산. 중간세팅은 고려하지 않음\n"
                                        "빠름=단일 선택 부위를 전부 제거\n중간=단일은 포함하되, 신화에 우선권 부여\n"
                                        "느림=세트 수 우선권 완화, 신화 우선권 삭제")

        tkinter.Button(self.main_window, command=guide_speed, image=self.image_extra['select_speed.png'], bd=0,
                       activebackground=self.color_list[0], bg=self.color_list[0]).place(x=634, y=7)
