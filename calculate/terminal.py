import calculate.fullset
import calculate.calculation
import calculate.set
import os
import multiprocessing as mp
from datetime import datetime

import data.dataload
import data.basic_arr


def divide_case(equipment_list, core_num):
    divide_list = []
    for i in range(0, core_num):
        temp_list = [equipment_list[x] for x in range(len(equipment_list)) if x % core_num == i]
        if temp_list == [[]] or temp_list == []:
            continue
        divide_list.append(temp_list)
    return divide_list


class Terminal:

    def __init__(self, dropdown_list, select_weapon_list, equipment_toggle):
        self.start_time = datetime.now()
        self.dropdown_list = dropdown_list
        self.select_weapon_list = select_weapon_list
        self.equipment_toggle = equipment_toggle

        self.values = {}  # 설정값 저장
        self.equipment_list = {
            '11': [], '12': [], '13': [], '14': [], '15': [], '21': [], '22': [], '23': [], '31': [], '32': [],
            '33': [],
            '11_0': [], '11_1': [], '21_0': [], '21_1': [], '33_0': [], '33_1': [],
            '41': [], '42': [], '43': [], '51': [], '52': [], '53': [], '54': [], '55': []
        }
        self.set_list = {}
        self.fusion_cases = []
        self.select_weapon_list_code = []

        self.basic_damage_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.basic_leveling_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.scent_option_input = []
        self.scent_value_input = []
        self.is_scent2_on = False
        self.purgatory_option_input = []
        self.purgatory_value_input = []
        self.purgatory_weapon_ult_input = False
        self.purgatory_auto_converting_weapon_ult_mode = 1

        self.get_equipment_values()
        self.make_fusion_cases()
        self.get_setting_values()
        self.core_num = os.cpu_count() - 1
        if self.core_num >= 8:
            self.core_num = 8
        elif self.core_num < 1:
            self.core_num = 1
        print("최대 가용 코어 개수 = " + str(self.core_num))
        self.case_terminal()

    def get_equipment_values(self):
        # 무기
        self.select_weapon_list_code = []
        for now_weapon in self.select_weapon_list:
            try:
                self.select_weapon_list_code.append(data.dataload.total_database[1][now_weapon])
            except KeyError:
                pass

        for i in range(1, 36):
            self.set_list[i] = [0, 0, 0, 0, 0, 0]

        for key, value in self.equipment_toggle.items():
            if not value or value is False:
                continue
            if len(key) == 5:
                part = key[0:2]
                if part == '11' or part == '21' or part == '33':
                    myth = key[-1]
                    self.equipment_list[part + '_' + myth].append(key)
                self.equipment_list[part].append(key)

                set_code = int(key[2:4])
                if self.set_list.get(set_code) is not None:
                    if key[-1] == '1':
                        self.set_list.get(set_code)[-1] = 1
                    else:
                        if 1 <= set_code <= 23:
                            self.set_list.get(set_code)[int(key[1]) - 1] = 1
                        else:
                            self.set_list.get(set_code)[int(key[0]) - 1] = 1
        # 풀셋이 존재한다면 단품은 제거
        # 방어구 악세 특장 하팔법 상목보 신반귀
        remove_list = [False, False, False, False, False, False]
        set_num = {}
        set_num_myth = {}
        for i in range(1, 36):
            if i < 16:
                set_sum = sum([self.set_list[i][j] for j in [0, 1, 2, 3, 4]])
                set_sum_myth = sum([self.set_list[i][j] for j in [5, 1, 2, 3, 4]])
                if set_sum == 5 or set_sum_myth == 5:
                    remove_list[0] = True
            else:
                set_sum = sum([self.set_list[i][j] for j in [0, 1, 2]])
                set_sum_myth = sum([self.set_list[i][j] for j in [5, 1, 2]])
                if set_sum == 3 or set_sum_myth == 3:
                    if 16 <= i <= 19:
                        index = 1
                    elif 20 <= i <= 23:
                        index = 2
                    elif 24 <= i <= 27:
                        index = 3
                    elif 28 <= i <= 31:
                        index = 4
                    else:
                        index = 5
                    remove_list[index] = True
            set_num[i] = set_sum
            set_num_myth[i] = set_sum_myth
        for i in range(1, 36):
            if i <= 15:
                index = 0
            elif 16 <= i <= 19:
                index = 1
            elif 20 <= i <= 23:
                index = 2
            elif 24 <= i <= 27:
                index = 3
            elif 28 <= i <= 31:
                index = 4
            else:
                index = 5
            if remove_list[index] is False:
                continue
            if set_num[i] <= 1 and set_num_myth[i] <= 1:
                for key, value_list in self.equipment_list.items():
                    if len(value_list) == 0:
                        continue
                    for now_code in value_list.copy():
                        if len(now_code) != 5:
                            continue
                        if now_code[2:4] == str(i + 100)[1:] and now_code[-1] != '1':
                            value_list.remove(now_code)

    def make_fusion_cases(self):
        self.is_scent2_on = True
        sirocco_case = self.equipment_list["41"]
        if len(sirocco_case) == 0:
            self.is_scent2_on = False
            sirocco_case.append("41500")
        ozma_case = self.equipment_list["55"]
        if len(ozma_case) == 0:
            ozma_case.append("55610")
        for sirocco in sirocco_case:
            for ozma in ozma_case:
                self.fusion_cases.append([sirocco, ozma])

    def get_setting_values(self):
        for key, value in self.dropdown_list.items():
            self.values[key] = value.get()

        basic_arr_class = data.basic_arr.BasicArr(self.values, self.is_scent2_on)

        basic_arrays = basic_arr_class.get_basic_arr_input()
        self.basic_damage_arr = basic_arrays[0]
        self.basic_leveling_arr = basic_arrays[1]

        scent_input = basic_arr_class.get_scent_input()
        self.scent_option_input = scent_input[0]
        self.scent_value_input = scent_input[1]

        purgatory_inputs = basic_arr_class.get_purgatory_input()
        self.purgatory_option_input = purgatory_inputs[0]
        self.purgatory_value_input = purgatory_inputs[1]
        self.purgatory_weapon_ult_input = purgatory_inputs[2]
        self.purgatory_auto_converting_weapon_ult_mode = purgatory_inputs[3]

        scent_mode = self.dropdown_list["scent_mode"].get()
        if scent_mode == "선택부여":
            now_scent1_option = self.dropdown_list["scent1_option"].get()
            if self.is_scent2_on is True:
                now_scent2_option = self.dropdown_list["scent2_option"].get()

    def case_terminal(self):
        # 풀셋모드
        # > 신화 풀셋 존재? 끝
        # > 에픽 풀셋 존재? 신화 포함 스까세팅만 계산
        # > 없음? All 모드

        full_set_list = calculate.fullset.make_full_set_case(self.set_list)
        full_set_list_normal = full_set_list[0]
        full_set_list_myth = full_set_list[1]

        if len(full_set_list_myth) != 0:
            now_all_case = full_set_list_normal + full_set_list_myth
            print(len(now_all_case)*len(self.select_weapon_list_code), "가지 계산 시작")
            self.calculate_damage(divide_case(now_all_case, self.core_num))
            pass
        elif len(full_set_list_normal) != 0:
            now_all_case = full_set_list_normal + calculate.set.make_case(self.equipment_list, 1)
            print(len(now_all_case)*len(self.select_weapon_list_code), "가지 계산 시작")
            self.calculate_damage(divide_case(now_all_case, self.core_num))
        else:
            now_all_case = calculate.set.make_case(self.equipment_list, 0)
            print(len(now_all_case)*len(self.select_weapon_list_code), "가지 계산 시작")
            self.calculate_damage(divide_case(now_all_case, self.core_num))

        date_diff = datetime.now() - self.start_time
        print("소모시간 = ", date_diff.seconds, "초")

    def calculate_damage(self, cases_list):
        manager = mp.Manager()
        mp_list = []
        result_list = []
        # test
        for i in range(len(cases_list)):
            result_list.append(manager.list())
            mp_list.append(
                mp.Process(
                    target=calculate.calculation.Calculation,
                    args=(
                        result_list[i], self.values["job"], data.dataload.total_database, cases_list[i],
                        self.select_weapon_list_code, self.fusion_cases,
                        self.basic_damage_arr, self.basic_leveling_arr,
                        self.is_scent2_on, self.scent_option_input,
                        self.purgatory_option_input, self.purgatory_value_input, self.purgatory_weapon_ult_input,
                        self.purgatory_auto_converting_weapon_ult_mode
                    )
                )
            )
        for now_mp in mp_list:
            now_mp.start()

        result_values_sum = [[], [], [], []]
        result_equipments_sum = [[], [], [], []]
        for i in range(len(mp_list)):
            mp_list[i].join()
            if result_list[i] is not None:
                for j in range(0, 4):
                    try:
                        result_values_sum[j] += result_list[i][0][j]
                        result_equipments_sum[j] += result_list[i][1][j]
                    except IndexError:
                        pass
        # print(result_values_sum[0])
        # print(result_equipments_sum[0])

        # print(max(result_values_sum[1]))
        # print(result_equipments_sum[1][result_values_sum[1].index(max(result_values_sum[1]))])










