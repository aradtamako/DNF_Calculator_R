import itertools


def remove_single(equipment_list, set_list):
    pass


def make_case(equipment_list, myth_mode):
    combined_list_normal = [
        equipment_list['11_0'], equipment_list['12'], equipment_list['13'], equipment_list['14'],
        equipment_list['15'],
        equipment_list['21_0'], equipment_list['22'], equipment_list['23'],
        equipment_list['31'], equipment_list['32'], equipment_list['33_0']
    ]

    combined_list_myth1 = [
        equipment_list['11_1'], equipment_list['12'], equipment_list['13'], equipment_list['14'],
        equipment_list['15'],
        equipment_list['21_0'], equipment_list['22'], equipment_list['23'],
        equipment_list['31'], equipment_list['32'], equipment_list['33_0']
    ]
    combined_list_myth2 = [
        equipment_list['11_0'], equipment_list['12'], equipment_list['13'], equipment_list['14'],
        equipment_list['15'],
        equipment_list['21_1'], equipment_list['22'], equipment_list['23'],
        equipment_list['31'], equipment_list['32'], equipment_list['33_0']
    ]

    combined_list_myth3 = [
        equipment_list['11_0'], equipment_list['12'], equipment_list['13'], equipment_list['14'],
        equipment_list['15'],
        equipment_list['21_0'], equipment_list['22'], equipment_list['23'],
        equipment_list['31'], equipment_list['32'], equipment_list['33_1']
    ]

    total_list = []
    total_list_myth = []

    if myth_mode != 2:
        if myth_mode == 0:  # 일반
            now_cases = list(itertools.product(*combined_list_normal))
            if len(now_cases) != 0:
                total_list += now_cases
        for now_combined_list in [combined_list_myth1, combined_list_myth2, combined_list_myth3]:
            try:
                now_cases = list(itertools.product(*now_combined_list))
                if len(now_cases) == 0:
                    continue
                total_list_myth += now_cases
            except TypeError:
                pass
    else:  # 에픽모드(에픽만)
        now_cases = list(itertools.product(*combined_list_normal))
        if len(now_cases) != 0:
            total_list += now_cases

    return total_list + total_list_myth
