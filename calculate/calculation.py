import calculate.damage

equipment_code_by_name = {}
equipment_name_by_code = {}
equipment_set_by_code = {}
equipment_type_by_code = {}
equipment_damage_option = {}
equipment_leveling_option = {}
equipment_cool_down_option = {}
equipment_cool_recover_option = {}
equipment_purgatory_option = {}
equipment_buff_option = {}
equipment_buff_leveling_option = {}
equipment_buff_damage_leveling_option = {}
dealer_job_data = {}
buff_skill_data = {}


def get_database(total_database):
    global equipment_code_by_name, equipment_name_by_code, equipment_set_by_code, equipment_type_by_code
    global equipment_damage_option, equipment_leveling_option, equipment_cool_down_option
    global equipment_cool_recover_option, equipment_purgatory_option, equipment_buff_option
    global equipment_buff_leveling_option, equipment_buff_damage_leveling_option
    global dealer_job_data, buff_skill_data
    equipment_code_by_name = total_database[0]
    equipment_name_by_code = total_database[1]
    equipment_set_by_code = total_database[2]
    equipment_type_by_code = total_database[3]
    equipment_damage_option = total_database[4]
    equipment_leveling_option = total_database[5]
    equipment_cool_down_option = total_database[6]
    equipment_cool_recover_option = total_database[7]
    equipment_purgatory_option = total_database[8]
    equipment_buff_option = total_database[9]
    equipment_buff_leveling_option = total_database[10]
    equipment_buff_damage_leveling_option = total_database[11]
    dealer_job_data = total_database[12]
    buff_skill_data = total_database[13]


class Calculation:

    def __init__(self, return_list, job, total_database, equipment_cases,
                 weapon_cases, fusion_cases,
                 basic_damage_arr, basic_leveling_arr,
                 is_scent2_on, scent_option_input,
                 purgatory_option_input, purgatory_value_input, purgatory_weapon_ult_input,
                 purgatory_auto_converting_weapon_ult_mode):

        is_buffer = False
        # sum, groggy, sustain, ult
        min_value = [0 for i in range(4)]
        result_value_saved = [[0 for i in range(20)], [0 for i in range(20)],
                              [0 for i in range(20)], [0 for i in range(20)]]
        result_equipment_saved = [[0 for i in range(20)], [0 for i in range(20)],
                                  [0 for i in range(20)], [0 for i in range(20)]]

        if len(equipment_cases) * len(weapon_cases) == 0:
            return
        get_database(total_database)
        if len(job) > 5 and job[0:4] == "(버퍼)":
            is_buffer = True
        if is_buffer is False:  # 딜러
            damage_class = calculate.damage.Damage(
                job, basic_damage_arr, basic_leveling_arr, False,
                is_scent2_on, scent_option_input,
                purgatory_option_input, purgatory_value_input, purgatory_weapon_ult_input,
                purgatory_auto_converting_weapon_ult_mode
            )
            for fusion in fusion_cases:
                for weapon in weapon_cases:
                    for case in equipment_cases:
                        damage_class.combine_damage_option(case + [weapon] + fusion)
                        now_result = damage_class.calculate_damage()
                        # print(now_result)
                        for i in range(4):
                            if min_value[i] < now_result[i]:
                                removing_index = result_value_saved[i].index(min_value[i])
                                result_value_saved[i][removing_index] = now_result[i]
                                result_equipment_saved[i][removing_index] = case + [weapon] + fusion
                                min_value[i] = min(result_value_saved[i])
            for i in range(4):
                while result_value_saved[i].__contains__(0):
                    result_value_saved[i].remove(0)
                    result_equipment_saved[i].remove(0)

            # 정밀 재계산
            detail_result_value_saved = [[], [], [], []]
            detail_result_equipment_saved = [[], [], [], []]
            detail_result_tran_saved = [[], [], [], []]

            damage_class_detail = calculate.damage.Damage(
                job, basic_damage_arr, basic_leveling_arr, True,
                is_scent2_on, scent_option_input,
                purgatory_option_input, purgatory_value_input, purgatory_weapon_ult_input,
                purgatory_auto_converting_weapon_ult_mode
            )
            for i in range(4):
                damage_class_detail.get_detail_code(i)
                for now_case in result_equipment_saved[i]:
                    damage_class_detail.combine_damage_option(now_case)
                    now_result_detail = damage_class_detail.calculate_damage()
                    detail_result_value_saved[i].append(now_result_detail[i])
                    detail_result_equipment_saved[i].append(now_case)
                    if len(now_result_detail) == 5:
                        detail_result_tran_saved[i].append(now_result_detail[4])
                    else:
                        detail_result_tran_saved[i].append([0])

            return_list.append(detail_result_value_saved)
            return_list.append(detail_result_equipment_saved)
            return_list.append(detail_result_tran_saved)

        else:
            pass




