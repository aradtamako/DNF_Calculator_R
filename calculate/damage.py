import calculate.calculation
import data.load_job
from collections import Counter
from itertools import product

hexagon_option_index = [2, 3, 4, 6, 7, 8, 0, 0, 0, 0]
hexagon_option_index_reverse = [9, '', 0, 1, 2, '', 3, 4, 5, 0]

index_passive = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 48, 50, 60, 70, 75, 80, 85, 95, 100]
index_active = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80, 85, 95, 100]
leveling_efficiency = [0, 0.05, 0.101443, 0.159328, 0, 0.231886]

simple_sum_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]
complex_sum_index = [11, 28, 29, 30]
not_set_list = ['136', '137', '138', '144', '145', '146', '147', '148', '149', '161']

michelle = 3.31
standard_stat = 54500
standard_dealer_stat = 16000
standard_buffer_solo_stat = 5450
standard_dealer_solo_stat = 4000
standard_atk_point = 4800
standard_solo_atk_point = 2764
standard_base_element = 13
standard_leveling_efficiency = [0.0213, 0.0652956, 0.04, 0.1203, 0.0674, 0.1882527]


class Damage:
    """nowDamageArray index
     * 0: 추가 스탯 수치
     * 1: 추가 공격력 수치
     * 2: 데미지 추가 증가
     * 3: 크리티컬 데미지 추가 증가
     * 4: 추가 데미지
     * 5: 속성 추가 데미지
     * 6: 모든 공격력 증가
     * 7: 공격력 % 증가
     * 8: 힘, 지능 % 증가
     * 9: 속성 강화
     * 10: 지속 데미지
     * 11: 스킬 공격력 증가
     * 12: 기타 특수성 데미지
     * 13: 공격속도 증가
     * 14: 크리티컬 확률 증가
     * 15~20: 액티브 레벨링 (1~45, 50, 60~80, 85, 95, 100)
     * 21~24: (안 쓰임)패시브 레벨링(전직패, 1각패, 2각패, 진각패)
     * 25: 기타 특수성 액티브 레벨링 실효율%
     * 26: 쿨타임 감소(진각캐 기준)
     * 27: 쿨타임 감소(2각캐 기준)
     * 28~30: 50,85,100레벨 스킬 공격력 증가
     """
    base_element = 131 + 25 + 7 + 60 - 50
    cool_efficiency_groggy = 0.2
    cool_efficiency_sustain = 0.7
    ratio_groggy_sustain = 0.5
    is_cool_down_on = 1

    def __init__(self, job, basic_damage_arr, basic_leveling_arr, is_calc_detail,
                 is_scent2_on, scent_option_input,
                 purgatory_option_input, purgatory_value_input, purgatory_weapon_ult_input,
                 purgatory_auto_converting_weapon_ult_mode):
        job_data = calculate.calculation.dealer_job_data[job]
        self.job_active_efficiency = job_data['nowJobActiveLevelingArray']
        self.job_passive_efficiency = job_data['nowJobPassiveLeveling']
        self.job_basic_element = job_data['nowBasicSkillElementalReinforce']
        self.job_passive_element = job_data['nowLvSkillElementalReinforce']

        self.weapon_type = "공통"
        self.basic_damage_arr = basic_damage_arr
        self.basic_leveling_arr = basic_leveling_arr

        self.is_calc_detail = is_calc_detail
        if is_calc_detail is True:
            try:
                job_detail_data = data.load_job.load_job_json(job)
                self.detail_active_list = job_detail_data["active"]
                self.detail_passive_list = job_detail_data["passive"]
                self.detail_special_list = job_detail_data["special"]
                self.detail_weapon_list = job_detail_data["weapon"]
                self.is_job_detail = True
            except FileNotFoundError:
                print("직업 계수 데이터 미존재")
                self.is_job_detail = False
        else:
            self.is_job_detail = False
            self.detail_code = None

        self.job_active_sum_groggy = sum(self.job_active_efficiency)
        self.job_active_sum_sustain = sum([self.job_active_efficiency[i] for i in [0, 2, 4]])
        self.job_active_sum_ult = sum([self.job_active_efficiency[i] for i in [1, 3, 5]])

        self.selected_stat_efficiency = standard_stat / 250 + 1
        self.selected_atk_point = standard_atk_point

        self.is_scent2_on = is_scent2_on
        self.scent_option_input = scent_option_input

        self.purgatory_auto_converting_weapon_ult_mode = purgatory_auto_converting_weapon_ult_mode
        self.purgatory_weapon_ult_input = purgatory_weapon_ult_input
        self.purgatory_converting_option = purgatory_option_input  # 변경 될 리스트
        self.purgatory_converting_value_fixed = purgatory_value_input # 변경 될 추가 값
        self.purgatory_converting_value = []
        self.purgatory_converted_option = [0, 0, 0, 0]  # 변경 전 리스트
        self.purgatory_converted_value = [0, 0, 0, 0]  # 변경 전 값
        self.purgatory_ult_value = 0
        self.converting_value_arr = []
        self.total_auto_converting_value = []

        self.auto_converting_index = [9, 9, 9, 9, 9, 9]
        self.total_converting_index = [0, 0, 0, 0, 0, 0]
        self.total_converting_value = [0, 0, 0, 0, 0, 0]

    now_damage_array = []
    now_leveling_array = []
    equipments_sets = []

    def get_detail_code(self, code):
        # detail_code
        # 0: total
        # 1: groggy
        # 2: sustain
        # 3: ult
        self.detail_code = code

    def prepare_calc(self):
        self.purgatory_converting_value = self.purgatory_converting_value_fixed.copy()
        self.now_damage_array = self.basic_damage_arr.copy()
        self.now_leveling_array = self.basic_leveling_arr.copy()
        self.total_converting_value = [0, 0, 0, 0, 0, 0]
        self.total_converting_index = [0, 0, 0, 0, 0, 0]
        self.auto_converting_index = [9, 9, 9, 9, 9, 9]
        self.total_converting_index[0] = self.scent_option_input[0]
        self.total_converting_index[1] = self.scent_option_input[1]
        for i in range(4):
            self.total_converting_index[i + 2] = self.purgatory_converting_option[i]
        self.purgatory_converted_option = [0, 0, 0, 0]
        self.purgatory_converted_value = [0, 0, 0, 0]
        self.total_auto_converting_value = []
        self.converting_value_arr = [0, 0, 0, 0, 0, 0]
        if self.scent_option_input[0] == 9:
            self.total_auto_converting_value.append(10)
            self.converting_value_arr[0] = 10
            self.total_converting_value[0] = 10
            if self.is_scent2_on:
                self.total_auto_converting_value.append(5)
                self.converting_value_arr[1] = 5
                self.total_converting_value[1] = 10
        else:
            self.total_converting_index[0] = self.scent_option_input[0]
            if self.is_scent2_on:
                self.total_converting_index[1] = self.scent_option_input[1]
            else:
                self.total_converting_index[1] = 0
        self.purgatory_ult_value = 0

    def combine_damage_option(self, equipments):
        self.prepare_calc()
        # log("equipments", equipments)

        sets = []
        size = len(equipments)
        set_list = ["1" + equipments[x][2:4] for x in range(size)
                    if len(equipments[x]) == 5]
        set_val = Counter(set_list)
        for key, num in set_val.items():
            if num > 1:
                sets.append(key + str(int(num * 0.7)))
                size += 1
        # log("sets", sets)

        damage_list = []
        leveling_list = []

        self.equipments_sets = equipments + sets

        for equipment in self.equipments_sets:
            try:  # 장비 옵션 조회
                damage_list.append(calculate.calculation.equipment_damage_option[equipment])
                leveling_list.append(calculate.calculation.equipment_leveling_option[equipment])
            except KeyError:
                print(equipment, "누락")

            now_purgatory = calculate.calculation.equipment_purgatory_option[equipment]  # 연옥 옵션 조회
            if now_purgatory[0] != 0:
                if len(equipment) == 6:  # 무기
                    self.weapon_type = calculate.calculation.equipment_type_by_code[equipment]
                    # log("self.weapon_type", self.weapon_type)
                    if now_purgatory[0] == 106 and self.purgatory_converting_option[0] != 0:  # 원초
                        self.purgatory_converted_value[0] = 0
                        self.purgatory_converting_value[0] = 0
                        self.now_damage_array[6] += 15
                    else:
                        now_index = 0
                        if now_purgatory[0] == 27:
                            self.purgatory_converted_option[now_index] = 0
                            self.purgatory_converted_value[now_index] = 0
                        else:
                            self.purgatory_converted_option[now_index] = now_purgatory[0]
                            self.purgatory_converted_value[now_index] = now_purgatory[1]

                        if self.purgatory_converting_option[0] == 0:
                            continue
                        elif self.purgatory_converting_option[0] == 9:
                            # 각성 토글 판정식
                            if self.purgatory_auto_converting_weapon_ult_mode == 1:  # 연옥 무기 태생유지
                                if now_purgatory[0] != 27:
                                    self.purgatory_converted_value[now_index] = 14
                            elif self.purgatory_auto_converting_weapon_ult_mode == 2:  # 연옥 무기 각성강제
                                if now_purgatory[0] != 27:
                                    self.purgatory_ult_value += 2
                                    self.purgatory_converting_value[now_index] -= 14
                            else:  # 연옥 무기 각성해제
                                if now_purgatory[0] == 27:
                                    self.purgatory_ult_value -= 2
                                    self.purgatory_converting_value[now_index] += 14
                        else:
                            if self.purgatory_weapon_ult_input:
                                if now_purgatory[0] != 27:
                                    self.purgatory_ult_value += 2
                                    self.purgatory_converting_value[now_index] -= 14
                            else:
                                if now_purgatory[0] == 27:
                                    self.purgatory_ult_value -= 2
                                    self.purgatory_converted_value[now_index] = 0
                                    self.purgatory_converting_value[now_index] += 14
                else:
                    now_index = int(equipment[0])
                    self.purgatory_converted_option[now_index] = now_purgatory[0]
                    self.purgatory_converted_value[now_index] = now_purgatory[1]

        for i in range(4):
            if self.purgatory_converting_option[i] == 0:
                self.purgatory_converted_value[i] = 0
            elif self.purgatory_converting_option[i] == 9:
                self.now_damage_array[self.purgatory_converted_option[i]] -= self.purgatory_converted_value[i]
                self.total_auto_converting_value.append(
                    self.purgatory_converted_value[i] + self.purgatory_converting_value[i]
                )
            else:
                self.now_damage_array[self.purgatory_converted_option[i]] -= self.purgatory_converted_value[i]
                self.total_converting_value[i + 2] = \
                    self.purgatory_converted_value[i] + self.purgatory_converting_value[i]
                self.now_damage_array[self.purgatory_converting_option[i]] += self.total_converting_value[i + 2]
                self.purgatory_converting_value[i] = 0
                self.purgatory_converted_value[i] = 0

        for index in simple_sum_index:
            self.now_damage_array[index] += sum([damage_list[x][index] for x in range(0, size)])
        for index in complex_sum_index:
            self.now_damage_array[index] = multiply_list([damage_list[x][index] for x in range(0, size)])
        self.now_damage_array[26] = anti_multiply_list([damage_list[x][26] for x in range(0, size)])
        for i in range(19):
            self.now_leveling_array[i] += sum([leveling_list[x][i] for x in range(0, size)])
        self.now_leveling_array[18] += self.purgatory_ult_value
        self.now_leveling_array[16] += self.purgatory_ult_value
        self.now_leveling_array[11] += self.purgatory_ult_value
        # log("self.now_damage_array", self.now_damage_array)
        # log("self.now_leveling_array", self.now_leveling_array)
        self.total_auto_converting_value.sort(reverse=True)
        # log("total_auto_converting_value", self.total_auto_converting_value)

    def calculate_damage(self):
        job_element = self.job_basic_element + sum([self.job_passive_element[i] * self.now_leveling_array[i]
                                                    for i in range(19)])
        self.now_damage_array[9] += job_element + self.base_element + standard_base_element
        # log("total_element", self.now_damage_array[9])

        self.now_damage_array[4] += \
            (1.05 + 0.0045 * self.now_damage_array[9]) * self.now_damage_array[5]
        # log("total_additional_damage", self.now_damage_array[4])

        if self.is_calc_detail:  # 정밀 계산 모드
            # 1. 변환 옵션 정밀 재계산
            simple_sum_options = [self.now_damage_array[2], self.now_damage_array[3], self.now_damage_array[4],
                                  self.now_damage_array[6], self.now_damage_array[7], self.now_damage_array[8]]
            converting_index_arr = []
            for i in range(4):
                self.converting_value_arr[i + 2] = self.purgatory_converting_value[i] + self.purgatory_converted_value[
                    i]
            # log("converting_value_arr", self.converting_value_arr)
            for v in self.converting_value_arr:
                if v == 0:
                    converting_index_arr.append([9])
                else:
                    converting_index_arr.append([0, 1, 2, 3, 4, 5])
            # log("converting_index_arr", converting_index_arr)
            all_cases = list(product(*converting_index_arr))
            # log("all_cases", all_cases)
            max_damage = 0
            max_sum_options = [0, 0, 0, 0, 0, 0]
            for case in all_cases:
                now_damage = 1
                now_sum_options = simple_sum_options.copy()
                for index, value in enumerate(case):
                    if value == 9:
                        continue
                    now_sum_options[value] += self.converting_value_arr[index]
                for v in now_sum_options:
                    now_damage = now_damage * (v / 100 + 1)
                if max_damage < now_damage:
                    max_damage = now_damage
                    max_sum_options = now_sum_options
                    self.auto_converting_index = case
            # log("auto_converting_index", self.auto_converting_index)
            # log("max_sum_options", max_sum_options)
            for i in range(6):
                if self.total_converting_index[i] == 9:
                    self.total_converting_index[i] = hexagon_option_index[self.auto_converting_index[i]]
            for i, value in enumerate(max_sum_options):
                self.now_damage_array[hexagon_option_index[i]] = value
            # log("total_converting_index", self.total_converting_index)

            # 2. 계수 정밀계산
            damage_tran_array = []
            if self.is_job_detail:
                # 무기 보정 판정
                weapon_atk_rate = 1
                weapon_cool_rate = 1
                if self.weapon_type == "공통":
                    pass
                else:
                    for weapon in self.detail_weapon_list:
                        if self.weapon_type == weapon["type"]:
                            weapon_atk_rate = weapon["damage"]
                            weapon_cool_rate = weapon["coolTime"]
                            break
                # 구간별 쿨타임 감소 계산
                cool_down_list = []
                cool_recover_list = []
                size = len(self.equipments_sets)
                for equipment in self.equipments_sets:
                    try:
                        cool_down_list.append(calculate.calculation.equipment_cool_down_option[equipment])
                        cool_recover_list.append(calculate.calculation.equipment_cool_recover_option[equipment])
                    except KeyError:
                        print(equipment, "누락")
                total_cool_down = []
                for i in range(0, 18):
                    now_cool_down = anti_multiply_list([cool_down_list[x][i] for x in range(0, size)])
                    now_cool_recover = sum([cool_recover_list[x][i] for x in range(0, size)])
                    total_cool_down.append((1 - now_cool_down / 100) / (1 + now_cool_recover / 100) * weapon_cool_rate)
                # log("total_cool_down", total_cool_down)

                # 액티브 정리
                ult_name = []
                active_leveling_arr = self.now_leveling_array.copy()
                # 사전에 패시브 전용 레벨링 제거
                if self.equipments_sets.__contains__("111016"):
                    active_leveling_arr[5] -= 3
                elif self.equipments_sets.__contains__("111024"):
                    active_leveling_arr[3] -= 1
                elif self.equipments_sets.__contains__("111029"):
                    active_leveling_arr[14] -= 2
                elif self.equipments_sets.__contains__("111036"):
                    active_leveling_arr[10] -= 4
                elif self.equipments_sets.__contains__("111059"):
                    active_leveling_arr[5] -= 1.5
                elif self.equipments_sets.__contains__("111060"):
                    active_leveling_arr[5] -= 2
                    active_leveling_arr[10] -= 2
                    active_leveling_arr[14] -= 2
                elif self.equipments_sets.__contains__("111062"):
                    active_leveling_arr[10] -= 3
                    active_leveling_arr[14] -= 3
                elif self.equipments_sets.__contains__("111069"):
                    active_leveling_arr[10] -= 3
                    active_leveling_arr[14] -= 3
                elif self.equipments_sets.__contains__("111075"):
                    active_leveling_arr[4] -= 4.5
                active_dict = {}
                for active in self.detail_active_list:
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
                    up_lv = active_leveling_arr[index_passive.index(active["requireLv"])]
                    now_tp = active["nowTp"]
                    max_tp = active["maxTp"]
                    skill_delay = active["delay"]
                    now_eff = leveling_efficiency[active["gapLv"]]
                    damage = int(damage *
                                 (1 + now_eff * (now_lv + up_lv - 1)) / (1 + now_eff * (max_lv - 1)) *
                                 (1 + 0.1 * now_tp) / (1 + 0.1 * max_tp) *
                                 weapon_atk_rate)
                    if active["requireLv"] == 50:
                        if now_lv != 0:
                            ult_name.append(active["name"])
                        damage = int(damage * (self.now_damage_array[28] / 100 + 1))
                    elif active["requireLv"] == 85:
                        if now_lv != 0:
                            ult_name.append(active["name"])
                        damage = int(damage * (self.now_damage_array[29] / 100 + 1))
                    elif active["requireLv"] == 100:
                        if now_lv != 0:
                            ult_name.append(active["name"])
                        damage = int(damage * (self.now_damage_array[30] / 100 + 1))
                    if cool_time is None:
                        cool_time = 0
                    cool_time = round(cool_time * total_cool_down[index_active.index(active["requireLv"])], 1)
                    # log("스킬명", active["name"])
                    # log("damage", damage)
                    # log("cool_time", cool_time)
                    active_dict[active["name"]] = [damage, cool_time, skill_delay]
                # log("active_dict", active_dict)

                # 패시브 레벨링 판정
                for passive in self.detail_passive_list:
                    requirement_type = passive["requirementType"]
                    if requirement_type is None:
                        is_condition = True
                    else:
                        is_condition = False
                    if requirement_type == "WEAPON":
                        if passive["requirementValue"][-1] != "!" and self.weapon_type == "공통":
                            is_condition = True
                        elif self.weapon_type == passive["requirementValue"]:
                            is_condition = True
                    up_lv = self.now_leveling_array[index_passive.index(passive["requireLv"])]
                    if is_condition is False:
                        continue
                    if passive["type"] == "DAMAGE":
                        index = 0
                        standard_value = 100 + passive["maxValue"]
                        now_value = standard_value + up_lv * passive["upValue"]
                    else:
                        index = 1
                        standard_value = 100 - passive["maxValue"]
                        now_value = standard_value - up_lv * passive["upValue"]
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

                # 특수 처리
                for special in self.detail_special_list:
                    requirement_type = special["requirementType"]
                    if requirement_type is None:
                        is_condition = True
                    else:
                        is_condition = False
                    if requirement_type == "WEAPON":
                        if special["requirementValue"][-1] != "!" and self.weapon_type == "공통":
                            is_condition = True
                        elif self.weapon_type == special["requirementValue"]:
                            is_condition = True
                    if is_condition is False:
                        continue
                    if special["type"] == "DAMAGE":
                        index = 0
                        value = special["value"] / 100 + 1
                    else:
                        index = 1
                        value = 1 - special["value"] / 100
                    if special["target"] == "ALL":
                        for name, value_list in active_dict.items():
                            value_list[index] = value_list[index] * value
                    else:
                        target_list = special["target"].split("^")  # ^ 구분자를 기준으로 split
                        for name, value_list in active_dict.items():
                            if target_list.__contains__(name):
                                value_list[index] = value_list[index] * value

                for name, value_list in active_dict.items():
                    value_list[0] = int(value_list[0])
                    value_list[1] = round(value_list[1], 1)
                # log("active_dict", active_dict)

        else:  # 간이식 계산 모드
            simple_sum_options = [self.now_damage_array[2], self.now_damage_array[3], self.now_damage_array[4],
                                  self.now_damage_array[6], self.now_damage_array[7], self.now_damage_array[8]]
            for now_value in self.total_auto_converting_value:
                simple_sum_options[simple_sum_options.index(min(simple_sum_options))] += now_value
            for i, value in enumerate(simple_sum_options):
                self.now_damage_array[hexagon_option_index[i]] = value

        total_stat_efficiency = ((self.now_damage_array[0] + standard_stat) * (1 + self.now_damage_array[8] / 100)
                                 / 250 + 1) / self.selected_stat_efficiency
        # log("total_stat_efficiency", total_stat_efficiency)
        # log("total_atk_efficiency", (self.now_damage_array[1] + self.selected_atk_point) / self.selected_atk_point)
        total_damage_no_active = (total_stat_efficiency *
                                  (self.now_damage_array[1] + self.selected_atk_point) / self.selected_atk_point *
                                  (self.now_damage_array[2] / 100 + 1) *
                                  (self.now_damage_array[3] / 100 + 1) *
                                  (self.now_damage_array[4] / 100 + 1) *
                                  (self.now_damage_array[6] / 100 + 1) *
                                  (self.now_damage_array[7] / 100 + 1) *
                                  (self.now_damage_array[9] * 0.0045 + 1.05) /
                                  (self.job_basic_element * 0.0045 + 1.05) *
                                  (self.now_damage_array[10] / 100 + 1) *
                                  (self.now_damage_array[11] / 100 + 1))
        # log("total_damage_no_active", total_damage_no_active)

        if self.is_job_detail and self.is_calc_detail:
            final_damage_ult = 0
            case = 0
            index_name = []
            index_cool = []
            index_damage = []
            index_delay = []
            index_use = []
            for name, value_list in active_dict.items():
                if value_list[1] == 0:
                    # 무쿨타임(평타)는 일단 제외
                    continue
                case += 1
                value_list[0] = int(value_list[0] * total_damage_no_active / 383.20)
                index_damage.append(value_list[0])
                index_cool.append(int(value_list[1]*10*0.8))  # 0.8 정신자극
                index_delay.append(int(value_list[2]*10))
                if ult_name.__contains__(name):
                    final_damage_ult += value_list[0]
            # log("active_dict", active_dict)

            damage_trans = []
            damage_25 = 0
            delay_25 = 0
            delay_time = []
            # 초반 25초: 쿨타임 위주의 계산
            for index in range(case):
                interval_time = index_cool[index]+index_delay[index]
                if interval_time > 270:
                    use = 1
                    delay_time.append(index_cool[index] - 250)
                elif interval_time > 130:
                    delay_time.append(int(index_cool[index] / 2 + 190) - 250)
                    use = 2
                elif interval_time > 86:
                    delay_time.append(int(index_cool[index] / 2 + 210) - 250)
                    use = 3
                elif interval_time > 62:
                    delay_time.append(int(index_cool[index] / 2 + 230) - 250)
                    use = 4
                else:
                    delay_time.append(int(index_cool[index] / 2 + 250) - 250)
                    use = 5
                damage_25 += index_damage[index] * use
                delay_25 += index_delay[index] * use
                index_use.append(use)
            for i in range(len(delay_time)):
                if delay_time[i] < 0:
                    delay_time[i] = 0
            # log("damage_25", damage_25)

            # 중후반 25~초: 쿨타임과 딜레이의 종합 계산
            now_time_damage = damage_25
            for c_sec in range(0, 251):
                damage_trans.append(now_time_damage)
            for c_sec in range(251, 1200):
                for index in range(case):
                    delay_time[index] -= 1
                    if delay_time[index] == 0:
                        delay_time[index] += index_cool[index] + index_delay[index]
                        if c_sec > 40:
                            now_time_damage += index_damage[index] * 0.6
                        else:
                            now_time_damage += index_damage[index]
                damage_trans.append(now_time_damage)
            cases = 0
            temp_damage_sum = 0
            for c_sec in range(245, 261):
                cases += 1
                temp_damage_sum += damage_trans[c_sec]
            final_damage_25 = int(temp_damage_sum / cases)
            cases = 0
            temp_damage_sum = 0
            for c_sec in range(391, 420):
                cases += 1
                temp_damage_sum += damage_trans[c_sec]
            final_damage_40 = int(temp_damage_sum / cases)
            cases = 0
            temp_damage_sum = 0
            for c_sec in range(1100, 1200):
                cases += 1
                temp_damage_sum += damage_trans[c_sec]
            final_damage_120 = int(temp_damage_sum / cases)
            # log("final_damage_40", final_damage_40)
            # log("final_damage_25", final_damage_25)
            # log("final_damage_120", final_damage_120)
            return [
                final_damage_40, final_damage_25, final_damage_120, final_damage_ult,
                damage_trans, self.now_damage_array, self.now_leveling_array
            ]

        else:
            total_passive_damage = 1
            for i in range(19):
                total_passive_damage = total_passive_damage * (1 + self.job_passive_efficiency[i] *
                                                               self.now_leveling_array[i])
            # log("total_passive_damage", total_passive_damage)

            self.now_damage_array[16] += self.purgatory_ult_value
            self.now_damage_array[18] += self.purgatory_ult_value
            self.now_damage_array[20] += self.purgatory_ult_value
            active_ratio_arr = \
                [(self.now_damage_array[i + 15] * standard_leveling_efficiency[i] + 1) * self.job_active_efficiency[i]
                 for i in range(6)]
            active_ratio_arr[1] = active_ratio_arr[1] * (self.now_damage_array[28] / 100 + 1)
            active_ratio_arr[3] = active_ratio_arr[3] * (self.now_damage_array[29] / 100 + 1)
            active_ratio_arr[5] = active_ratio_arr[5] * (self.now_damage_array[30] / 100 + 1)
            # log("active_ratio_arr", active_ratio_arr)

            active_efficiency_groggy = sum(active_ratio_arr) / self.job_active_sum_groggy
            active_efficiency_sustain = sum([active_ratio_arr[i] for i in [0, 2, 4]]) / self.job_active_sum_sustain
            active_efficiency_ult = sum([active_ratio_arr[i] for i in [1, 3, 5]]) / self.job_active_sum_ult
            # log("active_efficiency_groggy", active_efficiency_groggy)
            # log("active_efficiency_sustain", active_efficiency_sustain)
            # log("active_efficiency_ult", active_efficiency_ult)

            cool_down_point = (1 - self.now_damage_array[26] / 100)
            cool_down_value = (1.0 / cool_down_point - 1.0) / (
                    ((1 - cool_down_point) / 0.55) * ((1 - cool_down_point) / 0.55) * (
                        (1 - cool_down_point) / 0.55) + 1)
            cool_down_groggy = cool_down_value * self.cool_efficiency_groggy + 1
            cool_down_sustain = cool_down_value * self.cool_efficiency_sustain + 1

            total_damage = total_damage_no_active * total_passive_damage

            total_damage_groggy = total_damage * cool_down_groggy * (
                    active_efficiency_groggy + self.now_damage_array[12] / 100)
            total_damage_sustain = total_damage * cool_down_sustain * (
                    active_efficiency_sustain + self.now_damage_array[12] / 100)
            total_damage_ult = total_damage * active_efficiency_ult
            total_damage_sum = (total_damage_groggy * self.ratio_groggy_sustain +
                                total_damage_sustain * (1 - self.ratio_groggy_sustain))
            # log("total_damage_groggy", total_damage_groggy)
            # log("total_damage_sustain", total_damage_sustain)
            # log("total_damage_ult", total_damage_ult)
            # log("total_damage_sum", total_damage_sum)

            # log("now_damage_array", self.now_damage_array)
            return [total_damage_sum, total_damage_groggy, total_damage_sustain, total_damage_ult,
                    [0], self.now_damage_array, self.now_leveling_array]


def multiply_list(arr):
    return_value = 0
    for value in arr:
        return_value = (return_value / 100 + 1) * (value / 100 + 1) * 100 - 100
    return return_value


def anti_multiply_list(arr):
    return_value = 0
    for value in arr:
        return_value = 100 - (1 - return_value / 100) * (1 - value / 100) * 100
    return return_value


def log(name, value):
    print(name + " = " + str(value))
