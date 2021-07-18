import json
import multiprocessing as mp

total_database = None


class DataLoad:
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

    def __init__(self):
        manager = mp.Manager()
        return_list1 = manager.list()
        return_list2 = manager.list()
        return_list3 = manager.list()
        return_list4 = manager.list()
        mp1 = mp.Process(target=self.load_dealer_equipment_data, args=(return_list1,))
        mp2 = mp.Process(target=self.load_buffer_equipment_data, args=(return_list2,))
        mp3 = mp.Process(target=self.load_dealer_skill_data, args=(return_list3,))
        mp4 = mp.Process(target=self.load_buffer_skill_data, args=(return_list4,))
        mp1.start()
        mp2.start()
        mp3.start()
        mp4.start()
        mp1.join()
        mp2.join()
        mp3.join()
        mp4.join()

        self.equipment_code_by_name = return_list1[0]
        self.equipment_name_by_code = return_list1[1]
        self.equipment_set_by_code = return_list1[2]
        self.equipment_type_by_code = return_list1[3]
        self.equipment_damage_option = return_list1[4]
        self.equipment_leveling_option = return_list1[5]
        self.equipment_cool_down_option = return_list1[6]
        self.equipment_cool_recover_option = return_list1[7]
        self.equipment_purgatory_option = return_list1[8]

        self.equipment_buff_option = return_list2[0]
        self.equipment_buff_leveling_option = return_list2[1]
        self.equipment_buff_damage_leveling_option = return_list2[2]

        self.dealer_job_data = return_list3[0]

        self.buff_skill_data = return_list4[0]

        global total_database
        total_database = [self.equipment_code_by_name, self.equipment_name_by_code, self.equipment_set_by_code,
                          self.equipment_type_by_code, self.equipment_damage_option, self.equipment_leveling_option,
                          self.equipment_cool_down_option, self.equipment_cool_recover_option,
                          self.equipment_purgatory_option,
                          self.equipment_buff_option, self.equipment_buff_leveling_option,
                          self.equipment_buff_damage_leveling_option,
                          self.dealer_job_data, self.buff_skill_data]

    def load_dealer_equipment_data(self, return_list):
        json_data = self.load_json('./data/dealer_opt_list.json')
        equipment_code_by_name = {}
        equipment_name_by_code = {}
        equipment_set_by_code = {}
        equipment_type_by_code = {}
        equipment_damage_option = {}
        equipment_leveling_option = {}
        equipment_cool_down_option = {}
        equipment_cool_recover_option = {}
        equipment_purgatory_option = {}
        for item_code, item_value in json_data.items():
            now_damage_arr = []
            # 색적 데이터
            item_name = item_value["_itemName"]  # 아이템 이름/코드
            if item_name is not None and len(item_code) != 9:
                equipment_code_by_name[item_code] = item_name  # equipment_code_by_name
                equipment_name_by_code[item_name] = item_code  # equipment_name_by_code
            set_name = item_value["_setName"]  # 아이템 세트명
            if set_name is not None:
                equipment_set_by_code[item_code] = set_name  # equipment_set_by_code
            type_name = item_value["_typeName"]  # 아이템 타입
            if type_name is not None:
                equipment_type_by_code[item_code] = type_name  # equipment_type_by_code

            now_damage_option = item_value["damageOptions"]  # 데미지 옵션
            now_cool_down_option = item_value["cooltimeOptions"]  # 쿨타임 감소 옵션
            now_level_option = item_value["levelingOptions"]  # 레벨링 옵션
            now_ult_option = item_value["ultSkillOptions"]  # 각성기 스증 옵션

            now_damage_arr.append(now_damage_option['upBonusStat'])
            now_damage_arr.append(now_damage_option['upBonusAttackPoint'])
            now_damage_arr.append(now_damage_option['upIncreaseDamage'])
            now_damage_arr.append(now_damage_option['upCriticalDamage'])
            now_damage_arr.append(now_damage_option['upAdditionalDamage'])
            now_damage_arr.append(now_damage_option['upAdditionalElementalDamage'])
            now_damage_arr.append(now_damage_option['upAllDamage'])
            now_damage_arr.append(now_damage_option['upPercentAttackPoint'])
            now_damage_arr.append(now_damage_option['upPercentStat'])
            now_damage_arr.append(now_damage_option['upElementalReinforce'])
            now_damage_arr.append(now_damage_option['upContinuousDamage'])
            now_damage_arr.append(now_damage_option['upSkillDamage'])
            now_damage_arr.append(now_damage_option['upSpecialDamage'])
            now_damage_arr.append(now_damage_option['upSpeedRate'])
            now_damage_arr.append(now_damage_option['upCriticalRate'])
            active_leveling = now_level_option['activeLeveling']
            for i in range(0, 6):
                now_damage_arr.append(active_leveling[i])
            passive_leveling = now_level_option['passiveLeveling']
            for i in range(0, 4):
                now_damage_arr.append(passive_leveling[i])
            now_damage_arr.append(now_level_option['specialLeveling'])
            now_damage_arr.append(now_cool_down_option['coolDownNeo'])
            now_damage_arr.append(now_cool_down_option['coolDownOrigin'])
            for i in range(0, 3):
                now_damage_arr.append(now_ult_option[i])
            # 연옥 변환 옵션
            now_purgatory_option = item_value["_purgatory"]
            if now_purgatory_option[0] is not None:
                equipment_purgatory_option[item_code] = [now_purgatory_option[0], now_purgatory_option[1]]
                # equipment_purgatory_option

            equipment_damage_option[item_code] = now_damage_arr  # equipment_damage_option

            detail_leveling = now_level_option['detailLeveling']
            equipment_leveling_option[item_code] = detail_leveling  # equipment_leveling_option
            detail_cool_down = now_cool_down_option['coolDownDetail']
            equipment_cool_down_option[item_code] = detail_cool_down  # equipment_cool_down_option
            detail_cool_recover = now_cool_down_option['coolRecoverDetail']
            equipment_cool_recover_option[item_code] = detail_cool_recover  # equipment_cool_recover_option

        return_list.append(equipment_code_by_name)
        return_list.append(equipment_name_by_code)
        return_list.append(equipment_set_by_code)
        return_list.append(equipment_type_by_code)
        return_list.append(equipment_damage_option)
        return_list.append(equipment_leveling_option)
        return_list.append(equipment_cool_down_option)
        return_list.append(equipment_cool_recover_option)
        return_list.append(equipment_purgatory_option)

    def load_buffer_equipment_data(self, return_list):
        json_data = self.load_json('./data/buffer_opt_list.json')
        equipment_buff_option = {}
        equipment_buff_leveling_option = {}
        equipment_buff_damage_leveling_option = {}
        for item_code, item_value in json_data.items():
            now_buff_arr = []
            now_level_arr = []

            now_stat_option = item_value['statOptions']  # 스탯
            now_casting_option = item_value['castingOptions']  # 버프 스킬
            now_passive_option = item_value['passiveOptions']  # 패시브 스킬
            now_other_option = item_value['otherOptions']  # 기타
            now_detail_level_option = item_value['allLeveling']  # 상세 레벨링

            now_buff_arr.append(now_stat_option['upSpiritStat'])
            now_buff_arr.append(now_stat_option['upIntelligenceStat'])
            now_buff_arr.append(now_casting_option['upPercentBlessStat'])
            now_buff_arr.append(now_casting_option['upPercentBlessPhysicalAtk'])
            now_buff_arr.append(now_casting_option['upPercentBlessMagicalAtk'])
            now_buff_arr.append(now_casting_option['upPercentBlessIndependentAtk'])
            now_buff_arr.append(now_casting_option['upPointCruxStat'])
            now_buff_arr.append(now_casting_option['upPercentCruxStat'])
            now_buff_arr.append(now_passive_option['upPointSaintFirstAwakeningPassive'])
            now_buff_arr.append(now_passive_option['upPointSeraphimFirstAwakeningPassive'])
            now_buff_arr.append(now_other_option['coolDownAria'])
            now_buff_arr.append(now_other_option['coolDownHavesting'])
            now_buff_arr.append(now_other_option['specialDamageIncrease'])

            now_level_arr.append(now_casting_option['upBlessLeveling'])
            now_level_arr.append(now_casting_option['upCruxLeveling'])
            now_level_arr.append(now_casting_option['upNeoUltSkillLeveling'])
            now_level_arr.append(now_passive_option['upAdvancementPassiveLeveling'])
            now_level_arr.append(now_passive_option['upProtectionSignLeveling'])
            now_level_arr.append(now_passive_option['upFirstAwakeningPassiveLeveling'])
            now_level_arr.append(now_passive_option['upSecondAwakeningPassiveLeveling'])
            now_level_arr.append(now_passive_option['upSecondUltSkillLeveling'])
            now_level_arr.append(now_passive_option['upNeoAwakeningPassiveLeveling'])
            now_level_arr.append(now_passive_option['upGrandCrossCrashLeveling'])

            equipment_buff_option[item_code] = now_buff_arr
            equipment_buff_leveling_option[item_code] = now_level_arr
            equipment_buff_damage_leveling_option[item_code] = now_detail_level_option

        return_list.append(equipment_buff_option)
        return_list.append(equipment_buff_leveling_option)
        return_list.append(equipment_buff_damage_leveling_option)

    def load_dealer_skill_data(self, return_list):
        json_data = self.load_json('./data/dealer_leveling_list.json')
        job_data = {}
        for item_code, item_value in json_data.items():
            now_total_job_data = {}

            now_active = item_value['active']  # 액티브 레벨링
            now_active_arr = [now_active['etc'] / 2, now_active['lv50'], now_active['etc'] / 2,
                              now_active['lv85'], now_active['lv95'], now_active['lv100']]
            now_total_job_data['nowJobActiveLevelingArray'] = now_active_arr

            now_element_option = item_value['elementalReinforce']  # 자속강
            now_element_basic = now_element_option['basicSkillElementalReinforce']
            now_element_leveling = now_element_option['lvSkillElementalReinforce']
            now_total_job_data['nowBasicSkillElementalReinforce'] = now_element_basic
            now_total_job_data['nowLvSkillElementalReinforce'] = now_element_leveling

            now_passive = item_value['passive']  # 패시브
            now_total_job_data['nowJobPassiveLeveling'] = now_passive

            now_weapon = item_value['weaponCorrection']  # 무기 보정
            now_weapon_atk = now_weapon['weaponAtkRate']
            now_weapon_cool = now_weapon['weaponCoolTimeRate']
            now_total_job_data['nowJobWeaponAtkRate'] = now_weapon_atk
            now_total_job_data['nowJobWeaponCoolRate'] = now_weapon_cool

            job_data[item_code] = now_total_job_data

        return_list.append(job_data)

    def load_buffer_skill_data(self, return_list):
        json_data = self.load_json('./data/buffer_leveling_list.json')
        skill_data = {}
        for item_code, item_value in json_data.items():
            skill_data[item_code] = item_value
        return_list.append(skill_data)

    def load_json(self, file_name):
        with open(file_name, "r", encoding='UTF8') as json_file:
            json_data = json.load(json_file)
        return json_data
