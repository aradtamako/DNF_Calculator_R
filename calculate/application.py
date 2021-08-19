import data.dataload


class Application:
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
    def __init__(self, value_dict):
        self.value_dict = value_dict
        self.apply_dealer_custom()

    def apply_dealer_custom(self):
        equipment_damage_option = data.dataload.total_database[4]

        # 먼동
        sunset_reinforce = self.value_dict.get('sunset_reinforce')
        try:
            sunset_reinforce = int(sunset_reinforce)
        except:
            sunset_reinforce = 10
        equipment_damage_option['21170'][11] = sunset_reinforce + 5
        equipment_damage_option['21171'][11] = sunset_reinforce + 5
        equipment_damage_option['22170'][8] = sunset_reinforce + 5
        equipment_damage_option['23170'][2] = sunset_reinforce + 5

        # 대자연 속강
        element_type = self.value_dict.get('element_type')
        if element_type == "모속":
            equipment_damage_option['41540'][9] = 90
            equipment_damage_option['12150'][9] = 6
            equipment_damage_option['13150'][9] = 6
            equipment_damage_option['14150'][9] = 6
            equipment_damage_option['15150'][9] = 6
        else:
            equipment_damage_option['41540'][9] = 67
            if element_type == '수':
                equipment_damage_option['12150'][9] = 0
                equipment_damage_option['13150'][9] = 0
                equipment_damage_option['14150'][9] = 24
                equipment_damage_option['15150'][9] = 0
            elif element_type == '명':
                equipment_damage_option['12150'][9] = 0
                equipment_damage_option['13150'][9] = 0
                equipment_damage_option['14150'][9] = 0
                equipment_damage_option['15150'][9] = 24
            elif element_type == '암':
                equipment_damage_option['12150'][9] = 24
                equipment_damage_option['13150'][9] = 0
                equipment_damage_option['14150'][9] = 0
                equipment_damage_option['15150'][9] = 0
            else:
                equipment_damage_option['12150'][9] = 0
                equipment_damage_option['13150'][9] = 24
                equipment_damage_option['14150'][9] = 0
                equipment_damage_option['15150'][9] = 0

        # 사막 스증
        desert_super_armor = self.value_dict.get('desert_super_armor')
        if desert_super_armor == '노피격(6+4)':
            equipment_damage_option['1071'][11] = 6
            equipment_damage_option['1072'][11] = 1.15 * 1.06 * 100 - 100
            equipment_damage_option['1073'][11] = 1.15 * 1.44 * 1.04 * 1.06 * 100 - 100
        elif desert_super_armor == '슈아파괴(X)':
            equipment_damage_option['1071'][11] = 0
            equipment_damage_option['1072'][11] = 15
            equipment_damage_option['1073'][11] = 1.15 * 1.44 * 100 - 100
        else:
            equipment_damage_option['1071'][11] = 6
            equipment_damage_option['1072'][11] = 1.15 * 1.06 * 100 - 100
            equipment_damage_option['1073'][11] = 1.15 * 1.44 * 1.06 * 100 - 100

        # 흐름
        equipment_damage_option['11130'][12] = float(self.value_dict.get('flow_jacket'))
        equipment_damage_option['11131'][12] = float(self.value_dict.get('flow_jacket'))
        equipment_damage_option['12130'][12] = float(self.value_dict.get('flow_pants'))
        equipment_damage_option['13130'][12] = float(self.value_dict.get('flow_shoulder'))
        equipment_damage_option['14130'][12] = float(self.value_dict.get('flow_waist'))
        equipment_damage_option['15130'][12] = float(self.value_dict.get('flow_shoes'))

        # 선택신
        equipment_damage_option['15140'][12] = float(self.value_dict.get('selection_shoes'))















