import calculate.calculation
from collections import Counter
from itertools import product

hexagon_option_index = [2, 3, 4, 6, 7, 8, 0, 0, 0, 0]
hexagon_option_index_reverse = [9, '', 0, 1, 2, '', 3, 4, 5, 0]

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

        self.basic_damage_arr = basic_damage_arr
        self.basic_leveling_arr = basic_leveling_arr

        self.is_calc_detail = is_calc_detail

        self.job_active_sum_groggy = sum(self.job_active_efficiency)
        self.job_active_sum_sustain = sum([self.job_active_efficiency[i] for i in [0, 2, 4]])
        self.job_active_sum_ult = sum([self.job_active_efficiency[i] for i in [1, 3, 5]])

        self.basic_damage_arr[9] += (self.base_element + standard_base_element)

        self.selected_stat_efficiency = standard_stat / 250 + 1
        self.selected_atk_point = standard_atk_point

        self.is_scent2_on = is_scent2_on
        self.scent_option_input = scent_option_input

        self.purgatory_auto_converting_weapon_ult_mode = purgatory_auto_converting_weapon_ult_mode
        self.purgatory_weapon_ult_input = purgatory_weapon_ult_input
        self.purgatory_converting_option = purgatory_option_input  # 변경 될 리스트
        self.purgatory_converting_value = purgatory_value_input  # 변경 될 추가 값
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

    def prepare_calc(self):
        self.now_damage_array = self.basic_damage_arr.copy()
        self.now_leveling_array = self.basic_leveling_arr.copy()
        self.total_converting_value = [0, 0, 0, 0, 0, 0]
        self.total_converting_index = [0, 0, 0, 0, 0, 0]
        self.auto_converting_index = [9, 9, 9, 9, 9, 9]
        self.total_converting_index[0] = self.scent_option_input[0]
        self.total_converting_index[1] = self.scent_option_input[1]
        for i in range(4):
            self.total_converting_index[i+2] = self.purgatory_converting_option[i]
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

        for equipment in equipments + sets:
            try:  # 장비 옵션 조회
                damage_list.append(calculate.calculation.equipment_damage_option[equipment])
                leveling_list.append(calculate.calculation.equipment_leveling_option[equipment])
            except KeyError:
                print(equipment, "누락")

            now_purgatory = calculate.calculation.equipment_purgatory_option[equipment]  # 연옥 옵션 조회
            if now_purgatory[0] != 0:
                if len(equipment) == 6:  # 무기
                    if now_purgatory[0] == 106 and self.purgatory_converting_option != 0:  # 원초
                        self.purgatory_converted_value[0] = 0
                        self.purgatory_converting_value[0] = 0
                        self.now_damage_array[6] += 15
                    else:
                        now_index = 0
                        self.purgatory_converted_value[now_index] = now_purgatory[1]
                        if now_purgatory[0] == 27:
                            self.purgatory_converted_option[now_index] = 0
                        else:
                            self.purgatory_converted_option[now_index] = now_purgatory[0]
                        if self.purgatory_auto_converting_weapon_ult_mode == 1:  # 연옥 무기 태생유지
                            if now_purgatory[0] == 27:
                                self.purgatory_converted_value[now_index] = 0
                            else:
                                self.purgatory_converted_value[now_index] = 14
                        elif self.purgatory_auto_converting_weapon_ult_mode == 2:  # 연옥 무기 각성강제
                            if now_purgatory[0] == 27:
                                self.purgatory_converted_value[now_index] = 0
                            else:
                                self.purgatory_ult_value += 2
                                self.purgatory_converting_value[now_index] -= 14
                        else:  # 연옥 무기 각성해제
                            self.purgatory_converted_value[now_index] = 14
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
                self.total_converting_value[i+2] = \
                    self.purgatory_converted_value[i] + self.purgatory_converting_value[i]
                self.now_damage_array[self.purgatory_converting_option[i]] += self.total_converting_value[i+2]
                self.purgatory_converting_value[i] = 0
                self.purgatory_converted_value[i] = 0

        for index in simple_sum_index:
            self.now_damage_array[index] += sum([damage_list[x][index] for x in range(0, size)])
        for index in complex_sum_index:
            self.now_damage_array[index] = multiply_list([damage_list[x][index] for x in range(0, size)])
        self.now_damage_array[26] = anti_multiply_list([damage_list[x][26] for x in range(0, size)])
        for i in range(19):
            self.now_leveling_array[i] += sum([leveling_list[x][i] for x in range(0, size)])
        # log("self.now_damage_array", self.now_damage_array)
        # log("self.now_leveling_array", self.now_leveling_array)
        self.total_auto_converting_value.sort(reverse=True)
        # log("total_auto_converting_value", self.total_auto_converting_value)

    def calculate_damage(self):
        job_element = self.job_basic_element + sum([self.job_passive_element[i] * self.now_leveling_array[i]
                                                    for i in range(19)])
        self.now_damage_array[9] += job_element
        # log("total_element", total_element)

        self.now_damage_array[4] += (1.05 + 0.0045 * self.now_damage_array[9]) * self.now_damage_array[5]
        # log("total_additional_damage", total_additional_damage)

        if self.is_calc_detail:  # 정밀 계산 모드
            simple_sum_options = [self.now_damage_array[2], self.now_damage_array[3], self.now_damage_array[4],
                                  self.now_damage_array[6], self.now_damage_array[7], self.now_damage_array[8]]
            converting_index_arr = []
            for i in range(4):
                self.converting_value_arr[i+2] = self.purgatory_converting_value[i] + self.purgatory_converted_value[i]
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
                ((1 - cool_down_point) / 0.55) * ((1 - cool_down_point) / 0.55) * ((1 - cool_down_point) / 0.55) + 1)
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
        log("total_damage_groggy", total_damage_groggy)
        # log("total_damage_sustain", total_damage_sustain)
        # log("total_damage_ult", total_damage_ult)
        # log("total_damage_sum", total_damage_sum)
        log("now_damage_array", self.now_damage_array)

        return [total_damage_sum, total_damage_groggy, total_damage_sustain, total_damage_ult]


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
