import tkinter
import tkinter.ttk
import common
import data.load_job
import os


index_passive = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 48, 50, 60, 70, 75, 80, 85, 95, 100]
index_active = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80, 85, 95, 100]
leveling_efficiency = [0, 0.05, 0.101443, 0.159328, 0, 0.231886]


class JobRank:
    def __init__(self, master):
        self.colors = common.load_color()  # [dark_main, dark_sub, dark_blue, result_sub]
        self.fonts = common.load_font()  # [guide_font, small_font, mid_font, big_font]
        self.window = tkinter.Toplevel(master)
        self.window.geometry("800x600")
        self.canvas = None
        self.dropdowns = {}

        self.weapon_type = "공통"
        self.active_leveling_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.passive_leveling_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ult_damage_arr = [1, 1, 1]
        self.equipments_sets = []
        self.total_cool_down = 0.8
        self.fix_delay = 0.5
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
        self.canvas = tkinter.Canvas(self.window, width=900, height=700, bd=0, bg=self.colors[0])
        self.canvas.place(x=-2, y=-2)

        for i in range(0, 4):
            self.dropdowns['job{}'.format(i)] = tkinter.ttk.Combobox(
                self.window, values=self.job_list, width=10
            )
            self.dropdowns['job{}'.format(i)].set("-직업 선택-")
            self.dropdowns['job{}'.format(i)].place(x=90, y=10+40*i)
            self.dropdowns['job{}'.format(i)].bind(
                "<<ComboboxSelected>>", lambda event, job_index=i:
                self.get_job_tran(job_index)
            )

    def get_job_tran(self, job_index):
        job = self.dropdowns['job{}'.format(job_index)].get()
        try:
            job_detail_data = data.load_job.load_job_json(job)
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
            if cool_time is None:
                cool_time = 0
            cool_time = round(cool_time * weapon_cool_rate * self.total_cool_down, 1)
            # log("스킬명", active["name"])
            # log("damage", damage)
            # log("cool_time", cool_time)
            active_dict[active["name"]] = [damage, cool_time, skill_delay]
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
                    value_list[index] = value_list[index] * total_rate
            else:
                target_list = passive["target"].split("^")  # ^ 구분자를 기준으로 split
                for name, value_list in active_dict.items():
                    if target_list.__contains__(name):
                        value_list[index] = value_list[index] * total_rate
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
                    value_list[index] = value_list[index] * value
            else:
                target_list = special["target"].split("^")  # ^ 구분자를 기준으로 split
                for name, value_list in active_dict.items():
                    if target_list.__contains__(name):
                        # print(name + " 조건부 발동 확인됨")
                        value_list[index] = value_list[index] * value

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
        index_use = []
        index_use_total = []
        index_use_sustain = []
        delay_time = []
        for name, value_list in active_dict.items():
            if value_list[1] == 0:
                # 무쿨타임(평타)는 일단 제외
                continue
            case += 1
            index_name.append(name)
            value_list[0] = int(value_list[0] * self.damage_ratio)  # 혹시 환산할 일 생기면 여기를 바꾸면 된다
            index_damage.append(value_list[0])
            index_cool.append(int(value_list[1] * 10))
            index_delay.append(int(value_list[2] * 10))
            delay_time.append(0)
            index_use.append(0)
        # log("active_dict", active_dict)
        damage_trans = []
        damage_trans_ult = []
        damage_trans_high = []
        damage_trans_low = []
        now_time_damage = 0
        now_time_damage_ult = 0
        now_time_damage_high = 0
        now_time_damage_low = 0
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
                continue
            for index in range(case):
                if delay_time[index] <= 0:
                    index_use[index] += 1
                    cannot_damage_time = index_delay[index] + self.fix_delay
                    delay_time[index] = index_cool[index]
                    if c_sec > 400:
                        increasing_damage = int(index_damage[index] * 0.6)
                    else:
                        increasing_damage = int(index_damage[index])
                    now_time_damage += increasing_damage
                    if index_cool[index] / self.total_cool_down > 1000:
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
        log("damage_trans", damage_trans)
        log("damage_trans_ult", damage_trans_ult)
        log("damage_trans_high", damage_trans_high)
        log("damage_trans_low", damage_trans_low)
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
        start_point = [30, 530]
        colors = ['white', 'red', 'SteelBlue1', 'green2']
        tran_max = 50000000
        for i in range(0, 600):
            now_value_total = damage_trans[i * 2]
            now_y = int(start_point[1] - 400 * now_value_total / tran_max)
            if job_index == 0:  # 주 표시
                now_y_low = int(start_point[1] - 400 * damage_trans_low[i * 2] / tran_max)
                now_y_high = int(start_point[1] - 400 *
                                 (damage_trans_low[i * 2] + damage_trans_high[i * 2]) / tran_max)
                self.canvas.create_line(start_point[0]+i, now_y, start_point[0]+i+1, now_y_high,
                                        fill=_from_rgb((40, 10, 10)),
                                        width=1, tag="rank{}".format(job_index))
                self.canvas.create_line(start_point[0]+i, now_y_high, start_point[0]+i+1, now_y_low,
                                        fill=_from_rgb((10, 10, 40)),
                                        width=1, tag="rank{}".format(job_index))
                self.canvas.create_line(start_point[0]+i, now_y_low, start_point[0]+i+1, start_point[1],
                                        fill=_from_rgb((10, 40, 10)),
                                        width=1, tag="rank{}".format(job_index))
                self.canvas.create_line(start_point[0]+i, now_y, start_point[0]+i+1, now_y,
                                        fill=colors[job_index],
                                        width=2, tag="rank{}".format(job_index))
            else:
                self.canvas.create_line(start_point[0] + i, now_y, start_point[0] + i + 1, now_y,
                                        fill=colors[job_index],
                                        width=2, tag="rank{}".format(job_index))

    def create_graph_background(self):
        start_point = [30, 530]
        size = [600, -400]
        self.canvas.create_polygon(
            start_point[0], start_point[1],
            start_point[0]+size[0], start_point[1],
            start_point[0]+size[0], start_point[1]+size[1],
            start_point[0], start_point[1]+size[1],
            start_point[0], start_point[1], fill='gray10', width=0
        )

    def delete_widget_all(self, tag):
        while len(self.canvas.find_withtag(tag)) != 0:
            self.canvas.delete(tag)


def log(name, value):
    print(name + " = " + str(value))


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb






