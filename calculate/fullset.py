import itertools

# 일반 풀셋이 있어도 스까 가능 방어구 정리
# 역작
# able_mix_armor = [11]
able_mix_armor = [11]


def make_full_set_case(set_list):
    all_case = []
    all_case_myth_armor = []
    all_case_myth_acc = []
    all_case_myth_spe = []

    armor_case = []
    armor_case_myth = []
    accessory_case = []
    accessory_case_myth = []
    special_case = []
    special_case_myth = []

    # 방어구 5셋
    already_full_armor = []
    already_full_armor_myth = []
    for i in range(1, 16):
        now_index = set_list.get(i)
        set_num_temp = sum(now_index[x] for x in [1, 2, 3, 4])
        set_num = set_num_temp + now_index[0]
        set_num_myth = set_num_temp + now_index[-1]
        if set_num == 5:
            armor_case.append([i, i, i, i, i])
            already_full_armor.append(i)
        if set_num_myth == 5:
            armor_case_myth.append([i, i, i, i, i])
            already_full_armor_myth.append(i)

    # 방어구 3+2셋
    able_32_case = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    for case in able_32_case:
        not_case = [0, 1, 2, 3, 4, 5]
        not_case.remove(case[0])
        not_case.remove(case[1])
        if case.count(0) == 1:
            case.append(5)
            not_case.remove(5)
        for i in range(1, 16):
            for j in range(1, 16):
                if i == j:
                    continue
                now_index = [0, 0, 0, 0, 0, 0]
                for k in range(0, 6):
                    now_index[k] = i * case.count(k) * set_list[i][k] + j * not_case.count(k) * set_list[j][k]
                final_index = [now_index[x] for x in [0, 1, 2, 3, 4]]
                final_index_myth = [now_index[x] for x in [5, 1, 2, 3, 4]]
                if final_index.count(0) == 0 and (
                        (already_full_armor.count(i) + already_full_armor.count(j) == 0) or (
                        able_mix_armor.count(i) + able_mix_armor.count(j) != 0)):
                    armor_case.append(final_index)
                if final_index_myth.count(0) == 0 and (
                        (already_full_armor_myth.count(i) + already_full_armor_myth.count(j) == 0) or (
                        able_mix_armor.count(i) + able_mix_armor.count(j) != 0)):
                    armor_case_myth.append(final_index_myth)

    # 악세 3셋
    for i in range(16, 20):
        now_index = set_list.get(i)
        set_num = sum(now_index[x] for x in [0, 1, 2])
        set_num_myth = sum(now_index[x] for x in [5, 1, 2])
        if set_num == 3:
            accessory_case.append([i, i, i])
        if set_num_myth == 3:
            accessory_case_myth.append([i, i, i])

    # 특장 3셋
    for i in range(20, 24):
        now_index = set_list.get(i)
        set_num = sum(now_index[x] for x in [0, 1, 2])
        set_num_myth = sum(now_index[x] for x in [0, 1, 5])
        if set_num == 3:
            special_case.append([i, i, i])
        if set_num_myth == 3:
            special_case_myth.append([i, i, i])

    # 533 세팅 합
    for now_armor in armor_case:
        for now_acc in accessory_case:
            for now_spe in special_case:
                all_case.append(now_armor + now_acc + now_spe)
            for now_spe in special_case_myth:
                all_case_myth_spe.append(now_armor + now_acc + now_spe)
        for now_acc in accessory_case_myth:
            for now_spe in special_case:
                all_case_myth_acc.append(now_armor + now_acc + now_spe)
    for now_armor in armor_case_myth:
        for now_acc in accessory_case:
            for now_spe in special_case:
                all_case_myth_armor.append(now_armor + now_acc + now_spe)

    # 3332
    for i in [28, 29, 30, 31]:
        for j in [24, 25, 26, 27]:
            for k in [32, 33, 34, 35]:
                for l in range(1, 16):
                    now_cases = []
                    now_cases_myth_armor = []
                    now_cases_myth_acc = []
                    now_cases_myth_spe = []
                    # 껍질
                    temp_case = [
                        i * set_list[i][0], j * set_list[j][0], l * set_list[l][2],
                        l * set_list[l][3], k * set_list[k][0],
                        j * set_list[j][1], i * set_list[i][1], k * set_list[k][1],
                        i * set_list[i][2], j * set_list[j][2], k * set_list[k][2]]
                    # 표준 3332
                    case1 = temp_case.copy()
                    now_cases.append(case1)
                    # 신화 변형
                    for myth in [0, 5, 10]:
                        case1_myth = case1.copy()
                        change_value = 0
                        if myth == 0:
                            change_value = i * set_list[i][5]
                        elif myth == 5:
                            change_value = j * set_list[j][5]
                        elif myth == 10:
                            change_value = k * set_list[k][5]
                        case1_myth[myth] = change_value
                        if myth == 0:
                            now_cases_myth_armor.append(case1_myth)
                        elif myth == 5:
                            now_cases_myth_acc.append(case1_myth)
                        elif myth == 10:
                            now_cases_myth_spe.append(case1_myth)

                    # 변형 3332
                    for change in [0, 1, 4]:
                        change_case = temp_case.copy()
                        change_case[change] = l * set_list[l][change]
                        now_cases.append(change_case)
                        for myth in [0, 5, 10]:
                            change_case_myth = change_case.copy()
                            change_value = 0
                            if myth == 0:
                                if change == 0:
                                    change_value = l * set_list[l][5]
                                else:
                                    change_value = i * set_list[i][5]
                            elif myth == 5:
                                change_value = j * set_list[j][5]
                            elif myth == 10:
                                change_value = k * set_list[k][5]
                            change_case_myth[myth] = change_value
                            if myth == 0:
                                now_cases_myth_armor.append(change_case_myth)
                            elif myth == 5:
                                now_cases_myth_acc.append(change_case_myth)
                            elif myth == 10:
                                now_cases_myth_spe.append(change_case_myth)

                    for now_case in now_cases:
                        if now_case.count(0) == 0:
                            all_case.append(now_case)
                    for now_case in now_cases_myth_armor:
                        if now_case.count(0) == 0:
                            all_case_myth_armor.append(now_case)
                    for now_case in now_cases_myth_acc:
                        if now_case.count(0) == 0:
                            all_case_myth_acc.append(now_case)
                    for now_case in now_cases_myth_spe:
                        if now_case.count(0) == 0:
                            all_case_myth_spe.append(now_case)

    final_all_case = []
    final_all_case_myth = []

    index_part_code = ['11', '12', '13', '14', '15', '21', '22', '23', '31', '32', '33']
    for index, now_all_cases in enumerate([all_case, all_case_myth_armor, all_case_myth_acc, all_case_myth_spe]):
        myth_index = 99
        if index == 1:
            myth_index = 0
        elif index == 2:
            myth_index = 5
        elif index == 3:
            myth_index = 10
        for now_case in now_all_cases:
            convert_case = []
            for now_index, now_part in enumerate(now_case):
                myth_code = '0'
                if myth_index == now_index:
                    myth_code = '1'
                convert_case.append(index_part_code[now_index] + str(now_part+100)[1:] + myth_code)
            if index == 0:
                final_all_case.append(convert_case)
            else:
                final_all_case_myth.append(convert_case)

    return final_all_case, final_all_case_myth




