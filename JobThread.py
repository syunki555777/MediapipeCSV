import threading
import VideoOutput
from tkinter import messagebox

class JobThread(threading.Thread):
    def __init__(self, progress,start_button,model_path,csv_path,video_path):
        super().__init__()

        self.progress = progress
        self.start_button = start_button
        self.model_path = model_path
        self.csv_path = csv_path
        self.video_path = video_path

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
            VideoOutput.extract_face_landmarks_to_csv(video_path=self.video_path,csv_path=self.csv_path,model_path=self.model_path,progress_bar=self.progress)
        except Exception as e:
            messagebox.showwarning("Error", "Error occured." + str(e))
            print(e)
        # 終了
        self.stop()

    def stop(self):
        print("JobThread stopped")
        self.start_button["state"] = "enable"
        self.progress.destroy()