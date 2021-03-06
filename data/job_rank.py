import tkinter
import tkinter.ttk
import tkinter.messagebox
import common
import data.load_job
import os
import json
from . import translate

index_passive = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 48, 50, 60, 70, 75, 80, 85, 95, 100]
index_active = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80, 85, 95, 100]
leveling_efficiency = [0, 0.05, 0.101443, 0.159328, 0, 0.231886]
start_point = [30, 470]
size = [600, -400]


class JobRank:

    def __init__(self, master):
        self.colors = common.load_color()  # [dark_main, dark_sub, dark_blue, result_sub]
        self.fonts = common.load_font()  # [guide_font, small_font, mid_font, big_font]
        self.window = tkinter.Toplevel(master)
        self.window.geometry("1000x700")
        self.window.resizable(False, False)
        self.canvas = None
        self.alert = None
        self.dropdowns = {}
        self.entries = {}
        self.job_main_data = {}

        self.weapon_type = "공통"
        self.active_leveling_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.passive_leveling_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ult_damage_arr = [1, 1, 1]
        self.equipments_sets = []
        self.total_cool_down = 0.8
        self.fix_delay = 5
        self.no_cool_efficiency = 0.7
        self.damage_ratio = 1

        self.job_list = []
        file_list = os.listdir("./data/job")
        for name in file_list:
            self.job_list.append(name[:-5])

        self.create_gui()
        self.create_graph_background()

        def destroy_rank(e):
            self.window.destroy()
        self.window.bind('<Escape>', destroy_rank)

    def create_gui(self):
        self.canvas = tkinter.Canvas(self.window, width=1100, height=900, bd=0, bg=self.colors[0])
        self.canvas.place(x=-2, y=-2)

        tkinter.Label(self.window, text="직업명=", font=self.fonts[0], bg=self.colors[0], fg='white').place(x=30, y=10)
        tkinter.Label(
            self.window, text="고정 딜레이 0.5초 / 평타 효율 70% 기준", font=self.fonts[0], bg=self.colors[0], fg='white'
        ).place(x=30, y=38)
        for i in range(0, 2):
            self.dropdowns['job{}'.format(i)] = tkinter.ttk.Combobox(
                self.window, values=self.job_list, width=10
            )
            self.dropdowns['job{}'.format(i)].set("-직업 선택-")
            self.dropdowns['job{}'.format(i)].place(x=90, y=10+530*i)
            self.dropdowns['job{}'.format(i)].bind(
                "<<ComboboxSelected>>", lambda event, job_index=i:
                self.get_job_data(job_index)
            )
        save_image = tkinter.PhotoImage(file='ext_img/SAVE.png')
        save_btn = tkinter.Button(
            self.window, image=save_image, command=self.save_skill_custom, bg=self.colors[0],
            activebackground=self.colors[0], bd=0)
        save_btn.place(x=880, y=630)
        save_btn.image = save_image

    def get_job_data(self, job_index):
        job = self.dropdowns['job{}'.format(job_index)].get()
        try:
            job_detail_data = data.load_job.load_job_json(job)
            if job_index == 0:
                self.job_main_data = job_detail_data
            detail_active_list = job_detail_data["active"]
            detail_passive_list = job_detail_data["passive"]
            detail_special_list = job_detail_data["special"]
            detail_weapon_list = job_detail_data["weapon"]
        except FileNotFoundError:
            print("직업 계수 데이터 미존재")
            return None
        weapon_atk_rate = 1
        weapon_cool_rate = 1
        for weapon in detail_weapon_list:
            if weapon["type"] == self.weapon_type:
                weapon_atk_rate = weapon["damage"]
                weapon_cool_rate = weapon["coolTime"]
        active_dict = {}
        for active in detail_active_list:
            now_lv = active["nowLv"]
            if now_lv == 0:
                continue
            if active.get("talisman") is None:
                damage = active["damage"]
                cool_time = active["coolTime"]
            else:
                if active["talisman"]["available"] == 0:
                    damage = active["damage"]
                    cool_time = active["coolTime"]
                else:
                    damage = active["talisman"]["damage"]
                    cool_time = active["talisman"]["coolTime"]
                    if self.equipments_sets.__contains__("15140"):
                        if active["talisman"]["available"] == 1:
                            damage = damage * 1.55
                            cool_time = cool_time * 0.7
                        elif active["talisman"]["available"] == 2:
                            damage = damage * 1.45
                            cool_time = cool_time * 0.75
            max_lv = active["maxLv"]
            up_lv = self.active_leveling_arr[index_passive.index(active["requireLv"])]
            now_tp = active["nowTp"]
            max_tp = active["maxTp"]
            skill_delay = active["delay"]
            try:
                limit_s = active["limit_s"]
            except KeyError:
                limit_s = 0
            try:
                limit_f = active["limit_f"]
            except KeyError:
                limit_f = 9999
            now_eff = leveling_efficiency[active["gapLv"]]
            damage = int(damage *
                         (1 + now_eff * (now_lv + up_lv - 1)) / (1 + now_eff * (max_lv - 1)) *
                         (1 + 0.1 * now_tp) / (1 + 0.1 * max_tp) *
                         weapon_atk_rate)
            if active["requireLv"] == 50:
                damage = int(damage * self.ult_damage_arr[0])
            elif active["requireLv"] == 85:
                damage = int(damage * self.ult_damage_arr[1])
            elif active["requireLv"] == 100:
                damage = int(damage * self.ult_damage_arr[2])
            # 흐름
            elif active["requireLv"] == 45:
                if self.equipments_sets.__contains__("11130") or self.equipments_sets.__contains__("11131"):
                    damage = int(damage * 0.7)
            elif active["requireLv"] == 40:
                if self.equipments_sets.__contains__("12130"):
                    damage = int(damage * 0.7)
            elif active["requireLv"] == 35:
                if self.equipments_sets.__contains__("13130"):
                    damage = int(damage * 0.7)
            elif active["requireLv"] == 30:
                if self.equipments_sets.__contains__("14130"):
                    damage = int(damage * 0.7)
            elif active["requireLv"] == 25:
                if self.equipments_sets.__contains__("15130"):
                    damage = int(damage * 0.7)
            cool_fix = False
            if active.get("cool_fix") is not None:
                cool_fix = True
                if active.get("talisman") is None:
                    cool_time = active["coolTime"]
                else:
                    if active["talisman"]["available"] == 0:
                        cool_time = active["coolTime"]
                    else:
                        cool_time = active["talisman"]["coolTime"]
            else:
                try:
                    cool_time = round(cool_time * weapon_cool_rate * self.total_cool_down, 1)
                except TypeError:
                    cool_time = 0
            # log("스킬명", active["name"])
            # log("damage", damage)
            # log("cool_time", cool_time)
            active_dict[active["name"]] = [damage, cool_time, skill_delay, limit_s, limit_f, cool_fix]
        # log("active_dict", active_dict)
        before_passive = 0
        for key, value in active_dict.items():
            if active_dict[key][1] != 0:
                before_passive += active_dict[key][0] / active_dict[key][1]

        # 패시브 레벨링 판정
        for passive in detail_passive_list:
            requirement_type = passive["requirementType"]
            if requirement_type is None:
                is_condition = True
            else:
                is_condition = False
            if requirement_type == "ALL":
                is_condition = True
            elif requirement_type == "WEAPON":
                if passive["requirementValue"][-1] == "!":
                    only_require_type = passive["requirementValue"][:-1]
                    if only_require_type == self.weapon_type:
                        is_condition = True
                else:
                    if self.weapon_type == "공통" or passive["requirementValue"] == self.weapon_type:
                        is_condition = True
            elif requirement_type == "EQUIPMENT":
                if self.equipments_sets.__contains__(passive["requirementValue"]):
                    is_condition = True
            if is_condition is False:
                continue
            up_lv = self.passive_leveling_arr[index_passive.index(passive["requireLv"])]
            if passive["type"] == "DAMAGE":
                index = 0
                standard_value = 100 + passive["maxValue"]
                now_value = standard_value + up_lv * passive["upValue"]
            elif passive["type"] == "COOL":
                index = 1
                standard_value = 100 - passive["maxValue"]
                now_value = standard_value - up_lv * passive["upValue"]
            else:
                continue
            total_rate = now_value / standard_value
            if passive["target"] == "ALL":
                for name, value_list in active_dict.items():
                    if index == 1 and value_list[5] is True:
                        continue
                    value_list[index] = value_list[index] * total_rate
            else:
                target_list = passive["target"].split("^")  # ^ 구분자를 기준으로 split
                for target in target_list:
                    try:
                        active_dict[target][index] = active_dict[target][index] * total_rate
                    except KeyError:
                        pass
        # log("active_dict", active_dict)
        after_passive = 0
        for key, value in active_dict.items():
            if active_dict[key][1] != 0:
                after_passive += active_dict[key][0] / active_dict[key][1]
        passive_efficiency = after_passive / before_passive
        # log("passive_efficiency", passive_efficiency)

        # 특수 처리
        for special in detail_special_list:
            requirement_type = special["requirementType"]
            if requirement_type is None:
                is_condition = True
            else:
                is_condition = False
            if requirement_type == "ALL":
                is_condition = True
            elif requirement_type == "WEAPON":
                if special["requirementValue"][-1] == "!":
                    only_require_type = special["requirementValue"][:-1]
                    if only_require_type == self.weapon_type:
                        is_condition = True
                else:
                    if self.weapon_type == "공통" or special["requirementValue"] == self.weapon_type:
                        is_condition = True
            elif requirement_type == "EQUIPMENT":
                if self.equipments_sets.__contains__(special["requirementValue"]):
                    is_condition = True
            if is_condition is False:
                continue
            if special["type"] == "DAMAGE":
                index = 0
                value = special["value"] / 100 + 1
            elif special["type"] == "COOL":
                index = 1
                value = 1 - special["value"] / 100
            else:
                continue
            if special["target"] == "ALL":
                for name, value_list in active_dict.items():
                    if index == 1 and value_list[5] is True:
                        continue
                    value_list[index] = value_list[index] * value
            else:
                target_list = special["target"].split("^")  # ^ 구분자를 기준으로 split
                for target in target_list:
                    try:
                        active_dict[target][index] = active_dict[target][index] * value
                    except KeyError:
                        pass

        for name, value_list in active_dict.items():
            value_list[0] = int(value_list[0])
            value_list[1] = round(value_list[1], 1)
        log("active_dict", active_dict)

        final_damage_ult = 0
        case = 0
        index_name = []
        index_cool = []
        index_damage = []
        index_delay = []
        index_limit_s = []
        index_limit_f = []
        value_no_cool_sum = [0, 1, 1 - self.fix_delay]
        index_use = []
        index_use_sustain = []
        index_use_groggy = []
        delay_time = []
        for name, value_list in active_dict.items():
            if value_list[1] == 0:
                # 무쿨타임(평타)
                value_no_cool_sum[0] += int(value_list[0] * self.damage_ratio * self.no_cool_efficiency)
                value_no_cool_sum[1] = 1  # 쿨타임 없음
                value_no_cool_sum[2] = int(value_list[2] * 10 - self.fix_delay)  # 선입력 고정 딜레이를 감안하여 입력
            else:
                case += 1
                index_name.append(name)
                value_list[0] = int(value_list[0] * self.damage_ratio)
                index_damage.append(value_list[0])
                index_cool.append(int(value_list[1] * 10))
                index_delay.append(int(value_list[2] * 10))
                index_limit_s.append(int(value_list[3] * 10))
                index_limit_f.append(int(value_list[4] * 10))
                delay_time.append(0)
                index_use.append(0)
                index_use_sustain.append(0)
                index_use_groggy.append(0)
        case += 1
        index_name.append('평타')
        index_damage.append(value_no_cool_sum[0])
        index_cool.append(value_no_cool_sum[1])
        index_delay.append(value_no_cool_sum[2])
        delay_time.append(0)
        index_limit_s.append(0)
        index_limit_f.append(9999)
        index_use.append(0)
        index_use_sustain.append(0)
        index_use_groggy.append(0)
        # log("active_dict", active_dict)

        damage_trans = []
        damage_trans_ult = []
        damage_trans_high = []
        damage_trans_low = []
        damage_trans_no_cool = []
        now_time_damage = 0
        now_time_damage_ult = 0
        now_time_damage_high = 0
        now_time_damage_low = 0
        now_time_damage_no_cool = 0
        cannot_damage_time = 0
        for c_sec in range(0, 1201):
            cannot_damage_time -= 1
            for index in range(case):
                delay_time[index] -= 1
            if cannot_damage_time > 0:
                damage_trans.append(now_time_damage)
                damage_trans_ult.append(now_time_damage_ult)
                damage_trans_high.append(now_time_damage_high)
                damage_trans_low.append(now_time_damage_low)
                damage_trans_no_cool.append(now_time_damage_no_cool)
                continue
            for index in range(case):
                if delay_time[index] <= 0:
                    if index_limit_f[index] < c_sec or index_limit_s[index] > c_sec:
                        continue
                    # print(str(c_sec), 'cs 사용 스킬 = ', index_name[index])
                    index_use_sustain[index] += 1
                    cannot_damage_time = index_delay[index] + self.fix_delay
                    delay_time[index] = index_cool[index]
                    if c_sec > 400:
                        increasing_damage = int(index_damage[index] * 0.6)
                    else:
                        index_use[index] += 1
                        increasing_damage = int(index_damage[index])
                        if c_sec > 300:
                            index_use_groggy[index] += 1
                    now_time_damage += increasing_damage
                    if index_cool[index] < 3:
                        now_time_damage_no_cool += increasing_damage
                    elif index_cool[index] / self.total_cool_down > 1000:
                        now_time_damage_ult += increasing_damage
                    elif index_cool[index] / self.total_cool_down > 130:
                        now_time_damage_high += increasing_damage
                    else:
                        now_time_damage_low += increasing_damage
                    break
            damage_trans.append(now_time_damage)
            damage_trans_ult.append(now_time_damage_ult)
            damage_trans_high.append(now_time_damage_high)
            damage_trans_low.append(now_time_damage_low)
            damage_trans_no_cool.append(now_time_damage_no_cool)
        cases = 0
        temp_damage_sum = 0
        for c_sec in range(201, 300):
            cases += 1
            temp_damage_sum += damage_trans[c_sec]
        final_damage_25 = int(temp_damage_sum / cases)
        cases = 0
        temp_damage_sum = 0
        for c_sec in range(301, 500):
            cases += 1
            temp_damage_sum += damage_trans[c_sec]
        final_damage_40 = int(temp_damage_sum / cases)
        cases = 0
        temp_damage_sum = 0
        for c_sec in range(1101, 1200):
            cases += 1
            temp_damage_sum += damage_trans[c_sec]
        final_damage_120 = int(temp_damage_sum / cases)
        # log("damage_trans", damage_trans)
        # log("damage_trans_ult", damage_trans_ult)
        # log("damage_trans_high", damage_trans_high)
        # log("damage_trans_low", damage_trans_low)
        # log("final_damage_40", final_damage_40)
        # log("final_damage_25", final_damage_25)
        # log("final_damage_120", final_damage_120)
        final_active_info = {}
        for i in range(case):
            final_active_info[index_name[i]] = [
                index_damage[i], index_cool[i], index_use[i], index_damage[i] * index_use[i]
            ]
        log("final_active_info", final_active_info)

        self.delete_widget_all("rank{}".format(job_index))
        colors = ['white', 'red', 'SteelBlue1', 'green2']
        tran_max = 50000000
        for i in range(0, 600):
            now_value_total = damage_trans[i * 2]
            now_y = int(start_point[1] + size[1] * now_value_total / tran_max)
            if job_index == 0:  # 주 표시
                now_y_low = int(start_point[1] - 400 * damage_trans_no_cool[i * 2] / tran_max)
                now_y_middle = int(start_point[1] - 400 *
                                   (damage_trans_low[i * 2] + damage_trans_no_cool[i * 2]) / tran_max)
                now_y_high = int(start_point[1] - 400 *
                                 (damage_trans_low[i * 2] + damage_trans_high[i * 2] + damage_trans_no_cool[i * 2])
                                 / tran_max)
                self.canvas.create_line(start_point[0]+i, now_y, start_point[0]+i , now_y_high,
                                        fill=_from_rgb((40, 10, 10)),
                                        width=1, tag="rank{}".format(job_index))
                self.canvas.create_line(start_point[0]+i, now_y_high, start_point[0]+i, now_y_middle,
                                        fill=_from_rgb((10, 10, 40)),
                                        width=1, tag="rank{}".format(job_index))
                self.canvas.create_line(start_point[0]+i, now_y_middle, start_point[0]+i, now_y_low,
                                        fill=_from_rgb((10, 40, 10)),
                                        width=1, tag="rank{}".format(job_index))
                self.canvas.create_line(start_point[0] + i, now_y_low, start_point[0] + i, start_point[1],
                                        fill=_from_rgb((200, 200, 200)),
                                        width=1, tag="rank{}".format(job_index))
                self.canvas.create_line(start_point[0]+i, now_y, start_point[0]+i+1, now_y,
                                        fill=colors[job_index],
                                        width=2, tag="rank{}".format(job_index))
            else:
                self.canvas.create_line(start_point[0] + i, now_y, start_point[0] + i + 1, now_y,
                                        fill=colors[job_index],
                                        width=2, tag="rank{}".format(job_index))

        if job_index == 0:  # 주 표시
            i = 0
            while True:
                try:
                    self.entries['skill_nowLv{}'.format(i)].destroy()
                    self.entries['skill_nowTP{}'.format(i)].destroy()
                    try:
                        self.entries['skill_talisman{}'.format(i)].destroy()
                    except KeyError:
                        pass
                except KeyError:
                    break
                i += 1
            self.canvas.create_text(
                start_point[0]+55, start_point[1]+size[1]+32, font=self.fonts[0], fill='red',
                text='{}%'.format(round(damage_trans_ult[600]/damage_trans[600]*100, 1)),
                anchor='w', tag="rank{}".format(job_index))
            self.canvas.create_text(
                start_point[0]+55, start_point[1]+size[1]+55, font=self.fonts[0], fill='dodger blue',
                text='{}%'.format(round(damage_trans_high[600]/damage_trans[600]*100, 1)),
                anchor='w', tag="rank{}".format(job_index))
            self.canvas.create_text(
                start_point[0]+55, start_point[1]+size[1]+78, font=self.fonts[0], fill='green',
                text='{}%'.format(round(damage_trans_low[600]/damage_trans[600]*100, 1)),
                anchor='w', tag="rank{}".format(job_index))
            self.canvas.create_text(
                start_point[0] + 55, start_point[1]+size[1]+101, font=self.fonts[0], fill=_from_rgb((200, 200, 200)),
                text='{}%'.format(round(damage_trans_no_cool[600] / damage_trans[600] * 100, 1)),
                anchor='w', tag="rank{}".format(job_index))

            self.canvas.create_line(
                start_point[0] + size[0] / 2, start_point[1], start_point[0] + size[0] / 2, start_point[1] + size[1],
                width=1, tag="rank{}", fill='gray')
            i = 0
            for now_skill in detail_active_list:
                # print(now_skill)
                self.canvas.create_text(
                    680, 61+i*25, text=now_skill['requireLv'], font=self.fonts[0],
                    fill='white', tag="rank{}".format(job_index), anchor='c'
                )
                name = now_skill['name'].replace('\n', '')
                self.canvas.create_text(
                    710, 61+i*25, text=name, font=self.fonts[1],
                    fill='white', tag="rank{}".format(job_index), anchor='w', width=85
                )
                self.canvas.create_text(
                    810, 61 + i * 25, text=now_skill['maxLv'], font=self.fonts[0],
                    fill='white', tag="rank{}".format(job_index), anchor='c'
                )
                self.entries['skill_nowLv{}'.format(i)] = tkinter.Entry(self.window, width=4)
                self.entries['skill_nowLv{}'.format(i)].insert(0, now_skill['nowLv'])
                self.entries['skill_nowLv{}'.format(i)].place(x=830, y=50+i*25)
                self.canvas.create_text(
                    880, 61 + i * 25, text=now_skill['maxTp']*10, font=self.fonts[0],
                    fill='white', tag="rank{}".format(job_index), anchor='c'
                )
                self.entries['skill_nowTP{}'.format(i)] = tkinter.Entry(self.window, width=4)
                self.entries['skill_nowTP{}'.format(i)].insert(0, now_skill['nowTp']*10)
                self.entries['skill_nowTP{}'.format(i)].place(x=900, y=50+i*25)
                if now_skill['talisman'] is not None:
                    self.entries['skill_talisman{}'.format(i)] = tkinter.Entry(self.window, width=4)
                    self.entries['skill_talisman{}'.format(i)].insert(0, now_skill['talisman']['available'])
                    self.entries['skill_talisman{}'.format(i)].place(x=950, y=50 + i * 25)
                i += 1

    def save_skill_custom(self):
        try:
            job = self.dropdowns['job0'].get()
            active_data = self.job_main_data["active"]
            for i in range(len(active_data)):
                active_data[i]['nowLv'] = int(self.entries['skill_nowLv{}'.format(i)].get())
                active_data[i]['nowTp'] = round(float(self.entries['skill_nowTP{}'.format(i)].get()) / 10, 1)
                if active_data[i]['talisman'] is not None:
                    active_data[i]['talisman']['available'] = int(self.entries['skill_talisman{}'.format(i)].get())
            self.job_main_data["active"] = active_data
            kor_job_name = translate.get_job_name('jpn', 'kor', job)
            with open('data/job/' + kor_job_name + '.json', 'w', encoding='utf-8') as f:
                json.dump(self.job_main_data, f, indent='\t', ensure_ascii=False)
            self.get_job_data(0)
            self.canvas.itemconfig(self.alert, text="저장 완료", fill='green')
        except:
            self.canvas.itemconfig(self.alert, text="저장 실패", fill='red')

    def create_graph_background(self):
        self.canvas.create_polygon(
            start_point[0], start_point[1],
            start_point[0]+size[0], start_point[1],
            start_point[0]+size[0], start_point[1]+size[1],
            start_point[0], start_point[1]+size[1],
            start_point[0], start_point[1], fill='gray10', width=0
        )
        self.canvas.create_polygon(
            start_point[0], start_point[1]+size[1],
            start_point[0]+105, start_point[1]+size[1],
            start_point[0]+105, start_point[1]+size[1]+113,
            start_point[0], start_point[1]+size[1]+113,
            start_point[0], start_point[1]+size[1], fill='black', outline='gray', width=2
        )
        self.canvas.create_line(start_point[0], start_point[1]+size[1]+20,
                                start_point[0]+105, start_point[1]+size[1]+20, width=2, fill='gray')
        self.canvas.create_text(start_point[0]+52, start_point[1]+size[1]+10, font=self.fonts[0], fill='white',
                                text="스킬비중", anchor='c')
        self.canvas.create_text(start_point[0]+5, start_point[1]+size[1]+32, font=self.fonts[0], fill='red',
                                text="각성=", anchor='w')
        self.canvas.create_text(start_point[0]+5, start_point[1]+size[1]+55, font=self.fonts[0], fill='dodger blue',
                                text="상위=", anchor='w')
        self.canvas.create_text(start_point[0]+5, start_point[1]+size[1]+78, font=self.fonts[0], fill='green',
                                text="하위=", anchor='w')
        self.canvas.create_text(start_point[0]+5, start_point[1]+size[1]+101, font=self.fonts[0],
                                fill=_from_rgb((200, 200, 200)), text="평타=", anchor='w')
        self.canvas.create_line(start_point[0], start_point[1] + size[1] + 44,
                                start_point[0] + 105, start_point[1] + size[1] + 44, width=1, fill='gray')
        self.canvas.create_line(start_point[0], start_point[1] + size[1] + 67,
                                start_point[0] + 105, start_point[1] + size[1] + 67, width=1, fill='gray')
        self.canvas.create_line(start_point[0], start_point[1] + size[1] + 90,
                                start_point[0] + 105, start_point[1] + size[1] + 90, width=1, fill='gray')
        for i in range(0, 13):
            self.canvas.create_text(
                start_point[0]+size[0]/12*i, start_point[1]+10, text=str(i*10), font=self.fonts[0], fill='white'
            )
        self.canvas.create_line(665, 45, 990, 45, width=2, fill='white')
        self.canvas.create_text(680, 30, text="습득\n레벨", font=self.fonts[1], fill='white', anchor='c')
        self.canvas.create_text(752, 30, text="스킬명", font=self.fonts[1], fill='white', anchor='c')
        self.canvas.create_text(810, 30, text="최대\n레벨", font=self.fonts[1], fill='white', anchor='c')
        self.canvas.create_text(847, 30, text="입력\n레벨", font=self.fonts[1], fill='white', anchor='c')
        self.canvas.create_text(880, 30, text="TP%\n최대", font=self.fonts[1], fill='white')
        self.canvas.create_text(917, 30, text="TP%\n입력", font=self.fonts[1], fill='white')
        self.canvas.create_text(967, 30, text="탈리\n슬롯", font=self.fonts[1], fill='white', anchor='c')

        self.alert = self.canvas.create_text(800, 654, text="", font=self.fonts[0], fill='red', anchor='w')

    def delete_widget_all(self, tag):
        while len(self.canvas.find_withtag(tag)) != 0:
            self.canvas.delete(tag)


def log(name, value):
    print(name + " = " + str(value))


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb






