import queue
import threading
import time
class JobQueue:

    def __init__(self):
        self.q = queue.Queue()
    def run(self):

    def getWiget(self):


    def add_video(self, video_path, csv_path):


# 使用例
def task1():
    print("Task 1 is running")

def task2():
    print("Task 2 is running")

job_q = JobQueue()
job_q.add_task(task1)
job_q.add_task(task2)