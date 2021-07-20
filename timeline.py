import datetime
import threading
import tkinter.messagebox
import urllib.request
from urllib import parse
from json import loads
import data.dataload
import queue


try:
    import api_key
    apikey = api_key.get_api_key()
except:
    try:
        api_txt_file = open("API_key.txt", "r")
        apikey = api_txt_file.readline()
        if apikey == "":
            tkinter.messagebox.showerror("에러",
                                         "API 접근 권한 획득 실패. API_key.txt 파일에 API 키를 입력하고 다시 실행하세요.")
        api_txt_file.close()
    except:
        tkinter.messagebox.showerror("에러", "API 접근 권한 획득 실패. API_key.txt 파일에 API 키를 입력하고 다시 실행하세요.")
time_code = '504,505,506,507,508,510,511,512,513,514'


class Timeline:
    def __init__(self, server, name):
        self.error = ""
        server_dict = {'안톤': 'anton', '바칼': 'bakal', '카인': 'cain', '카시야스': 'casillas',
                       '디레지에': 'diregie', '힐더': 'hilder', '프레이': 'prey', '시로코': 'siroco'}
        self.server = server_dict.get(server)
        if self.server is None:
            tkinter.messagebox.showerror(title='타임라인 조회', message="서버 입력값 오류")
            return
        self.name = str(name)
        self.cha_id = None
        self.timeline_list = []
        self.main_queue = queue.Queue()
        self.thread_queue = queue.Queue()
        self.equipment_name_by_code = data.dataload.total_database[1]
        self.return_lists = []

        try:
            self.load_cha_id()
        except:
            tkinter.messagebox.showerror(title='타임라인 조회', message="캐릭 조회 실패")
            return
        try:
            self.load_timeline_api()
        except:
            tkinter.messagebox.showerror(title='타임라인 조회', message="타임라인 조회 실패")
            return

    def return_list(self):
        return self.return_lists

    def load_cha_id(self):
        cha_id_api = urllib.request.urlopen(
            'https://api.neople.co.kr/df/servers/' + self.server + '/characters?characterName=' + parse.quote(
                self.name) + '&apikey=' + apikey)
        cha_id_dic = loads(cha_id_api.read().decode("utf-8"))
        self.cha_id = cha_id_dic['rows'][0]['characterId']
        print(self.cha_id)

    def load_timeline_api(self):
        target_day = datetime.date(2020, 1, 1)
        target_day_str = target_day.strftime("%Y%m%dT0000")
        today = datetime.date.today()
        day_dif = (today - target_day).days
        while day_dif > 89:
            day_after = target_day + datetime.timedelta(days=89)
            day_after_str = day_after.strftime("%Y%m%dT0000")
            now_thread = threading.Thread(target=self.get_api_equipment_list,
                                          args=(day_after_str, target_day_str))
            self.thread_queue.put(now_thread)
            now_thread.start()
            target_day = day_after
            target_day_str = day_after_str
            day_dif = (today - target_day).days
        day_after = datetime.datetime.now()
        day_after_str = day_after.strftime("%Y%m%dT%H%M")
        now_thread = threading.Thread(target=self.get_api_equipment_list,
                                      args=(day_after_str, target_day_str), daemon=True)
        self.thread_queue.put(now_thread)
        now_thread.start()

        while self.thread_queue.qsize():
            self.thread_queue.get().join()
        while self.main_queue.qsize():
            now_name = self.main_queue.get()
            now_code = self.equipment_name_by_code.get(now_name)
            if now_code is None or len(now_code) == 6:
                continue
            self.return_lists.append(now_code)
        print(len(self.return_lists))

    def get_api_equipment_list(self, time_start, time_end):
        timeline = urllib.request.urlopen(
            'https://api.neople.co.kr/df/servers/' + self.server + '/characters/' +
            self.cha_id + '/timeline?limit=100&code=' + time_code + '&startDate=' +
            time_end + '&endDate=' + time_start + '&apikey=' + apikey)
        timeline = loads(timeline.read().decode("utf-8"))['timeline']
        show_next = timeline['next']
        if show_next is not None:
            now_thread = threading.Thread(target=self.get_api_next_list, args=(show_next,), daemon=True)
            self.thread_queue.put(now_thread)
            now_thread.start()
        timeline_list = timeline['rows']
        for now in timeline_list:
            equipment_name = now['data']['itemName']
            self.main_queue.put(equipment_name)

    def get_api_next_list(self, next_code):
        timeline_next = urllib.request.urlopen(
            'https://api.neople.co.kr/df/servers/' + self.server + '/characters/' + self.cha_id + '/timeline?next='
            + next_code + '&apikey=' + apikey)
        timeline_next = loads(timeline_next.read().decode("utf-8"))['timeline']
        show_next = timeline_next['next']
        if show_next is not None:
            now_thread = threading.Thread(target=self.get_api_next_list, args=(show_next,), daemon=True)
            self.thread_queue.put(now_thread)
            now_thread.start()
        timeline_list = timeline_next['rows']
        for now in timeline_list:
            equipment_name = now['data']['itemName']
            self.main_queue.put(equipment_name)













