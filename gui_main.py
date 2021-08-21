import tkinter
import tkinter.ttk
import tkinter.font
import tkinter.messagebox
import threading
import json

import data.job_rank
import data.weapon as weapon
import data.job as job
import common
import calculate.terminal as terminal
import gui_result
import gui_loading
import timeline


class MainGUI(tkinter.Frame):
    font_list = []  # [guide_font, small_font, mid_font, big_font]
    color_list = []  # [dark_main, dark_sub, dark_blue, result_sub]
    image_equipment = []
    image_extra = {}
    btn_list = {}
    dropdown_list = {}
    label_list = {}
    entry_list = {}
    select_weapon_list = []
    equipment_toggle = {}
    main_window = None
    result_class = None
    loading_class = None

    def __init__(self, master, version):
        super(MainGUI, self).__init__(master)
        self.main_window = master
        self.font_list = common.load_font()
        self.color_list = common.load_color()
        self.image_equipment = common.load_equipment_image()
        self.image_extra = common.load_extra_image()
        self.custom_frame = None
        self.version = version
        self.is_custom_open = False
        self.create_main()
        threading.Thread(target=self.set_btn_equipment).start()
        threading.Thread(target=self.set_function_button).start()
        threading.Thread(target=self.set_function_weapon).start()
        threading.Thread(target=self.set_function_job).start()
        threading.Thread(target=self.set_function_scent).start()
        threading.Thread(target=self.set_function_purgatory).start()
        threading.Thread(target=self.set_function_extra).start()
        threading.Thread(target=self.set_extra).start()
        threading.Thread(target=self.set_save_load_function).start()
        threading.Thread(target=self.set_timeline_function).start()
        threading.Thread(target=self.set_custom_function).start()

        threading.Thread(target=self.create_sub_gui).start()

    def create_sub_gui(self):
        self.result_class = gui_result.ResultGUI(
            self.main_window,
            self.image_equipment, self.image_extra, self.dropdown_list, self.version
        )
        self.loading_class = gui_loading.LoadingGUI(
            self.main_window
        )

    def create_main(self):
        self.main_window.geometry("909x720")
        self.main_window.resizable(False, False)
        self.main_window.title('에픽조합계산기R Beta')
        self.main_window.iconbitmap('ext_img/icon.ico')
        tkinter.Label(self.main_window, image=self.image_extra['bg_img.png'], bd=0).place(x=-2, y=0)
        self.main_window.configure(bg=self.color_list[0])
        self.custom_frame = tkinter.Frame(
            self.main_window, bd=0, bg=self.color_list[1], width=240, height=700
        )
        self.custom_frame.place(x=910, y=10)

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

    def update_equipment(self):
        for equipment, toggle in self.equipment_toggle.items():
            if toggle is True:
                self.btn_list[equipment]['image'] = self.image_equipment[equipment + 'n.png']
            else:
                self.btn_list[equipment]['image'] = self.image_equipment[equipment + 'f.png']

    def set_function_extra(self):
        # 계산모드 설정
        self.create_dropdown('mode', 18, [
            'AUTO MODE', 'ALL MODE'
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
            self.wep_img_list_refresh()

        def wep_reset():
            self.select_weapon_list = []
            self.wep_img_list_refresh()

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

    def wep_img_list_refresh(self):
        for i in range(0, 10):
            if len(self.select_weapon_list) > i:
                now_image = self.image_equipment[weapon.wep_filename_image[self.select_weapon_list[i]] + '.png']
            else:
                now_image = self.image_extra['00000.png']
            self.label_list['weapon_select_image'][i].configure(image=now_image)

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
                      fg="white", bg=self.color_list[1]).place(x=312, y=464)
        self.create_dropdown('purgatory_ult_mode', 15, ['태생유지', '각성강제', '각성해제'], 315, 482)

        self.dropdown_list['purgatory1_value']['state'] = 'disabled'
        self.dropdown_list['purgatory2_value']['state'] = 'disabled'
        self.dropdown_list['purgatory3_value']['state'] = 'disabled'
        self.dropdown_list['purgatory4_value']['state'] = 'disabled'

        def purgatory_toggle_all():
            for i in range(1, 5):
                self.dropdown_list['purgatory{}_option'.format(i)].set('최적변환')

        self.btn_list["purgatory_toggle"] = tkinter.Button(
            self.main_window, relief='flat', bd=0, activebackground=self.color_list[0], command=purgatory_toggle_all,
            bg=self.color_list[0], image=self.image_extra['purgatory_toggle.png'])
        self.btn_list["purgatory_toggle"].place(x=325, y=435)

    def create_dropdown(self, tag, width, values, place_x, place_y):
        now_dropdown = tkinter.ttk.Combobox(self.main_window, width=width, values=values)
        try:
            now_dropdown.set(values[0])
        except IndexError:
            pass
        now_dropdown.place(x=place_x, y=place_y)
        self.dropdown_list[tag] = now_dropdown

    def set_function_button(self):
        def start_calc_thread():
            if terminal.is_running is True:
                tkinter.messagebox.showinfo(title='계산하기', message='이미 작동중입니다.')
                return
            if len(self.select_weapon_list) == 0:
                now_selected = str(self.dropdown_list['weapon'].get())
                select_weapon_list = [now_selected]
            else:
                select_weapon_list = self.select_weapon_list
            calc_start = threading.Thread(target=terminal.Terminal, args=(
                self.dropdown_list, self.entry_list, select_weapon_list, self.equipment_toggle,
                self.result_class, self.label_list["dialog"]
            ), daemon=True)
            calc_start.start()

        self.label_list["dialog"] = tkinter.Label(
            self.main_window, text="대기중...", font=self.font_list[1],
            fg="white", bg=self.color_list[1])
        self.label_list["dialog"].place(x=691, y=107)

        self.btn_list["calculate"] = tkinter.Button(self.main_window, relief='flat', bd=0,
                                                    activebackground=self.color_list[0],
                                                    bg=self.color_list[0], image=self.image_extra['calc.png'])
        self.btn_list["calculate"]['command'] = start_calc_thread
        self.btn_list["calculate"].place(x=505, y=7)

    def set_timeline_function(self):
        def load_timeline():
            timeline_class = timeline.Timeline(self.dropdown_list['server'].get(), name_entry.get())
            return_list = timeline_class.return_list()
            for code in self.equipment_toggle.keys():
                if return_list.__contains__(code):
                    self.equipment_toggle[code] = True
                else:
                    self.equipment_toggle[code] = False
            self.update_equipment()

        sever_list = ['카인', '디레지에', '바칼', '힐더', '안톤', '카시야스', '프레이', '시로코']
        self.create_dropdown('server', 8, sever_list, 512, 242)
        name_entry = tkinter.Entry(self.main_window, width=11)
        name_entry.insert(0, '캐릭명')
        name_entry.place(x=510, y=270)
        self.btn_list['timeline'] = tkinter.Button(
            self.main_window, relief='flat', bd=0,
            activebackground=self.color_list[0], command=load_timeline,
            bg=self.color_list[0], image=self.image_extra['timeline.png']
        )
        self.btn_list['timeline'].place(x=600, y=240)

    def set_save_load_function(self):
        def get_save_names():
            with open('./data/save.json', 'rt', encoding='UTF-8') as infile:
                save_dict = json.load(infile)
            save_names = list(save_dict.keys())
            self.dropdown_list['save']['values'] = save_names
            self.dropdown_list['save'].set(save_names[0])

        def delete_save():
            ask_del = tkinter.messagebox.askquestion(
                title='데이터 삭제',
                message='해당 세이브 데이터를 삭제합니다. 정말로 진행하시겠습니까?')
            if ask_del == 'yes':
                pass
            else:
                return
            with open('./data/save.json', 'rt', encoding='UTF-8') as infile:
                save_dict = json.load(infile)
            del save_dict[str(self.dropdown_list['save'].get())]
            save_names = list(save_dict.keys())
            self.dropdown_list['save']['values'] = save_names
            with open('./data/save.json', 'wt', encoding='UTF-8') as outfile:
                json.dump(save_dict, outfile, ensure_ascii=False)

        def save_now():
            ask_save = tkinter.messagebox.askquestion(
                title='저장하기',
                message='해당 세이브 슬롯에 데이터를 저장합니다. 기존에 있던 동일 슬롯의 데이터는 전부 덮어씁니다.'
                        '정말로 진행하시겠습니까?')
            if ask_save == 'yes':
                pass
            else:
                return
            with open('./data/save.json', 'rt', encoding='UTF-8') as infile:
                save_dict = json.load(infile)
            now_save_name = str(self.dropdown_list['save'].get())
            save_equipments = []
            for code, toggle in self.equipment_toggle.items():
                if toggle:
                    save_equipments.append(code)
            save_dropdown = {}
            for code, dropdown in self.dropdown_list.items():
                save_dropdown[code] = str(dropdown.get())
            del save_dropdown['save']
            save_setting = {}
            for code, entry in self.entry_list.items():
                save_setting[code] = str(entry.get())
            save_dict[now_save_name] = {
                'weapons': self.select_weapon_list,
                'equipments': save_equipments,
                'dropdown': save_dropdown,
                'setting': save_setting
            }
            save_names = list(save_dict.keys())
            self.dropdown_list['save']['values'] = save_names
            with open('./data/save.json', 'wt', encoding='UTF-8') as outfile:
                json.dump(save_dict, outfile, ensure_ascii=False)
            tkinter.messagebox.showinfo(title='저장하기', message='저장 완료')

        def load_now():
            ask_load = tkinter.messagebox.askquestion(
                title='불러오기',
                message='해당 세이브 슬롯에 데이터를 불러옵니다. 정말로 진행하시겠습니까?')
            if ask_load == 'yes':
                pass
            else:
                return
            with open('./data/save.json', 'rt', encoding='UTF-8') as infile:
                save_dict = json.load(infile)
            now_save_name = str(self.dropdown_list['save'].get())
            save_values = save_dict.get(now_save_name)
            if save_values is None:
                tkinter.messagebox.showerror(title='불러오기', message='해당 이름의 저장 슬롯이 존재하지 않습니다.')
                return
            self.select_weapon_list = save_values['weapons']
            self.wep_img_list_refresh()
            save_equipment = save_values['equipments']
            for code in self.equipment_toggle.keys():
                if save_equipment.__contains__(code):
                    self.equipment_toggle[code] = True
                else:
                    self.equipment_toggle[code] = False
            self.update_equipment()
            save_dropdown = save_values['dropdown']
            for key, value in save_dropdown.items():
                self.dropdown_list[key].set(value)
            save_setting = save_values['setting']
            for key, value in save_setting.items():
                self.entry_list[key].delete(0, "end")
                self.entry_list[key].insert(0, value)
            tkinter.messagebox.showinfo(title='불러오기', message='불러오기 완료')

        self.btn_list["save"] = tkinter.Button(
            self.main_window, relief='flat', bd=0, activebackground=self.color_list[0],
            bg=self.color_list[0], image=self.image_extra['SAVE.png'])
        self.btn_list["save"]['command'] = save_now
        self.btn_list["save"].place(x=510, y=340)
        self.btn_list["load"] = tkinter.Button(
            self.main_window, relief='flat', bd=0, activebackground=self.color_list[0],
            bg=self.color_list[0], image=self.image_extra['LOAD.png'])
        self.btn_list["load"]['command'] = load_now
        self.btn_list["load"].place(x=600, y=340)
        self.create_dropdown('save', 8, [], 513, 311)
        self.btn_list["delete_save"] = tkinter.Button(
            self.main_window, relief='flat', bd=0, activebackground=self.color_list[0],
            bg=self.color_list[0], image=self.image_extra['delete_small.png'])
        self.btn_list["delete_save"]['command'] = delete_save
        self.btn_list["delete_save"].place(x=600, y=309)
        get_save_names()

    def set_custom_function(self):
        def open_custom():
            if self.is_custom_open:
                self.result_class.get_main_expand(False)
                self.is_custom_open = False
                self.main_window.geometry('909x720')
            else:
                self.result_class.get_main_expand(True)
                self.is_custom_open = True
                self.main_window.geometry('1160x720')
        self.btn_list['custom'] = tkinter.Button(
            self.main_window, command=open_custom, image=self.image_extra['custom.png'], bd=0,
            activebackground=self.color_list[0], bg=self.color_list[0])
        self.btn_list['custom'].place(x=813, y=40)

        def create_entry(tag, text, inv, value, x, y, width):
            tkinter.Label(self.custom_frame, text=text, fg='white', bg=self.color_list[1],
                          font=self.font_list[0]).place(x=x, y=y)
            self.entry_list[tag] = tkinter.ttk.Entry(self.custom_frame, width=width)
            self.entry_list[tag].insert(0, value)
            self.entry_list[tag].place(x=x+inv, y=y)
        tkinter.Label(self.custom_frame, text="<속강 커스텀>", fg='white', bg=self.color_list[1],
                      font=self.font_list[2]).place(x=50, y=5)
        tkinter.Label(self.custom_frame, text="주속성=", fg='white', bg=self.color_list[1],
                      font=self.font_list[0]).place(x=5, y=40)
        self.dropdown_list['element_type'] = tkinter.ttk.Combobox(
            self.custom_frame, width=4, values=['화', '수', '명', '암', '모속']
        )
        tkinter.Label(self.custom_frame, text="모속강은 수문장 전용", fg='red', bg=self.color_list[1],
                      font=self.font_list[1]).place(x=120, y=42)
        self.dropdown_list['element_type'].set('화')
        self.dropdown_list['element_type'].place(x=60, y=40)
        create_entry('element_single', "단속강=", 55, 163, 5, 70, 6)
        create_entry('element_all', "모속강=", 55, 153, 5, 100, 6)
        create_entry('element_debuff', "총속깎=", 55, 60, 120, 70, 6)
        create_entry('element_resist', "몹속저=", 55, 50, 120, 100, 6)

        tkinter.Label(self.custom_frame, text="<딜러 커스텀>", fg='white', bg=self.color_list[1],
                      font=self.font_list[2]).place(x=50, y=140)
        create_entry('sunset_reinforce', "먼동강화=            강 (0~13)", 67, 10, 5, 175, 6)
        tkinter.Label(self.custom_frame, text="사막축복=", fg='white', bg=self.color_list[1],
                      font=self.font_list[0]).place(x=5, y=205)
        self.dropdown_list['desert_super_armor'] = tkinter.ttk.Combobox(
            self.custom_frame, width=9, values=['노피격(6+4)', '슈아유지(6)', '슈아파괴(X)']
        )
        self.dropdown_list['desert_super_armor'].set('슈아유지(6)')
        self.dropdown_list['desert_super_armor'].place(x=70, y=205)

        tkinter.Label(self.custom_frame, text="-가환산 특수딜 보정%-", fg='white', bg=self.color_list[1],
                      font=self.font_list[0]).place(x=50, y=235)
        create_entry('flow_shoulder', "흐름어깨=", 65, 0, 5, 260, 6)
        create_entry('flow_jacket', "흐름상의=", 65, 0, 120, 260, 6)
        create_entry('flow_pants', "흐름하의=", 65, 0, 5, 295, 6)
        create_entry('flow_waist', "흐름벨트=", 65, 0, 120, 295, 6)
        create_entry('flow_shoes', "흐름신발=", 65, 0, 5, 330, 6)
        create_entry('selection_shoes', "선택신발=", 65, 15, 120, 330, 6)
        tkinter.Label(self.custom_frame, text="-가환산 쿨감보정-", fg='white', bg=self.color_list[1],
                      font=self.font_list[0]).place(x=62, y=360)
        create_entry('cool_ratio_groggy', "순간딜=", 55, 20, 5, 385, 6)
        create_entry('cool_ratio_sustain', "지속딜=", 55, 70, 120, 385, 6)
        tkinter.Label(self.custom_frame, text="-정밀계산 보정-", fg='white', bg=self.color_list[1],
                      font=self.font_list[0]).place(x=70, y=415)
        create_entry('fix_delay', "고정 딜레이=            초 (0.0~1.0)", 85, 0.5, 5, 440, 6)
        create_entry('section_groggy', "순간딜 구간=              초 (20이상)", 85, "20~30", 5, 470, 8)
        create_entry('section_total', "종합딜 구간=              초", 85, "30~50", 5, 500, 8)
        create_entry('section_sustain', "지속딜 구간=              초 (120이하)", 85, "110~120", 5, 530, 8)

    def set_extra(self):
        def guide_speed():
            tkinter.messagebox.showinfo("정확도 선택",
                                        "AUTO MODE: 신화풀셋 > 일반풀셋 = 신화혼합 > 일반혼합 순으로 진행\n\n"
                                        "ALL MODE: 모든 경우의 수 계산")

        tkinter.Button(self.main_window, command=guide_speed, image=self.image_extra['select_speed.png'], bd=0,
                       activebackground=self.color_list[0], bg=self.color_list[0]).place(x=634, y=7)

        def run_job_rank():
            data.job_rank.JobRank(self.main_window)
        tkinter.Button(
            self.main_window, command=run_job_rank, text="직업 비교"
        ).place(x=700, y=650)
