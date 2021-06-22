from multiprocessing import Process
import os


class Test:
    num_arr = []
    procs = []

    def __init__(self):
        cpu_num = os.cpu_count()
        print(cpu_num)
        for i in range(0, cpu_num):
            self.num_arr.append(int(1000000 / cpu_num))

        for index, number in enumerate(self.num_arr):
            proc = Process(target=self.count, args=(number,))
            self.procs.append(proc)
            proc.start()

        for proc in self.procs:
            proc.join()

        print("종료")

    def count(self, cnt):
        proc = os.getpid()
        for i in range(cnt):
            a = i


