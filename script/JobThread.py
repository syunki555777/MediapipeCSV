import threading
import VideoOutput
from tkinter import messagebox
import tkinter as tk

class JobThread(threading.Thread):
    def __init__(self, progress,start_button,model_path,csv_path,video_path,progress_text, progress_image_update_function):
        super().__init__()

        self.progress = progress
        self.start_button = start_button
        self.model_path = model_path
        self.csv_path = csv_path
        self.video_path = video_path
        self.progress_text = progress_text
        self.progress_image_update_function = progress_image_update_function

    def setCSVPath(self,path):
        self.csv_path = path

    def setVideoPath(self,path):
        self.video_path = path
    def run(self):
        if self.video_path == '':
            messagebox.showwarning("Warning", "Job cannot start. Please provide the video path.")
            self.stop()
            return False
        if self.csv_path == '':
            messagebox.showwarning("Warning", "Job cannot start. Please provide the csv path.")
            self.stop()
            return False
        print("JobThread started")

        try:
            VideoOutput.extract_face_landmarks_to_csv(video_path=self.video_path,csv_path=self.csv_path,model_path=self.model_path,progress_bar=self.progress,progress_text=self.progress_text,progress_image_update_function=self.progress_image_update_function)
        except Exception as e:
            print(e)

            self.stop()
            self.progress_text.set("エラーが発生しました。:"+str(e))
            return False
        # 終了
        self.stop()
        self.progress_text.set("処理が完了しました。")
    def safe_showwarning(self, title, msg):
        root = tk.Tk()
        root.after(0, messagebox.showwarning, title, msg)

    def stop(self):
        print("JobThread stopped")
        self.start_button["state"] = "enable"

