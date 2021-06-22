import data.damage_data


class BasicArr:

    def __init__(self, value_dict, is_scent2_on):
        self.basic_damage_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.basic_leveling_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.scent_option_input = [0, 0]
        self.scent_value_input = [0, 0]
        self.purgatory_option_input = [0, 0, 0, 0]
        self.purgatory_value_input = [0, 0, 0, 0]
        self.purgatory_weapon_ult_input = False
        self.purgatory_auto_converting_weapon_ult_mode = 1  # 1: 태생유지, 2: 각성강제, 3: 각성해제
        self.value_dict = value_dict
        self.is_scent2_on = is_scent2_on
        self.set_title_value()
        self.set_creature_value()
        self.set_scent_value()
        self.set_purgatory_value()

    def get_basic_arr_input(self):
        return [self.basic_damage_arr, self.basic_leveling_arr]

    def set_title_value(self):
        title = self.value_dict["title"]
        title_opt_arr = data.damage_data.title[title]
        self.basic_damage_arr[title_opt_arr[0]] += title_opt_arr[1]

    def set_creature_value(self):
        creature = self.value_dict["creature"]
        creature_opt_arr = data.damage_data.creature[creature]
        self.basic_damage_arr[creature_opt_arr[0]] += creature_opt_arr[1]
        if creature == "크증18%" or creature == "물마독공18%":
            self.basic_leveling_arr[14] += 1
        if creature == "크증18%" and self.value_dict["title"] == "크증10%":
            self.basic_damage_arr[3] -= 10

    def get_scent_input(self):
        return [self.scent_option_input, self.scent_value_input]

    def set_scent_value(self):
        scent_mode = self.value_dict["scent_mode"]
        if scent_mode == "최적부여":
            self.scent_option_input = [9, 9]
            if self.is_scent2_on is False:
                self.scent_option_input[1] = 0
            return
        elif scent_mode == "미부여":
            return
        scent1_option = self.value_dict["scent1_option"]
        scent1_value = self.value_dict["scent1_value"]
        if scent1_value == "상(노랑)":
            self.scent_value_input[0] = 10
        elif scent1_value == "중(보라)":
            self.scent_value_input[0] = 8
        else:
            self.scent_value_input[0] = 6
        self.scent_option_input[0] = data.damage_data.damage_string_index[scent1_option[0:2]]
        self.basic_damage_arr[self.scent_option_input[0]] += self.scent_value_input[0]
        if self.is_scent2_on is True:
            scent2_option = self.value_dict["scent2_option"]
            scent2_value = self.value_dict["scent2_value"]
            if scent2_value == "상(노랑)":
                self.scent_value_input[1] = 5
            elif scent2_value == "중(보라)":
                self.scent_value_input[1] = 4
            else:
                self.scent_value_input[1] = 3
            self.scent_option_input[1] = data.damage_data.damage_string_index[scent2_option[0:2]]
            self.basic_damage_arr[self.scent_option_input[1]] += self.scent_value_input[1]

    def get_purgatory_input(self):
        return [self.purgatory_option_input, self.purgatory_value_input, self.purgatory_weapon_ult_input,
                self.purgatory_auto_converting_weapon_ult_mode]

    def set_purgatory_value(self):
        purgatory_auto_ult_option = self.value_dict["purgatory_ult_mode"]
        if purgatory_auto_ult_option == "각성강제":
            self.purgatory_auto_converting_weapon_ult_mode = 2
        elif purgatory_auto_ult_option == "각성해제":
            self.purgatory_auto_converting_weapon_ult_mode = 3
        else:
            self.purgatory_auto_converting_weapon_ult_mode = 1
        for i in range(1, 5):
            now_purgatory_option = self.value_dict["purgatory{}_option".format(i)]
            now_purgatory_value = self.value_dict["purgatory{}_value".format(i)]
            if now_purgatory_option == "미변환":
                self.purgatory_option_input[i-1] = 0
                self.purgatory_value_input[i-1] = 0
            elif now_purgatory_option == "최적변환":
                self.purgatory_option_input[i-1] = 9
                if i == 1:
                    self.purgatory_value_input[i-1] = 16
                else:
                    self.purgatory_value_input[i-1] = 8
            else:
                self.purgatory_option_input[i-1] = data.damage_data.damage_string_index[now_purgatory_option[0:2]]
                if i == 1 and "각성+2" in now_purgatory_option:
                    self.purgatory_weapon_ult_input = True
                self.purgatory_value_input[i-1] = int(now_purgatory_value[1:])












